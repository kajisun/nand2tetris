file = r"C:\Users\papap\atelier\nand2tetris\projects\06\pong\Pong.hack"
compare = r"C:\Users\papap\atelier\nand2tetris\projects\06\Pong.hack"

binary_file = []
compare_file = []

with open(file) as f:
    for i in f:
        binary_file.append(i)

with open(compare) as f:
    for i in f:
        compare_file.append(i)
for i in range(len(binary_file)):
    if binary_file[i] != compare_file[i]:
        print(i)

