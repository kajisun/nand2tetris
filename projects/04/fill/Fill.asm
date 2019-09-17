// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@WAIT
(WAIT)
  @i
  M=0
  @KBD
  D=M
  @NEG
  D;JLE
  @POS
  D;JGT

  (POS)
    @i
    D=M
    @SCREEN
    A=A+D
    M=-1
    @8191
    D=D-A
    @PEND
    D;JEQ
    @i
    M=M+1
    @POS
    0;JMP
      (PEND)
        @WAIT
        0;JMP

    (NEG)
      @i
      D=M
      @SCREEN
      A=A+D
      M=0
      @8191
      D=D-A
      @NEND
      D;JEQ
      @i
      M=M+1
      @NEG
      0;JMP
        (NEND)
          @WAIT
          0;JMP
