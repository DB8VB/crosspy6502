import os

# Tokenize: Each line becomes a list containing the first element 
# (i.e. compiler directive, label or command) and the rest of the line
def tokenize(fp):
    tokens = []

    def process_file(fp): # Process the file
        fp.seek(0)
        lines = fp.readlines()

        for line in lines:
            line = line.split(';', 1)[0].strip()  # Remove comments and strip whitespace
            if not line:
                continue

            words = line.split()
            if words:
                first_word = words[0].lower()
                if first_word == '.include':
                    include_path = ' '.join(words[1:]).strip('"')   # Remove quotes
                    if os.path.isabs(include_path):
                        include_fp = open(include_path, 'r')
                    else:
                        include_fp = open(os.path.join(os.path.dirname(fp.name), include_path), 'r') # Open the included file
                    process_file(include_fp) # Process the included file recursively to handle nested includes
                    include_fp.close()
                else:
                    if ''.join(words[1:]).startswith('"'):  # if the first character is a quote, we have a text directive
                        rest = ' '.join(words[1:])
                    else:
                        rest = ''.join(words[1:]).lower()
                    tokens.append([first_word, rest])

    process_file(fp)
    return tokens
