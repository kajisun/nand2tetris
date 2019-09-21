import re

A_COMMAND_PATTERN = re.compile(r'@([0-9a-zA-Z_\.\$:]+)')
L_COMMAND_PATTERN = re.compile(r'\(([0-9a-zA-Z_\.\$:]*)\)')
C_COMMAND_PATTERN = re.compile(r'(?:(A?M?D?)=)?([^;]+)(?:;(.+))?')

"""class HackPaser():

    def __init__(self, file_path):
        self.f_read = open(file_path)

    def __enter__(self):
"""

line = "(END_EQ)"
m = L_COMMAND_PATTERN.match(line)
print(m.group(1))

