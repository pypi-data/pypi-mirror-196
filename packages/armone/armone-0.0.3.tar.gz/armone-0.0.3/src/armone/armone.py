import random
import argparse
import io
import tokenize

CHARLIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 
'v', 'w', 'x', 'y', 'z', '!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']
VA2SY = dict(enumerate(CHARLIST))
SY2VA = dict(map(reversed, VA2SY.items()))

def remove_comments_and_docstrings(source):
    
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0

    for tok in tokenize.generate_tokens(io_obj.readline):

        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]

        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line

    return out

def encode(string, base):

    integer = int.from_bytes(string.encode("utf-8"), byteorder = "big")
    array = []

    while integer:
        integer, value = divmod(integer, base)
        array.append(VA2SY[value])

    return ''.join(reversed(array))
    
def decode(string, base):

    integer = 0

    for character in string:
        value = SY2VA[character]
        integer *= base
        integer += value

    return integer.to_bytes(((integer.bit_length() + 7) // 8), byteorder = "big").decode("utf-8")

def prepare_code(code):

    code = remove_comments_and_docstrings(code)
    return code

def main():

    parser = argparse.ArgumentParser(description = "A command line tool to obfuscate python scripts!")

    parser.add_argument("input", type = str, nargs = 1,
                    metavar = "input_file_path", default = None,
                    help = "The path to the file that is to be obfuscated")
    parser.add_argument("-o", "--output", type = str, nargs = 1,
                    metavar = "output_file_path", default = ["obfuscated.py"],
                    help = "The path to the file that is to be obfuscated")

    args = parser.parse_args()
    
    with open(args.input[0], 'r') as read_obj:
        code = prepare_code(read_obj.read())

    for _ in range(random.randint(1, 32)):

        base = random.randint(1, 90)
        encoded = encode(code, base)
        code = f"import armone\neval(compile(armone.decode(r'{encoded}', {base}), '<string>', 'exec'))"

    with open(args.output[0], "w") as write_obj:
        write_obj.write(code)