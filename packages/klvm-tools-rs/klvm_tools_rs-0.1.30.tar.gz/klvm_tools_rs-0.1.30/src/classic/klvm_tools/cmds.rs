use core::cell::RefCell;

use std::collections::{BTreeMap, HashMap};
use std::fs;
use std::io;
use std::io::Write;
use std::mem::swap;
use std::rc::Rc;
use std::sync::mpsc::{channel, Receiver, Sender};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::SystemTime;

use core::cmp::max;

use linked_hash_map::LinkedHashMap;
use yaml_rust::{Yaml, YamlEmitter};

use klvm_rs::allocator::{Allocator, NodePtr};
use klvm_rs::reduction::EvalErr;
use klvm_rs::run_program::PreEval;

use crate::classic::klvm::__type_compatibility__::{t, Bytes, BytesFromType, Stream, Tuple};
use crate::classic::klvm::keyword_from_atom;
use crate::classic::klvm::serialize::{sexp_from_stream, sexp_to_stream, SimpleCreateKLVMObject};
use crate::classic::klvm::sexp::{enlist, proper_list, sexp_as_bin};
use crate::classic::klvm_tools::binutils::{assemble_from_ir, disassemble, disassemble_with_kw};
use crate::classic::klvm_tools::debug::{
    check_unused, trace_pre_eval, trace_to_table, trace_to_text,
};
use crate::classic::klvm_tools::ir::reader::read_ir;
use crate::classic::klvm_tools::klvmc::detect_modern;
use crate::classic::klvm_tools::sha256tree::sha256tree;
use crate::classic::klvm_tools::stages;
use crate::classic::klvm_tools::stages::stage_0::{
    DefaultProgramRunner, RunProgramOption, TRunProgram,
};
use crate::classic::klvm_tools::stages::stage_2::operators::run_program_for_search_paths;
use crate::classic::platform::PathJoin;

use crate::classic::platform::argparse::{
    Argument, ArgumentParser, ArgumentValue, ArgumentValueConv, IntConversion, NArgsSpec,
    TArgOptionAction, TArgumentParserProps,
};

use crate::compiler::cldb::{hex_to_modern_sexp, CldbNoOverride, CldbRun, CldbRunEnv};
use crate::compiler::compiler::{compile_file, run_optimizer, DefaultCompilerOpts};
use crate::compiler::comptypes::{CompileErr, CompilerOpts};
use crate::compiler::debug::build_symbol_table_mut;
use crate::compiler::klvm::start_step;
use crate::compiler::prims;
use crate::compiler::sexp;
use crate::compiler::sexp::parse_sexp;
use crate::compiler::srcloc::Srcloc;
use crate::util::collapse;

pub struct PathOrCodeConv {}

impl ArgumentValueConv for PathOrCodeConv {
    fn convert(&self, arg: &str) -> Result<ArgumentValue, String> {
        match fs::read_to_string(arg) {
            Ok(s) => Ok(ArgumentValue::ArgString(Some(arg.to_string()), s)),
            Err(_) => Ok(ArgumentValue::ArgString(None, arg.to_string())),
        }
    }
}

// export function stream_to_bin(write_f: (f: Stream) => void){
//   const f = new Stream();
//   write_f(f);
//   return f.getValue();
// }

pub trait TConversion {
    fn invoke<'a>(
        &self,
        allocator: &'a mut Allocator,
        text: &str,
    ) -> Result<Tuple<NodePtr, String>, String>;
}
pub fn call_tool(
    allocator: &mut Allocator,
    tool_name: &str,
    desc: &str,
    conversion: Box<dyn TConversion>,
    input_args: &[String],
) {
    let props = TArgumentParserProps {
        description: desc.to_string(),
        prog: tool_name.to_string(),
    };

    let mut parser = ArgumentParser::new(Some(props));
    parser.add_argument(
        vec!["-H".to_string(), "--script-hash".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Show only sha256 tree hash of program".to_string()),
    );
    parser.add_argument(
        vec!["path_or_code".to_string()],
        Argument::new()
            .set_n_args(NArgsSpec::KleeneStar)
            .set_type(Rc::new(PathOrCodeConv {}))
            .set_help("path to klvm script, or literal script".to_string()),
    );

    let rest_args: Vec<String> = input_args.iter().skip(1).cloned().collect();
    let args_res = parser.parse_args(&rest_args);
    let args: HashMap<String, ArgumentValue> = match args_res {
        Ok(a) => a,
        Err(e) => {
            println!("{}", e);
            return;
        }
    };

    let args_path_or_code_val = match args.get(&"path_or_code".to_string()) {
        None => ArgumentValue::ArgArray(vec![]),
        Some(v) => v.clone(),
    };

    let args_path_or_code = match args_path_or_code_val {
        ArgumentValue::ArgArray(v) => v,
        _ => vec![],
    };

    for program in args_path_or_code {
        match program {
            ArgumentValue::ArgString(_, s) => {
                if s == "-" {
                    panic!("Read stdin is not supported at this time");
                }

                let conv_result = conversion.invoke(allocator, &s);
                match conv_result {
                    Ok(conv_result) => {
                        let sexp = *conv_result.first();
                        let text = conv_result.rest();
                        if args.contains_key(&"script_hash".to_string()) {
                            println!("{}", sha256tree(allocator, sexp).hex());
                        } else if !text.is_empty() {
                            println!("{}", text);
                        }
                    }
                    Err(e) => {
                        panic!("Conversion returned error: {:?}", e);
                    }
                }
            }
            _ => {
                panic!("inappropriate argument conversion");
            }
        }
    }
}

pub struct OpcConversion {}

impl TConversion for OpcConversion {
    fn invoke<'a>(
        &self,
        allocator: &'a mut Allocator,
        hex_text: &str,
    ) -> Result<Tuple<NodePtr, String>, String> {
        read_ir(hex_text)
            .and_then(|ir_sexp| assemble_from_ir(allocator, Rc::new(ir_sexp)).map_err(|e| e.1))
            .map(|sexp| t(sexp, sexp_as_bin(allocator, sexp).hex()))
    }
}

pub struct OpdConversion {}

impl TConversion for OpdConversion {
    fn invoke<'a>(
        &self,
        allocator: &'a mut Allocator,
        hex_text: &str,
    ) -> Result<Tuple<NodePtr, String>, String> {
        let mut stream = Stream::new(Some(Bytes::new(Some(BytesFromType::Hex(
            hex_text.to_string(),
        )))));

        sexp_from_stream(allocator, &mut stream, Box::new(SimpleCreateKLVMObject {}))
            .map_err(|e| e.1)
            .map(|sexp| {
                let disassembled = disassemble(allocator, sexp.1);
                t(sexp.1, disassembled)
            })
    }
}

pub fn opc(args: &[String]) {
    let mut allocator = Allocator::new();
    call_tool(
        &mut allocator,
        "opc",
        "Compile a klvm script.",
        Box::new(OpcConversion {}),
        args,
    );
}

pub fn opd(args: &[String]) {
    let mut allocator = Allocator::new();
    call_tool(
        &mut allocator,
        "opd",
        "Disassemble a compiled klvm script from hex.",
        Box::new(OpdConversion {}),
        args,
    );
}

struct StageImport {}

impl ArgumentValueConv for StageImport {
    fn convert(&self, arg: &str) -> Result<ArgumentValue, String> {
        if arg == "0" {
            return Ok(ArgumentValue::ArgInt(0));
        } else if arg == "1" {
            return Ok(ArgumentValue::ArgInt(1));
        } else if arg == "2" {
            return Ok(ArgumentValue::ArgInt(2));
        }
        Err(format!("Unknown stage: {}", arg))
    }
}

pub fn run(args: &[String]) {
    let mut s = Stream::new(None);
    launch_tool(&mut s, args, "run", 2);
    io::stdout()
        .write_all(s.get_value().data())
        .expect("stdout");
}

pub fn brun(args: &[String]) {
    let mut s = Stream::new(None);
    launch_tool(&mut s, args, "brun", 0);
    io::stdout()
        .write_all(s.get_value().data())
        .expect("stdout");
}

fn to_yaml(entries: &[BTreeMap<String, String>]) -> Yaml {
    let result_array: Vec<Yaml> = entries
        .iter()
        .map(|tm| {
            let mut h = LinkedHashMap::new();
            for (k, v) in tm.iter() {
                h.insert(Yaml::String(k.clone()), Yaml::String(v.clone()));
            }
            Yaml::Hash(h)
        })
        .collect();
    Yaml::Array(result_array)
}

pub fn cldb(args: &[String]) {
    let tool_name = "cldb".to_string();
    let props = TArgumentParserProps {
        description: "Execute a klvm script.".to_string(),
        prog: format!("klvm_tools {}", tool_name),
    };

    let mut search_paths = Vec::new();
    let mut parser = ArgumentParser::new(Some(props));
    parser.add_argument(
        vec!["-i".to_string(), "--include".to_string()],
        Argument::new()
            .set_type(Rc::new(PathJoin {}))
            .set_help("add a search path for included files".to_string())
            .set_action(TArgOptionAction::Append)
            .set_default(ArgumentValue::ArgArray(vec![])),
    );
    parser.add_argument(
        vec!["-O".to_string(), "--optimize".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("run optimizer".to_string()),
    );
    parser.add_argument(
        vec!["-x".to_string(), "--hex".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("parse input program and arguments from hex".to_string()),
    );
    parser.add_argument(
        vec!["-y".to_string(), "--symbol-table".to_string()],
        Argument::new()
            .set_type(Rc::new(PathOrCodeConv {}))
            .set_help("path to symbol file".to_string()),
    );
    parser.add_argument(
        vec!["path_or_code".to_string()],
        Argument::new()
            .set_type(Rc::new(PathOrCodeConv {}))
            .set_help("filepath to klvm script, or a literal script".to_string()),
    );
    parser.add_argument(
        vec!["env".to_string()],
        Argument::new()
            .set_n_args(NArgsSpec::Optional)
            .set_type(Rc::new(PathOrCodeConv {}))
            .set_help("klvm script environment, as klvm src, or hex".to_string()),
    );
    let arg_vec = args[1..].to_vec();

    let mut input_file = None;
    let mut input_program = "()".to_string();

    let prog_srcloc = Srcloc::start("*program*");
    let args_srcloc = Srcloc::start("*args*");

    let mut args = Rc::new(sexp::SExp::atom_from_string(args_srcloc.clone(), ""));
    let mut parsed_args_result: String = "".to_string();

    let parsed_args: HashMap<String, ArgumentValue> = match parser.parse_args(&arg_vec) {
        Err(e) => {
            println!("FAIL: {}", e);
            return;
        }
        Ok(pa) => pa,
    };

    if let Some(ArgumentValue::ArgArray(v)) = parsed_args.get("include") {
        for p in v {
            if let ArgumentValue::ArgString(_, s) = p {
                search_paths.push(s.to_string());
            }
        }
    }

    if let Some(ArgumentValue::ArgString(file, path_or_code)) = parsed_args.get("path_or_code") {
        input_file = file.clone();
        input_program = path_or_code.to_string();
    }

    if let Some(ArgumentValue::ArgString(_, s)) = parsed_args.get("env") {
        parsed_args_result = s.to_string();
    }

    let mut allocator = Allocator::new();

    let symbol_table = parsed_args
        .get("symbol_table")
        .and_then(|jstring| match jstring {
            ArgumentValue::ArgString(_, s) => {
                let decoded_symbol_table: Option<HashMap<String, String>> =
                    serde_json::from_str(s).ok();
                decoded_symbol_table
            }
            _ => None,
        });

    let do_optimize = parsed_args
        .get("optimize")
        .map(|x| matches!(x, ArgumentValue::ArgBool(true)))
        .unwrap_or_else(|| false);
    let runner = Rc::new(DefaultProgramRunner::new());
    let use_filename = input_file
        .clone()
        .unwrap_or_else(|| "*command*".to_string());
    let opts = Rc::new(DefaultCompilerOpts::new(&use_filename))
        .set_optimize(do_optimize)
        .set_search_paths(&search_paths);

    let mut use_symbol_table = symbol_table.unwrap_or_default();
    let unopt_res = compile_file(
        &mut allocator,
        runner.clone(),
        opts.clone(),
        &input_program,
        &mut use_symbol_table,
    );

    let mut output = Vec::new();
    let yamlette_string = |to_print: Vec<BTreeMap<String, String>>| {
        let mut result = String::new();
        let mut emitter = YamlEmitter::new(&mut result);
        match emitter.dump(&to_yaml(&to_print)) {
            Ok(_) => result,
            Err(e) => format!("error producing yaml: {:?}", e),
        }
    };

    let res = match parsed_args.get("hex") {
        Some(ArgumentValue::ArgBool(true)) => hex_to_modern_sexp(
            &mut allocator,
            &use_symbol_table,
            prog_srcloc.clone(),
            &input_program,
        )
        .map_err(|_| CompileErr(prog_srcloc, "Failed to parse hex".to_string())),
        _ => {
            if do_optimize {
                unopt_res.and_then(|x| run_optimizer(&mut allocator, runner.clone(), Rc::new(x)))
            } else {
                unopt_res.map(Rc::new)
            }
        }
    };

    let program = match res {
        Ok(r) => r,
        Err(c) => {
            let mut parse_error = BTreeMap::new();
            parse_error.insert("Error-Location".to_string(), c.0.to_string());
            parse_error.insert("Error".to_string(), c.1);
            output.push(parse_error.clone());
            println!("{}", yamlette_string(output));
            return;
        }
    };

    match parsed_args.get("hex") {
        Some(ArgumentValue::ArgBool(true)) => {
            match hex_to_modern_sexp(
                &mut allocator,
                &HashMap::new(),
                args_srcloc,
                &parsed_args_result,
            ) {
                Ok(r) => {
                    args = r;
                }
                Err(p) => {
                    let mut parse_error = BTreeMap::new();
                    parse_error.insert("Error".to_string(), p.to_string());
                    output.push(parse_error.clone());
                    println!("{}", yamlette_string(output));
                    return;
                }
            }
        }
        _ => match parse_sexp(Srcloc::start("*arg*"), parsed_args_result.bytes()) {
            Ok(r) => {
                if !r.is_empty() {
                    args = r[0].clone();
                }
            }
            Err(c) => {
                let mut parse_error = BTreeMap::new();
                parse_error.insert("Error-Location".to_string(), c.0.to_string());
                parse_error.insert("Error".to_string(), c.1);
                output.push(parse_error.clone());
                println!("{}", yamlette_string(output));
                return;
            }
        },
    };

    let mut prim_map = HashMap::new();
    for p in prims::prims().iter() {
        prim_map.insert(p.0.clone(), Rc::new(p.1.clone()));
    }
    let program_lines: Vec<String> = input_program.lines().map(|x| x.to_string()).collect();
    let step = start_step(program, args);
    let cldbenv = CldbRunEnv::new(
        input_file,
        program_lines,
        Box::new(CldbNoOverride::new_symbols(use_symbol_table)),
    );
    let mut cldbrun = CldbRun::new(runner, Rc::new(prim_map), Box::new(cldbenv), step);

    loop {
        if cldbrun.is_ended() {
            println!("{}", yamlette_string(output));
            return;
        }

        if let Some(result) = cldbrun.step(&mut allocator) {
            output.push(result);
        }
    }
}

struct RunLog<T> {
    log_entries: RefCell<Vec<T>>,
}

impl<T> RunLog<T> {
    fn push(&self, new_log: T) {
        self.log_entries.replace_with(|log| {
            let mut empty_log = Vec::new();
            swap(&mut empty_log, &mut *log);
            empty_log.push(new_log);
            empty_log
        });
    }

    fn finish(&self) -> Vec<T> {
        let mut empty_log = Vec::new();
        self.log_entries.replace_with(|log| {
            swap(&mut empty_log, &mut *log);
            Vec::new()
        });
        empty_log
    }
}

fn calculate_cost_offset(
    allocator: &mut Allocator,
    run_program: Rc<dyn TRunProgram>,
    run_script: NodePtr,
) -> i64 {
    /*
     These commands are used by the test suite, and many of them expect certain costs.
     If boilerplate invocation code changes by a fixed cost, you can tweak this
     value so you don't have to change all the tests' expected costs.
     Eventually you should re-tare this to zero and alter the tests' costs though.
     This is a hack and need to go away, probably when we do dialects for real,
     and then the dialect can have a `run_program` API.
    */
    let almost_empty_list = enlist(allocator, &[allocator.null()]).unwrap();
    let cost = run_program
        .run_program(allocator, run_script, almost_empty_list, None)
        .map(|x| x.0)
        .unwrap_or_else(|_| 0);

    53 - cost as i64
}

fn fix_log(
    allocator: &mut Allocator,
    log_result: &mut [NodePtr],
    log_updates: &[(NodePtr, Option<NodePtr>)],
) {
    let mut update_map: HashMap<NodePtr, Option<NodePtr>> = HashMap::new();
    for update in log_updates {
        update_map.insert(update.0, update.1);
    }

    for (i, entry) in log_result.to_vec().iter().enumerate() {
        update_map.get(entry).and_then(|v| *v).map(|v| {
            proper_list(allocator, *entry, true).map(|list| {
                let mut updated = list.to_vec();
                updated.push(v);
                log_result[i] = enlist(allocator, &updated).unwrap();
            })
        });
    }
}

fn write_sym_output(compiled_lookup: &HashMap<String, String>, path: &str) -> Result<(), String> {
    m! {
        output <- serde_json::to_string(compiled_lookup).map_err(|_| {
            "failed to serialize to json".to_string()
        });

        fs::write(path, output).map_err(|_| {
            format!("failed to write {}", path)
        }).map(|_| ())
    }
}

pub fn launch_tool(stdout: &mut Stream, args: &[String], tool_name: &str, default_stage: u32) {
    let props = TArgumentParserProps {
        description: "Execute a klvm script.".to_string(),
        prog: format!("klvm_tools {}", tool_name),
    };

    let mut parser = ArgumentParser::new(Some(props));
    parser.add_argument(
        vec!["-s".to_string(), "--stage".to_string()],
        Argument::new()
            .set_type(Rc::new(StageImport {}))
            .set_help("stage number to include".to_string())
            .set_default(ArgumentValue::ArgInt(default_stage as i64)),
    );
    parser.add_argument(
        vec!["--strict".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Unknown opcodes are always fatal errors in strict mode".to_string()),
    );
    parser.add_argument(
        vec!["-x".to_string(), "--hex".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Read program and environment as hexadecimal bytecode".to_string()),
    );
    parser.add_argument(
        vec!["-v".to_string(), "--verbose".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Display resolve of all reductions, for debugging".to_string()),
    );
    parser.add_argument(
        vec!["-t".to_string(), "--table".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Print diagnostic table of reductions, for debugging".to_string()),
    );
    parser.add_argument(
        vec!["-c".to_string(), "--cost".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Show cost".to_string()),
    );
    parser.add_argument(
        vec!["--time".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Print execution time".to_string()),
    );
    parser.add_argument(
        vec!["-d".to_string(), "--dump".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("dump hex version of final output".to_string()),
    );
    parser.add_argument(
        vec!["--quiet".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Suppress printing the program result".to_string()),
    );
    parser.add_argument(
        vec!["-y".to_string(), "--symbol-table".to_string()],
        Argument::new()
            .set_type(Rc::new(PathJoin {}))
            .set_help(".SYM file generated by compiler".to_string()),
    );
    parser.add_argument(
        vec!["-n".to_string(), "--no-keywords".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Output result as data, not as a program".to_string()),
    );
    parser.add_argument(
        vec!["-i".to_string(), "--include".to_string()],
        Argument::new()
            .set_type(Rc::new(PathJoin {}))
            .set_help("add a search path for included files".to_string())
            .set_action(TArgOptionAction::Append)
            .set_default(ArgumentValue::ArgArray(vec![])),
    );
    parser.add_argument(
        vec!["path_or_code".to_string()],
        Argument::new()
            .set_type(Rc::new(PathOrCodeConv {}))
            .set_help("filepath to klvm script, or a literal script".to_string()),
    );
    parser.add_argument(
        vec!["env".to_string()],
        Argument::new()
            .set_n_args(NArgsSpec::Optional)
            .set_type(Rc::new(PathOrCodeConv {}))
            .set_help("klvm script environment, as klvm src, or hex".to_string()),
    );
    parser.add_argument(
        vec!["-m".to_string(), "--max-cost".to_string()],
        Argument::new()
            .set_type(Rc::new(IntConversion::new(Rc::new(|| "help".to_string()))))
            .set_default(ArgumentValue::ArgInt(11000000000))
            .set_help("Maximum cost".to_string()),
    );
    parser.add_argument(
        vec!["-O".to_string(), "--optimize".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("run optimizer".to_string()),
    );
    parser.add_argument(
        vec!["--only-exn".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Only show frames along the exception path".to_string()),
    );
    parser.add_argument(
        vec!["-g".to_string(), "--extra-syms".to_string()],
        Argument::new()
            .set_action(TArgOptionAction::StoreTrue)
            .set_help("Produce more diagnostic info in symbols".to_string()),
    );
    parser.add_argument(
        vec!["--symbol-output-file".to_string()],
        Argument::new()
            .set_type(Rc::new(PathJoin {}))
            .set_default(ArgumentValue::ArgString(None, "main.sym".to_string())),
    );

    if tool_name == "run" {
        parser.add_argument(
            vec!["--check-unused-args".to_string()],
            Argument::new()
                .set_action(TArgOptionAction::StoreTrue)
                .set_help(
                    "check for unused uncurried parameters (by convention lower case)".to_string(),
                ),
        );
    }

    let arg_vec = args[1..].to_vec();
    let parsed_args: HashMap<String, ArgumentValue> = match parser.parse_args(&arg_vec) {
        Err(e) => {
            stdout.write_str(&format!("FAIL: {}\n", e));
            return;
        }
        Ok(pa) => pa,
    };

    let empty_map = HashMap::new();
    let keywords = match parsed_args.get("no_keywords") {
        None => keyword_from_atom(),
        Some(ArgumentValue::ArgBool(_b)) => &empty_map,
        _ => keyword_from_atom(),
    };

    // If extra symbol output is desired (not all keys are hashes, but there's
    // more info).
    let extra_symbol_info = parsed_args.get("extra_syms").map(|_| true).unwrap_or(false);

    // Get name of included file so we can use it to initialize the compiler's
    // runner, which contains operators used at compile time in klvm to update
    // symbols.  This is the only means we have of communicating with the
    // compilation process from this level.
    let mut input_file = None;
    let mut input_program = "()".to_string();

    if let Some(ArgumentValue::ArgString(file, path_or_code)) = parsed_args.get("path_or_code") {
        input_file = file.clone();
        input_program = path_or_code.to_string();
    }

    let reported_input_file = input_file
        .as_ref()
        .cloned()
        .unwrap_or_else(|| "*command*".to_string());

    let dpr;
    let run_program: Rc<dyn TRunProgram>;
    let mut search_paths = Vec::new();
    match parsed_args.get("include") {
        Some(ArgumentValue::ArgArray(v)) => {
            let mut bare_paths = Vec::with_capacity(v.len());
            for p in v {
                if let ArgumentValue::ArgString(_, s) = p {
                    bare_paths.push(s.to_string());
                }
            }
            let special_runner =
                run_program_for_search_paths(&reported_input_file, &bare_paths, extra_symbol_info);
            search_paths = bare_paths;
            dpr = special_runner.clone();
            run_program = special_runner;
        }
        _ => {
            let ordinary_runner =
                run_program_for_search_paths(&reported_input_file, &Vec::new(), extra_symbol_info);
            dpr = ordinary_runner.clone();
            run_program = ordinary_runner;
        }
    }

    let mut allocator = Allocator::new();

    let input_serialized = None;
    let mut input_sexp: Option<NodePtr> = None;

    let time_start = SystemTime::now();
    let mut time_read_hex = SystemTime::now();
    let mut time_assemble = SystemTime::now();

    let mut input_args = "()".to_string();

    if let Some(ArgumentValue::ArgString(file, path_or_code)) = parsed_args.get("env") {
        input_file = file.clone();
        input_args = path_or_code.to_string();
    }

    match parsed_args.get("hex") {
        Some(_) => {
            let assembled_serialized =
                Bytes::new(Some(BytesFromType::Hex(input_program.to_string())));

            let env_serialized = if input_args.is_empty() {
                Bytes::new(Some(BytesFromType::Hex("80".to_string())))
            } else {
                Bytes::new(Some(BytesFromType::Hex(input_args)))
            };

            time_read_hex = SystemTime::now();

            let mut prog_stream = Stream::new(Some(assembled_serialized));
            let input_prog_sexp = sexp_from_stream(
                &mut allocator,
                &mut prog_stream,
                Box::new(SimpleCreateKLVMObject {}),
            )
            .map(|x| Some(x.1))
            .unwrap();

            let mut arg_stream = Stream::new(Some(env_serialized));
            let input_arg_sexp = sexp_from_stream(
                &mut allocator,
                &mut arg_stream,
                Box::new(SimpleCreateKLVMObject {}),
            )
            .map(|x| Some(x.1))
            .unwrap();
            if let (Some(ip), Some(ia)) = (input_prog_sexp, input_arg_sexp) {
                input_sexp = allocator.new_pair(ip, ia).ok();
            }
        }
        _ => {
            let src_sexp;
            if let Some(ArgumentValue::ArgString(f, content)) = parsed_args.get("path_or_code") {
                match read_ir(content) {
                    Ok(s) => {
                        input_program = content.clone();
                        input_file = f.clone();
                        src_sexp = s;
                    }
                    Err(e) => {
                        stdout.write_str(&format!("FAIL: {}\n", e));
                        return;
                    }
                }
            } else {
                stdout.write_str(&format!("FAIL: {}\n", "non-string argument"));
                return;
            }

            let assembled_sexp = assemble_from_ir(&mut allocator, Rc::new(src_sexp)).unwrap();
            let mut parsed_args_result = "()".to_string();

            if let Some(ArgumentValue::ArgString(_f, s)) = parsed_args.get("env") {
                parsed_args_result = s.to_string();
            }

            let env_ir = read_ir(&parsed_args_result).unwrap();
            let env = assemble_from_ir(&mut allocator, Rc::new(env_ir)).unwrap();
            time_assemble = SystemTime::now();

            input_sexp = allocator.new_pair(assembled_sexp, env).ok();
        }
    }

    // Symbol table related checks: should one be loaded, should one be saved.
    // This code is confusingly woven due to 'run' and 'brun' serving many roles.
    let mut symbol_table: Option<HashMap<String, String>> = None;
    let mut emit_symbol_output = false;

    let symbol_table_clone = parsed_args
        .get("symbol_table")
        .and_then(|jstring| match jstring {
            ArgumentValue::ArgString(_, s) => fs::read_to_string(s).ok().and_then(|s| {
                let decoded_symbol_table: Option<HashMap<String, String>> =
                    serde_json::from_str(&s).ok();
                decoded_symbol_table
            }),
            _ => None,
        })
        .map(|st| {
            emit_symbol_output = true;
            symbol_table = Some(st.clone());
            st
        });

    if let Some(ArgumentValue::ArgBool(true)) = parsed_args.get("verbose") {
        emit_symbol_output = true;
    }

    // Add unused check.
    let do_check_unused = parsed_args
        .get("check_unused_args")
        .map(|a| matches!(a, ArgumentValue::ArgBool(true)))
        .unwrap_or(false);

    let dialect = input_sexp.and_then(|i| detect_modern(&mut allocator, i));
    let mut stderr_output = |s: String| {
        if dialect.is_some() {
            eprintln!("{}", s);
        } else {
            stdout.write_str(&s);
        }
    };

    if do_check_unused {
        let opts =
            Rc::new(DefaultCompilerOpts::new(&reported_input_file)).set_search_paths(&search_paths);
        match check_unused(opts, &input_program) {
            Ok((success, output)) => {
                stderr_output(output);
                if !success {
                    return;
                }
            }
            Err(e) => {
                stderr_output(format!("{}: {}\n", e.0, e.1));
                return;
            }
        }
    }

    let symbol_table_output = parsed_args
        .get("symbol_output_file")
        .and_then(|s| {
            if let ArgumentValue::ArgString(_, v) = s {
                Some(v.clone())
            } else {
                None
            }
        })
        .unwrap_or_else(|| "main.sym".to_string());

    // In testing: short circuit for modern compilation.
    if let Some(dialect) = dialect {
        let do_optimize = parsed_args
            .get("optimize")
            .map(|x| matches!(x, ArgumentValue::ArgBool(true)))
            .unwrap_or_else(|| false);
        let runner = Rc::new(DefaultProgramRunner::new());
        let use_filename = input_file.unwrap_or_else(|| "*command*".to_string());
        let opts = Rc::new(DefaultCompilerOpts::new(&use_filename))
            .set_optimize(do_optimize)
            .set_search_paths(&search_paths)
            .set_frontend_opt(dialect > 21);
        let mut symbol_table = HashMap::new();

        let unopt_res = compile_file(
            &mut allocator,
            runner.clone(),
            opts.clone(),
            &input_program,
            &mut symbol_table,
        );
        let res = if do_optimize {
            unopt_res.and_then(|x| run_optimizer(&mut allocator, runner, Rc::new(x)))
        } else {
            unopt_res.map(Rc::new)
        };

        match res {
            Ok(r) => {
                stdout.write_str(&r.to_string());

                build_symbol_table_mut(&mut symbol_table, &r);
                write_sym_output(&symbol_table, &symbol_table_output).expect("writing symbols");
            }
            Err(c) => {
                stdout.write_str(&format!("{}: {}", c.0, c.1));
            }
        }

        return;
    }

    let mut pre_eval_f: Option<PreEval> = None;

    // Collections used to generate the run log.
    let log_entries: Arc<Mutex<RunLog<NodePtr>>> = Arc::new(Mutex::new(RunLog {
        log_entries: RefCell::new(Vec::new()),
    }));
    #[allow(clippy::type_complexity)]
    let log_updates: Arc<Mutex<RunLog<(NodePtr, Option<NodePtr>)>>> =
        Arc::new(Mutex::new(RunLog {
            log_entries: RefCell::new(Vec::new()),
        }));

    // klvm_rs uses boxed callbacks with unspecified lifetimes so in order to
    // support logging as intended, we must have values that can be moved so
    // the callbacks can become immortal.  Our strategy is to use channels
    // and threads for this.
    let (pre_eval_req_out, pre_eval_req_in) = channel();
    let (pre_eval_resp_out, pre_eval_resp_in): (Sender<()>, Receiver<()>) = channel();

    let (post_eval_req_out, post_eval_req_in) = channel();
    let (post_eval_resp_out, post_eval_resp_in): (Sender<()>, Receiver<()>) = channel();

    let post_eval_fn: Rc<dyn Fn(NodePtr, Option<NodePtr>)> = Rc::new(move |at, n| {
        post_eval_req_out.send((at, n)).ok();
        post_eval_resp_in.recv().unwrap();
    });

    #[allow(clippy::type_complexity)]
    let pre_eval_fn: Rc<dyn Fn(&mut Allocator, NodePtr)> = Rc::new(move |_allocator, new_log| {
        pre_eval_req_out.send(new_log).ok();
        pre_eval_resp_in.recv().unwrap();
    });

    #[allow(clippy::type_complexity)]
    let closure: Rc<dyn Fn(NodePtr) -> Box<dyn Fn(Option<NodePtr>)>> = Rc::new(move |v| {
        let post_eval_fn_clone = post_eval_fn.clone();
        Box::new(move |n| {
            let post_eval_fn_clone_2 = post_eval_fn_clone.clone();
            (*post_eval_fn_clone_2)(v, n)
        })
    });

    if emit_symbol_output {
        #[allow(clippy::type_complexity)]
        let pre_eval_f_closure: Box<
            dyn Fn(
                &mut Allocator,
                NodePtr,
                NodePtr,
            ) -> Result<Option<Box<(dyn Fn(Option<NodePtr>))>>, EvalErr>,
        > = Box::new(move |allocator, sexp, args| {
            let pre_eval_clone = pre_eval_fn.clone();
            trace_pre_eval(
                allocator,
                &|allocator, n| (*pre_eval_clone)(allocator, n),
                symbol_table_clone.clone(),
                sexp,
                args,
            )
            .map(|t| {
                t.map(|log_ent| {
                    let closure_clone = closure.clone();
                    (*closure_clone)(log_ent)
                })
            })
        });

        pre_eval_f = Some(pre_eval_f_closure);
    }

    let run_script = match parsed_args.get("stage") {
        Some(ArgumentValue::ArgInt(0)) => stages::brun(&mut allocator),
        _ => stages::run(&mut allocator),
    };

    let cost_offset = calculate_cost_offset(&mut allocator, run_program.clone(), run_script);

    let max_cost = parsed_args
        .get("max_cost")
        .map(|x| match x {
            ArgumentValue::ArgInt(i) => *i - cost_offset,
            _ => 0,
        })
        .unwrap_or_else(|| 0);
    let max_cost = max(0, max_cost);

    if input_sexp.is_none() {
        input_sexp = sexp_from_stream(
            &mut allocator,
            &mut Stream::new(input_serialized),
            Box::new(SimpleCreateKLVMObject {}),
        )
        .map(|x| Some(x.1))
        .unwrap();
    };

    // Part 2 of doing pre_eval: Have a thing that receives the messages and
    // performs some action.
    let log_entries_clone = log_entries.clone();
    thread::spawn(move || {
        let pre_in = pre_eval_req_in;
        let pre_out = pre_eval_resp_out;

        while let Ok(received) = pre_in.recv() {
            {
                let locked = log_entries_clone.lock();
                locked.unwrap().push(received);
            }
            pre_out.send(()).ok();
        }
    });

    let log_updates_clone = log_updates.clone();
    thread::spawn(move || {
        let post_in = post_eval_req_in;
        let post_out = post_eval_resp_out;

        while let Ok(received) = post_in.recv() {
            {
                let locked = log_updates_clone.lock();
                locked.unwrap().push(received);
            }
            post_out.send(()).ok();
        }
    });

    let time_parse_input = SystemTime::now();
    let res = run_program
        .run_program(
            &mut allocator,
            run_script,
            input_sexp.unwrap(),
            Some(RunProgramOption {
                max_cost: if max_cost == 0 {
                    None
                } else {
                    Some(max_cost as u64)
                },
                pre_eval_f,
                strict: parsed_args
                    .get("strict")
                    .map(|_| true)
                    .unwrap_or_else(|| false),
            }),
        )
        .map(|run_program_result| {
            let mut cost: i64 = run_program_result.0 as i64;
            let result = run_program_result.1;
            let time_done = SystemTime::now();

            if parsed_args.get("cost").is_some() {
                if cost > 0 {
                    cost += cost_offset;
                }
                stdout.write_str(&format!("cost = {}\n", cost));
            };

            if let Some(ArgumentValue::ArgBool(true)) = parsed_args.get("time") {
                if parsed_args.get("hex").is_some() {
                    stdout.write_str(&format!(
                        "read_hex: {}\n",
                        time_read_hex
                            .duration_since(time_start)
                            .unwrap()
                            .as_millis()
                    ));
                } else {
                    stdout.write_str(&format!(
                        "assemble_from_ir: {}\n",
                        time_assemble
                            .duration_since(time_start)
                            .unwrap()
                            .as_millis()
                    ));
                    stdout.write_str(&format!(
                        "to_sexp_f: {}\n",
                        time_parse_input
                            .duration_since(time_assemble)
                            .unwrap()
                            .as_millis()
                    ));
                }

                stdout.write_str(&format!(
                    "run_program: {}\n",
                    time_done
                        .duration_since(time_parse_input)
                        .unwrap()
                        .as_millis()
                ));
            }

            let mut run_output = disassemble_with_kw(&mut allocator, result, keywords);
            if let Some(ArgumentValue::ArgBool(true)) = parsed_args.get("dump") {
                let mut f = Stream::new(None);
                sexp_to_stream(&mut allocator, result, &mut f);
                run_output = f.get_value().hex();
            } else if let Some(ArgumentValue::ArgBool(true)) = parsed_args.get("quiet") {
                run_output = "".to_string();
            };

            run_output
        });

    let output = collapse(res.map_err(|ex| {
        format!(
            "FAIL: {} {}",
            ex.1,
            disassemble_with_kw(&mut allocator, ex.0, keywords)
        )
    }));

    let compile_sym_out = dpr.get_compiles();
    if !compile_sym_out.is_empty() {
        write_sym_output(&compile_sym_out, &symbol_table_output).ok();
    }

    stdout.write_str(&format!("{}\n", output));

    // Third part of our scheme: now that we have results from the forward pass
    // and the pass doing the post callbacks, we can integrate them in the main
    // thread.  We didn't do this in the callbacks because we didn't want to
    // deal with a possibly escaping mutable allocator &.
    let mut log_content = log_entries.lock().unwrap().finish();
    let log_updates = log_updates.lock().unwrap().finish();
    fix_log(&mut allocator, &mut log_content, &log_updates);

    let only_exn = parsed_args
        .get("only_exn")
        .map(|_| true)
        .unwrap_or_else(|| false);

    if emit_symbol_output {
        stdout.write_str("\n");
        trace_to_text(
            &mut allocator,
            stdout,
            only_exn,
            &log_content,
            symbol_table.clone(),
            &disassemble,
        );
        if parsed_args.get("table").is_some() {
            trace_to_table(
                &mut allocator,
                stdout,
                only_exn,
                &log_content,
                symbol_table,
                &disassemble,
            );
        }
    }
}

/*
Copyright 2018 Chik Network Inc
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 */
