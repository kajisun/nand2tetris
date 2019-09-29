class VMconverter:
    def __init__(self, command_set, file_symbol):
        self.command_set = command_set
        self.file_symbol = file_symbol
        self.mem_seg_table = {
            "argument": "ARG",
            "local": "LCL",
            "this": "THIS",
            "that": "THAT",

        }
        self.operator = self.command_set.group(1)
        self.mem_seg = self.command_set.group(2)
        self.value = self.command_set.group(3)
        self.fill_D_M = "@SP\nA=M-1\nD=M\nA=A-1\n"
        self.DintoSP = "@SP\nA=M\nM=D\n"
        self.sp_plus = "@SP\nM=M+1\n"
        self.sp_minus = "@SP\nM=M-1\n"


    def C_PUSH(self):
        if self.mem_seg == "constant":
            asm_codes = "@" + self.value + "\n" \
                        "D=A\n" +\
                        self.DintoSP +\
                        self.sp_plus
            return asm_codes

        elif self.mem_seg in self.mem_seg_table:
            asm_codes = "@" + self.value + "\n" \
                        "D=A\n" \
                        "@" + self.mem_seg_table[self.mem_seg] + "\n" + \
                        "A=D+M\n"\
                        "D=M\n" +\
                        self.DintoSP +\
                        self.sp_plus
            return asm_codes

        elif self.mem_seg == "temp":
            asm_codes = "@" + str(5 + int(self.value)) + "\n"\
                        "D=M\n" +\
                        self.DintoSP +\
                        self.sp_plus
            return asm_codes

        elif self.mem_seg == "static":
            asm_codes = "@" + self.file_symbol +".STATIC" + self.value + "\n"\
                        "D=M\n" +\
                        self.DintoSP +\
                        self.sp_plus
            return asm_codes
        elif self.mem_seg == "pointer":
            if int(self.value):
                which = "THAT\n"
            else:
                which = "THIS\n"
            asm_codes = "@" + which +\
                        "D=M\n" + \
                        self.DintoSP + self.sp_plus
            return asm_codes

    def C_POP(self):
        if self.mem_seg in self.mem_seg_table:
            asm_codes = "@" + self.value + "\n" + \
                        "D=A\n" + \
                        "@" + self.mem_seg_table[self.mem_seg] + "\n" + \
                        "M=D+M\n" +\
                        self.sp_minus +\
                        "A=M\n" \
                        "D=M\n" + \
                        "@" + self.mem_seg_table[self.mem_seg] + "\n" + \
                        "A=M\n" \
                        "M=D\n" \
                        "@" + self.value + "\n" + \
                        "D=A\n" + \
                        "@" + self.mem_seg_table[self.mem_seg] + "\n" + \
                        "M=M-D\n"
            return asm_codes

        elif self.mem_seg == "temp":
            asm_codes = self.sp_minus +\
                        "A=M\n" \
                        "D=M\n" + \
                        "@" + str(5 + int(self.value)) + "\n" \
                        "M=D\n"
            return asm_codes

        elif self.mem_seg == "static":
            asm_codes = self.sp_minus +\
                        "A=M\n" \
                        "D=M\n" +\
                        "@" + self.file_symbol + ".STATIC" + self.value + "\n"\
                        "M=D\n"
            return asm_codes

        elif self.mem_seg == "pointer":
            if int(self.value):
                which = "THAT\n"
            else:
                which = "THIS\n"
            asm_codes = self.sp_minus +\
                        "A=M\n" \
                        "D=M\n" \
                        "@" + which +\
                        "M=D\n"
            return asm_codes

    def C_ARITHMETIC(self, logic_counter):
        self.operator = self.command_set.group(1)
        asm_codes = ""

        group_1 = {
            "add": "M=D+M\n",
            "sub": "M=M-D\n",
            "and": "M=D&M\n",
            "or" : "M=D|M\n",

        }
        group_2 = {
            "eq": "JEQ\n",
            "lt": "JLT\n",
            "gt": "JGT\n",

        }
        group_3 = {
            "neg": "M=-M\n",
            "not": "M=!M\n",
        }

        if self.operator in group_1:
            asm_codes = self.fill_D_M + \
                        group_1[self.operator] + \
                        self.sp_minus

        elif self.operator in group_2:
            asm_codes = self.fill_D_M +\
                        "D=M-D\n" + \
                        self.sp_minus * 2 +\
                        "@" + self.file_symbol + ".LOGIC" + str(logic_counter) + "\n" +\
                        "D;" + group_2[self.operator] + \
                        "@SP\n" \
                        "A=M\n" \
                        "M=0\n" \
                        "@" + self.file_symbol + ".END" + str(logic_counter) +"\n"\
                        "0;JMP\n" \
                        "(" + self.file_symbol + ".LOGIC" + str(logic_counter) + ")\n" \
                        "@SP\n" \
                        "A=M\n" \
                        "M=-1\n" \
                        "(" + self.file_symbol + ".END" + str(logic_counter) + ")\n" + \
                        self.sp_plus

        elif self.operator in group_3:
            asm_codes = "@SP\n" \
                        "A=M-1\n" +\
                        group_3[self.operator]

        return asm_codes

    def C_LABEL(self, func_name):
        asm_codes = "(" + func_name +self.file_symbol + "." + self.mem_seg + ")\n"
        return asm_codes

    def C_IF(self, func_name):
        asm_codes = self.sp_minus + \
                    "@SP\n" \
                    "A=M\n" \
                    "D=M\n" +\
                    "@" + func_name + self.file_symbol + "." + self.mem_seg + "\n"\
                    "D;JNE\n"
        return asm_codes

    def C_GOTO(self, fun_name):
        asm_codes = "@" + fun_name +self.file_symbol + "." + self.mem_seg +"\n"\
                    "0;JMP\n"
        return asm_codes

    def C_FUNCTION(self, logic_counter, func_name):
        asm_codes = "("+ self.mem_seg + ")\n" \
                    "@" + self.value + "\n" \
                    "D=A\n" \
                    "(" + func_name +"LCLs_SET_START" + str(logic_counter) + ")\n" \
                    "@" + func_name +"LCLs_SET_END" + str(logic_counter) + "\n" \
                    "D;JEQ\n" \
                    "@LCL\n" \
                    "A=D+M\n" \
                    "A=A-1\n" \
                    "M=0\n" \
                    "D=D-1\n" \
                    "@"+ func_name +"LCLs_SET_START" + str(logic_counter) + "\n" \
                    "0;JMP\n" \
                    "(" + func_name + "LCLs_SET_END" + str(logic_counter) + ")\n" \
                    "@" +self.value + "\nD=A\n" \
                    "@SP\nM=D+M\n"
        return asm_codes

    def C_RETURN(self):
        asm_codes = "@FRAME\nM=0\n" \
                    "@LCL\nD=M\n" \
                    "@FRAME\nM=D\n" \
                    "@RET\nM=0\n" \
                    "@FRAME\nA=M\n" + "A=A-1\n" * 5 + "D=M\n" \
                    "@RET\nM=D\n" \
                    "@SP\nA=M-1\nD=M\n" \
                    "@ARG\nA=M\nM=D\nA=A+1\nD=A\n" \
                    "@SP\nM=D\n" \
                    "@FRAME\nA=M\n" + "A=A-1\n" * 1 + "D=M\n" \
                    "@THAT\nM=D\n" \
                    "@FRAME\nA=M\n" + "A=A-1\n" * 2 + "D=M\n" \
                    "@THIS\nM=D\n" \
                    "@FRAME\nA=M\n" + "A=A-1\n" * 3 + "D=M\n" \
                    "@ARG\nM=D\n" \
                    "@FRAME\nA=M\n" + "A=A-1\n" * 4 + "D=M\n" \
                    "@LCL\nM=D\n" \
                    "@RET\nA=M\n" \
                    "0;JMP\n"
        return asm_codes

    def C_CALL(self,logic_counter):
        asm_codes = "@RETURN_ADDRESS" + str(logic_counter) + "\nD=A\n" \
                    "@SP\nA=M\nM=D\n" +\
                    self.sp_plus +\
                    "@LCL\nD=M\n" \
                    "@SP\nA=M\nM=D\n" +\
                    self.sp_plus +\
                    "@ARG\nD=M\n" \
                    "@SP\nA=M\nM=D\n" +\
                    self.sp_plus + \
                    "@THIS\nD=M\n" \
                    "@SP\nA=M\nM=D\n" + \
                    self.sp_plus + \
                    "@THAT\nD=M\n" \
                    "@SP\nA=M\nM=D\n" + \
                    self.sp_plus + \
                    "@SP\nD=M\n" \
                    "@" + str(int(self.value) + 5) + "\n" \
                    "D=D-A\n" \
                    "@ARG\nM=D\n" \
                    "@SP\nD=M\n" \
                    "@LCL\nM=D\n" \
                    "@" + self.mem_seg +"\n" \
                    "0;JMP\n" \
                    "(RETURN_ADDRESS" + str(logic_counter) + ")\n"
        return asm_codes