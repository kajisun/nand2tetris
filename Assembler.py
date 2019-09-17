#read file
file_path= "projects/06/add/Add.asm"

with open(file_path) as f:
    lines = f.readlines()

#eliminate space, comments and break line(br)
preprocess = []

print(lines)

for line in lines:
    exist_comment = line.find("//")
    if exist_comment != -1:
        line = line[0:exist_comment]
    if line.rstrip() != "":
        preprocess.append(line.rstrip().replace(" ", ""))

print(preprocess)

#parser
