
class FunctionHeaderPiece:
    def __init__(self, string):
        self.prep = None
        self.literal = None
        self.type = None
        self.name = None


        if ':' in string:
            self.prep, string = string.split(':')
        
        if string.endswith('"'):
            self.literal = string.strip('"')

        elif string[0] == '(' and string[-1] == ')':
            self.type, self.name = (string
                .removeprefix('(')
                .removesuffix(')')
                .split()
            )
        else:
            self.type = string
    
    def __str__(self):
        r = []
        if self.prep:
            r.append(f'prep={self.prep}')
        if self.literal:
            r.append(f'literal={self.literal}')
        if self.type:
            r.append(f'type={self.type}')
        if self.name:
            r.append(f'name={self.name}')
        return '<'+', '.join(r)+'>'


def parse_function_header(header):
    assert header.strip().endswith(' >>')
    parts = header.strip().removesuffix(' >>').split()

    # join together parens
    kept = []
    off = False
    for prev, part in zip(parts, parts[1:]+['']):
        if '(' in prev and ')' in part:
            off = True
            kept.append(prev+' '+part)
        elif off:
            off = False
        else:
            kept.append(prev)

    print()
    for part in kept:
        print(FunctionHeaderPiece(part))

# parse_function_header('int "multiple" of:int >>')
# parse_function_header('(int a) "multiple" of:(int b) >>')
# parse_function_header('int is:"prime" >>')
# parse_function_header('"fizzbuzz" list.int >>')


def dispatch_line(string):
    state = 'FLAT'

    if string.strip().endswith('>>'):
        return parse_function_header(string)


