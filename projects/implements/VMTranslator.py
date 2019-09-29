#standard library
import argparse
import re
import os.path
import sys
import glob

#import projects.implements.module.parser as VMparser
import module.parser as VMparser
#import projects.implements.module.VMconverter as VMconv
import module.VMconverter as VMconv

command_pattern =  re.compile(r"([-a-z]+) ?([a-zA-Z0-9_\.:]+)? ?([0-9]+)?")
pattern_table = {"command" : command_pattern}
ignore_pattern = re.compile(r'(?://.*)')

file_pattern = re.compile(r"(.*\\)*(.*|.*\.vm$)?")


def main():
    terminal_arg = argparse.ArgumentParser()
    terminal_arg.add_argument("vm_file", type=str, help="vm_file")
    args = terminal_arg.parse_args()
    vm_file = args.vm_file

    output_file = os.path.splitext(vm_file)[0] + ".asm"

    with open(output_file, "w") as init:
        init.write("")

    with open(vm_file) as stream:
        parser = VMparser.Parser(stream)
        parser.add_pattern(pattern_table)
        parser.ignore_pattern["ignore"] = ignore_pattern
        logic_counter = 0

        while True:
            line = parser.advance()

            if parser.hasMoreCommands() != True:
                break

            current_type = parser.commandType()
            if current_type is None:
                continue
            else:
                command_set = parser.pattern_table[current_type].match(line)

            converter = VMconv.VMconverter(command_set)
            operator = converter.command_set.group(1)

            if operator == "push":
                asm_codes = converter.C_PUSH()
            elif operator == "pop":
                asm_codes = converter.C_POP()
            elif operator in ["add", "sub", "neg", "and", "or", "not", ]:
                asm_codes = converter.C_ARITHMETIC(logic_counter)
            elif operator in ["eq", "lt", "gt"]:
                asm_codes = converter.C_ARITHMETIC(logic_counter)
                logic_counter += 1
            elif operator == "label":
                asm_codes = converter.C_LABEL()
            elif operator == "goto":
                asm_codes = converter.C_GOTO()
            elif operator == "if-goto":
                asm_codes = converter.C_IF()
            elif operator == "function":
                asm_codes = converter.C_FUNCTION()
            elif operator == "return":
                asm_codes = converter.C_RETURN()

            with open(output_file, "a") as f_write:
                f_write.write(asm_codes)

def args():
    get_arg = sys.argv[1]
    match = file_pattern.match(get_arg)
    vm_files = []
    logic_counter = 0
    bootstrap = ""
    if ".vm" in get_arg:
        vm_files.append(match.group(0))
        output_file = os.path.splitext(vm_files[0])[0] + ".asm"
    else:
        get_path = match.group(0)
        vm_files = glob.glob(get_path + "\\*.vm")
        output_file =match.group(0) + "\\" + match.group(2) + ".asm"
        bootstrap = "@256\nD=A\n@SP\nM=D\n" \
                    "@RETURN_ADDRESS" + str(logic_counter) + "\nD=A\n" \
                    "@SP\nA=M\nM=D\n@SP\nM=M+1\n" \
                    "@LCL\nD=M\n" \
                    "@SP\nA=M\nM=D\n@SP\nM=M+1\n" \
                    "@ARG\nD=M\n" \
                    "@SP\nA=M\nM=D\n@SP\nM=M+1\n" \
                    "@THIS\nD=M\n" \
                    "@SP\nA=M\nM=D\n@SP\nM=M+1\n" \
                    "@THAT\nD=M\n" \
                    "@SP\nA=M\nM=D\n@SP\nM=M+1\n" \
                    "@SP\nD=M\n@5\nD=D-A\n" \
                    "@ARG\nM=D\n" \
                    "@SP\nD=M\n" \
                    "@LCL\nM=D\n" \
                    "@Sys.init\n" \
                    "0;JMP\n" \
                    "(RETURN_ADDRESS" + str(logic_counter) + ")\n"
        logic_counter += 1


    with open(output_file, "w") as init:
        init.write(bootstrap)

    for vm_file in vm_files:
        func_names = ["", ]
        file_symbol = file_pattern.match(vm_file).group(2).replace(".vm", "")
        with open(vm_file) as stream:
            parser = VMparser.Parser(stream)
            parser.add_pattern(pattern_table)
            parser.ignore_pattern["ignore"] = ignore_pattern

            while True:
                line = parser.advance()

                if parser.hasMoreCommands() != True:
                    break

                current_type = parser.commandType()
                if current_type is None:
                    continue
                else:
                    command_set = parser.pattern_table[current_type].match(line)

                converter = VMconv.VMconverter(command_set, file_symbol)
                operator = converter.command_set.group(1)

                if operator == "push":
                    asm_codes = converter.C_PUSH()
                elif operator == "pop":
                    asm_codes = converter.C_POP()
                elif operator in ["add", "sub", "neg", "and", "or", "not", ]:
                    asm_codes = converter.C_ARITHMETIC(logic_counter)
                elif operator in ["eq", "lt", "gt"]:
                    asm_codes = converter.C_ARITHMETIC(logic_counter)
                    logic_counter += 1
                elif operator == "label":
                    asm_codes = converter.C_LABEL(func_names[-1])
                elif operator == "goto":
                    asm_codes = converter.C_GOTO(func_names[-1])
                elif operator == "if-goto":
                    asm_codes = converter.C_IF(func_names[-1])
                elif operator == "function":
                    func_names.append(converter.command_set.group(2) + "$")
                    asm_codes = converter.C_FUNCTION(logic_counter, func_names[-1])
                    logic_counter += 1
                elif operator == "return":
                    asm_codes = converter.C_RETURN()
                elif operator == "call":
                    asm_codes = converter.C_CALL(logic_counter)
                    logic_counter += 1

                with open(output_file, "a") as f_write:
                    f_write.write(asm_codes)

if __name__ == "__main__":
    args()
