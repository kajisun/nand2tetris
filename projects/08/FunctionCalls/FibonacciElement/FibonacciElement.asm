@256
D=A
@SP
M=D
@RETURN_ADDRESS0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RETURN_ADDRESS0)
(Main.fibonacci)
@0
D=A
(Main.fibonacci$LCLs_SET_START1)
@Main.fibonacci$LCLs_SET_END1
D;JEQ
@LCL
A=D+M
A=A-1
M=0
D=D-1
@Main.fibonacci$LCLs_SET_START1
0;JMP
(Main.fibonacci$LCLs_SET_END1)
@0
D=A
@SP
M=D+M
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@SP
M=M-1
@SP
M=M-1
@Main.LOGIC2
D;JLT
@SP
A=M
M=0
@Main.END2
0;JMP
(Main.LOGIC2)
@SP
A=M
M=-1
(Main.END2)
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@Main.fibonacci$Main.IF_TRUE
D;JNE
@Main.fibonacci$Main.IF_FALSE
0;JMP
(Main.fibonacci$Main.IF_TRUE)
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@FRAME
M=0
@LCL
D=M
@FRAME
M=D
@RET
M=0
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@RET
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
A=A+1
D=A
@SP
M=D
@FRAME
A=M
A=A-1
D=M
@THAT
M=D
@FRAME
A=M
A=A-1
A=A-1
D=M
@THIS
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
D=M
@ARG
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@RET
A=M
0;JMP
(Main.fibonacci$Main.IF_FALSE)
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@RETURN_ADDRESS3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_ADDRESS3)
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@RETURN_ADDRESS4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_ADDRESS4)
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
@FRAME
M=0
@LCL
D=M
@FRAME
M=D
@RET
M=0
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@RET
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
A=A+1
D=A
@SP
M=D
@FRAME
A=M
A=A-1
D=M
@THAT
M=D
@FRAME
A=M
A=A-1
A=A-1
D=M
@THIS
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
D=M
@ARG
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@RET
A=M
0;JMP
(Sys.init)
@0
D=A
(Sys.init$LCLs_SET_START5)
@Sys.init$LCLs_SET_END5
D;JEQ
@LCL
A=D+M
A=A-1
M=0
D=D-1
@Sys.init$LCLs_SET_START5
0;JMP
(Sys.init$LCLs_SET_END5)
@0
D=A
@SP
M=D+M
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@RETURN_ADDRESS6
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_ADDRESS6)
(Sys.init$Sys.WHILE)
@Sys.init$Sys.WHILE
0;JMP