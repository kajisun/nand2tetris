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

