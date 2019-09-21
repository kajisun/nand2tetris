#file_path = "projects/06/max/Max.asm"
#file_path = "projects/06/rect/Rect.asm"
file_path = "projects/06/pong/Pong.asm"
#make_file_name = "Max.hack"
#make_file_name = "Rect.hack"
make_file_name = "Pong.hack"

def preprocess(file_path):
    with open(file_path) as f:
        lines = f.readlines()

    #eliminate space, comments and break line(br)
    preprocess = []
    for line in lines:
        exist_comment = line.find("//")
        if exist_comment != -1:
            line = line[0:exist_comment]
        if line.rstrip() != "":
            preprocess.append(line.rstrip().replace(" ", ""))

    return preprocess

def C_command(line):

    #destination
    dest=""
    eq_ind = line.find("=")
    if eq_ind != -1:
        dest = line[0:eq_ind + 1]

    dest_list = ["0", "0", "0"]
    if "A" in dest:
        dest_list[0] = "1"
    if "D" in dest:
        dest_list[1] = "1"
    if "M" in dest:
        dest_list[2] = "1"

    dest_result =""
    for i in dest_list:
        dest_result += i

    #jump
    jump = ""
    jump_codes = {
        "JGT":"001",
        "JEQ":"010",
        "JGE":"011",
        "JLT":"100",
        "JNE":"101",
        "JLE":"110",
        "JMP":"111",
    }
    jump_result = "000"
    semco_ind = line.find(";")
    if semco_ind != -1:
        jump = line[semco_ind:]
    if jump[1:] in jump_codes.keys():
        jump_result = jump_codes[jump[1:]]

    #compute
    comp =line.replace(dest, "").replace(jump, "")
    comp_list = {
        "0":"0101010",
        "1":"0111111",
        "-1":"0111010",
        "D":"0001100",
        "A":"0110000",
        "M":"1110000",
        "!D":"0001101",
        "!A":"0110001",
        "!M":"1110001",
        "-D":"0001111",
        "-A":"0110011",
        "-M":"1110011",
        "D+1":"0011111",
        "A+1":"0110111",
        "M+1":"1110111",
        "D-1":"0001110",
        "A-1":"0110010",
        "M-1":"1110010",
        "D+A":"0000010",
        "D+M":"1000010",
        "D-A":"0010011",
        "D-M":"1010011",
        "A-D":"0000111",
        "M-D":"1000111",
        "D&A":"0000000",
        "D&M":"1000000",
        "D|A":"0010101",
        "D|M":"1010101",
    }
    if comp in comp_list.keys():
        comp_result = comp_list[comp]
    else:
        print("comp command is invalid.")

    C_instruction = "111" + comp_result + dest_result + jump_result

    return C_instruction

def A_command(line):
    line = int(line.replace("@", ""))
    return str(format(line, "016b"))

def symbol_init():
    symbol_table = {
        "SP":"0",
        "LCL":"1",
        "ARG":"2",
        "THIS":"3",
        "THAT":"4",
        "SCREEN":"16384",
        "KBD":"24576",
    }
    for i in range(16):
        symbol_table["R"+str(i)] = str(i)
    return symbol_table

def convert_L(file_path):
    lines = preprocess(file_path)
    symbol_table = symbol_init()

    #first_path
    counter = 0
    for line in lines[:]:
        if line[0] != "(":
            counter += 1
        else:
            label = line.replace("(", "").replace(")", "")
            duplicated = label not in symbol_table.keys()
            assert duplicated, "the label is duplicated"
            if duplicated:
                symbol_table[label] = str(counter)
                lines.remove(line)

    #second_path
    lines_L = []
    counter = 16
    for line in lines:
        if line[0] == "@":
            value = line.replace("@", "")
            if not value.isdigit():
                duplicated = value in symbol_table.keys()
                if not duplicated:
                    symbol_table[value] = str(counter)
                    counter += 1
                lines_L.append(line[0] + symbol_table[value])
            else:
                lines_L.append(line)
        else:
            lines_L.append(line)
    return lines_L

def judge_type(line):
    if "@" in line:
        return A_command(line)
    else:
        return C_command(line)

def assembler(file_path, make_file_name):
    lines = convert_L(file_path)
    binary = []
    for line in lines:
        binary.append(judge_type(line))

    with open(make_file_name,"w") as f:
        f.write("\n".join(binary))

assembler(file_path, make_file_name)
