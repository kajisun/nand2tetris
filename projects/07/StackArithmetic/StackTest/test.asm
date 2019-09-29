"(" + self.mem_seg + ")\n" \
                    "@" + self.value +"\n"\
                    "D=A\n" +\
                    self.DintoSP +\
                    self.sp_plus +\
                    "@0\nD=A\n" + \
                    self.DintoSP + \
                    "(LCL_SET_START)\n" \
                    "@SP\nA=M\nD=M\n@LCL\nM=D+M\nA=M\nM=0\n" \
                    "@SP\nA=M\nM=M+1\nD=M\nA=A-1\nD=M-D\n" \
                    "@LCL_SET_START\nD;JNE\n" +\
                    self.sp_minus +\
                    "@" + self.value + "\n" \
                    "D=A\nD=D-1\n@LCL\nM=M-D\n"