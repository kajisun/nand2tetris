import argparse
import re
import os.path

#file_path = r"C:\Users\papap\atelier\nand2tetris\projects\07\StackArithmetic\SimpleAdd\SimpleAdd.vm"
#output_file_name = "SimpleAdd.asm"

"""
class Parser(object):
    def __init__(self):
        self.current_command = None
        self.open_file = open(file_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.open_file.close()

    def hasMoreCommands(self):
        self.open_file.readline()
"""
"""
def hasMoreCommands(iter):
    return True if next(iter) else False
"""
"""first idea
with open(file_path) as f:
    while True:
        try:
            current_item = next(f)
            print(current_item)
        except StopIteration:
            break
"""
def memory_segments():
    memory_segments = {
        "argument": "ARG",
        "local": "LCL",
        "this": "THIS",
        "that": "THAT",
    }
    return memory_segments

def trimming(line):
    line = line.strip()
    exist_comment = line.find("//")
    if exist_comment != -1:
        line = line[:exist_comment]
    return line

def sepalate_command(line):
    command_pattern = re.compile(r"([a-z]+)(?: )?([a-z]+)?(?: )?([0-9]+)?")
    match = command_pattern.match(line)
    if match:
        return match


def C_PUSH(commands):
    mem_seg_table = memory_segments()
    mem_seg = commands.group(2)
    value = commands.group(3)
    if mem_seg == "constant":
        asm_codes = "@" + str(value) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        return asm_codes
"""
    @10
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
"""

def C_POP(commands):
    mem_seg_table = memory_segments()
    mem_seg = commands.group(2)
    value = commands.group(3)
    asm_codes = "@" + value +"\n" + \
                "D=A\n" + \
                "@" + mem_seg_table[mem_seg] + "\n" + \
                "M=D+M\n@SP\nM=M-1\nA=M\nD=M\n"+ \
                "@" + mem_seg_table[mem_seg] + "\n" + \
                "A=M\nM=D\n"
    return asm_codes

"""
@0
D=A
@LCL
M=D+M
@SP
M=M-1
A=M
D=M
@LCL
A=M
M=D

"""

def Add():
    asm_codes = "@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=D+M\n@SP\nM=M-1\n"
    return asm_codes
"""
@SP
A=M
A=A-1
D=M
A=A-1
M=D+M
@SP
M=M-1
"""

def arithmetic_table():
    arithmetics = {"add": Add(),
                   #"sub": Sub(),
                   #"neg": Neg(),
                   #"eq" : Eq(),
                   #"gt" : Gt(),
                   #"lt" : Lt(),
                   #"and": And(),
                   #"or" : Or(),
                   #"not": Not(),
                   }

    return arithmetics

def command_type(commands):
    arith_table = arithmetic_table()
    cmd = commands.group(1)
    if cmd == "push":
        return C_PUSH(commands)
    elif cmd == "pop":
        return C_POP(commands)
    elif cmd in arith_table.keys():
        return arith_table[cmd]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vm_file", type=str, help="vm_file")
    args = parser.parse_args()
    vm_file = args.vm_file

    output_file = os.path.splitext(vm_file)[0] + ".asm"

    with open(output_file, "w") as init:
        init.write("")

    with open(vm_file) as f_read:
        for line in f_read:
            trimmed = trimming(line)
            if trimmed != "":
                commands = sepalate_command(trimmed)
                asm_codes = command_type(commands)
                with open(output_file, "a") as f_write:
                    f_write.write(asm_codes)


#execution
"""
line = "add"
cmds= sepalate_command(line)
print(command_type(cmds))
"""

#if __name__ == "__main__":
#    main()