import re
import argparse
import os.path

A_COMMAND = re.compile(r'@([0-9a-zA-Z_\.\$:]+)')
L_COMMAND = re.compile(r'\(([0-9a-zA-Z_\.\$:]*)\)')
C_COMMAND = re.compile(r'(?:(A?M?D?)=)?([-+&|!AMD01]+)(?:;(.+))?')
ignore_pattern = re.compile(r'(?://.*| )')

pattren_table = {
    "A_COMMAND": A_COMMAND,
    "L_COMMAND": L_COMMAND,
    "C_COMMAND": C_COMMAND,
}

class Parser:
    stream = None
    command_type = None
    current_line = None

    def __init__(self, stream):
        self.stream = stream
        self.pattern_table = {}
        self.ignore_pattern = {}

    def add_pattern(self, pattern_table):
        for type, pattern in pattern_table.items():
            self.pattern_table[type] = pattern

    def hasMoreCommands(self):
        return self.current_line != ""

    def advance(self):
        for pattern in self.ignore_pattern.values():
            self.current_line = pattern.sub("", self.stream.readline())
            return self.current_line

    def commandType(self):
        for type, pattern in self.pattern_table.items():
            self.command_type = pattern.match(self.current_line)
            if self.command_type is not None:
                return type

    # functions for this assembler
    # use A or L command
    def symbol(self):
        return self.command_type.group(1)

    # use C command
    def dest(self):
        return self.command_type.group(1)

    def comp(self):
        return self.command_type.group(2)

    def jump(self):
        return self.command_type.group(3)


class SymbolTable:
    def __init__(self):
        self.symbol_address = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        for i in range(16):
            self.symbol_address["R" + str(i)] = i

    def addEntry(self, symbol, address):
        self.symbol_address[symbol] = address

    def contains(self, symbol):
        return symbol in self.symbol_address

    def getAddress(self, symbol):
        return self.symbol_address[symbol]


def C_converter(dest, comp, jump):
    # destination
    if dest is None:
        dest = ""
    dest_pattern = ["0", "0", "0"]
    if "A" in dest:
        dest_pattern[0] = "1"
    if "D" in dest:
        dest_pattern[1] = "1"
    if "M" in dest:
        dest_pattern[2] = "1"

    dest_code = ""
    for i in dest_pattern:
        dest_code += i

    # jump
    jump_table = {
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }
    if jump is None:
        jump_code = "000"
    else:
        jump_code = jump_table[jump]

    # compute
    comp_table = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "M": "1110000",
        "!D": "0001101",
        "!A": "0110001",
        "!M": "1110001",
        "-D": "0001111",
        "-A": "0110011",
        "-M": "1110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "M+1": "1110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "M-1": "1110010",
        "D+A": "0000010",
        "D+M": "1000010",
        "D-A": "0010011",
        "D-M": "1010011",
        "A-D": "0000111",
        "M-D": "1000111",
        "D&A": "0000000",
        "D&M": "1000000",
        "D|A": "0010101",
        "D|M": "1010101",
    }
    if comp is not None:
        comp_code = comp_table[comp]

    else:
        assert False, "comp is invalid"

    C_code = "111" + comp_code + dest_code + jump_code

    return C_code

def A_converter(line):
    line = int(line.replace("@", ""))
    return str(format(line, "016b"))

def main():
    #read file
    terminal_arg = argparse.ArgumentParser()
    terminal_arg.add_argument("asm_file", type=str, help="asm_file")
    args = terminal_arg.parse_args()
    file_path = args.asm_file

    output_file = os.path.splitext(file_path)[0] + ".hack"

    #create new blank file
    with open(output_file, "w") as init:
        init.write("")

    #first path
    with open(file_path) as stream:
        paser = Parser(stream)
        paser.add_pattern(pattren_table)
        paser.ignore_pattern["ignore"] = ignore_pattern
        st = SymbolTable()
        address = 0

        while True:
            line = paser.advance()
            if paser.hasMoreCommands() != True:
                break

            command_type = paser.commandType()
            if command_type is None:
                continue

            if command_type == "L_COMMAND":
                st.addEntry(paser.symbol(), address)

            if command_type == "A_COMMAND" or command_type == "C_COMMAND":
                address = address + 1

    #second path
    with open(file_path) as stream:
        paser = Parser(stream)
        paser.add_pattern(pattren_table)
        paser.ignore_pattern["ignore"] = ignore_pattern
        variable_address = 16
        binary = ""

        while True:
            line = paser.advance()
            command_type = paser.commandType()
            if paser.hasMoreCommands() != True:
                break

            if command_type is None:
                continue

            if command_type == "L_COMMAND":
                continue

            if command_type == "C_COMMAND":
                dest = paser.dest()
                comp = paser.comp()
                jump = paser.jump()
                binary = C_converter(dest, comp, jump)

            if command_type == "A_COMMAND":
                symbol = paser.symbol()
                if symbol.isdigit():
                    binary = A_converter(line)
                elif st.contains(symbol):
                    line_L = "@" + str(st.getAddress(symbol))
                    binary = A_converter(line_L)
                else:
                    st.addEntry(symbol, variable_address)
                    line_L = "@" + str(st.getAddress(symbol))
                    binary = A_converter(line_L)
                    variable_address += 1

            with open(output_file, "a") as f_write:
                f_write.write(binary + "\n")

if __name__ == "__main__":
    main()
