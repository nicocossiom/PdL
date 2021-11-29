class Position:
    def __init__(self, index: int , lineNumber :int, colNumber:int, filename: str, ftxt):
            self.index = idx
            self.lineNumber = ln
            self.colNumber = col
            self.fn = fn
            self.ftxt = ftxt

    def advance(self, current_char=None):
            self.index += 1
            self.colNumber += 1
            if current_char == '\n':
                    self.ln += 1
                    self.col = 0
            return self

    def copy(self):
            return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Error:
    def __init__(self, pos_start : Position, pos_end: Positon, error_name: str, details: str):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def string_with_arrows(text, pos_start, pos_end):
        result = ''
        # Calculate indices
        idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)
        # Generate each line
        line_count = pos_end.ln - pos_start.ln + 1
        for i in range(line_count):
            # Calculate line columns
            line = text[idx_start:idx_end]
            col_start = pos_start.col if i == 0 else 0
            col_end = pos_end.col if i == line_count - 1 else len(line) - 1
            # Append to result
            result += line + '\n'
            result += ' ' * col_start + '^' * (col_end - col_start)
            # Re-calculate indices
            idx_start = idx_end
            idx_end = text.find('\n', idx_start + 1)
            if idx_end < 0: idx_end = len(text)
        return result.replace('\t', '')
    
    def __str__(self):
        '''Pritns'''
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
        
class lexicalError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

