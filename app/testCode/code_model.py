class Code:
    def __innit__(self, language, code, input, output, expected_output):
        self.language = language
        self.code = code
        self.input = input
        self.output = output
        self.expected_output = expected_output
