import sys
from parser import single_opcode_dict, double_opcode_dict, triple_opcode_dict, other_opcodes, is_hex_string, check_type

# In this early version .org must be the first line in the file -- if needed
def get_memory_offset(tokens):
    offset = 0

    if (tokens[0][0] == '.org'):          
        if (tokens[0][1][0]=='$' and is_hex_string(tokens[0][1][1:])):
            if (int(tokens[0][1][1:],16) >=0 ) and int(tokens[0][1][1:],16) <= 65535:
                return int(tokens[0][1][1:],16)
            else:
                print ("File offset (.org) address out of range...\n" )
                sys.exit(1)
                
        if tokens[0][1].isnumeric():
            if (int(tokens[0][1]) >=0 and int(tokens[0][1]) <= 65535):
                return int(tokens[0][1])                        
            else:
                print ("File offset (.org) address out of range...\n" )
                sys.exit(1)
    return offset

def get_constants(tokens):
    constants = []
    for i in range(len(tokens)):
        if (tokens[i][0] == '.const'):
            constants.append([tokens[i][1].lower(), tokens[i][2].lower()])
    return constants

def replace_constants(tokens, constants):
    for i in range(len(tokens)):
        for j in range(len(constants)):
            if constants[j][0] in tokens[i][1]:
                tokens[i][1] = tokens[i][1].replace(constants[j][0], constants[j][1])
    return tokens

# Every line where the first word ends with a colon is a label
def get_labels(tokens):
    labels = []
    for i in range(len(tokens)):
        if (tokens[i][0][-1] == ':'):
            labels.append([tokens[i][0][0:-1],0x0000])
    return labels


# reads through the file and returns a dictionary of all location
# labels with their line numbers
def get_label_offsets( tokens , offset, label_list):
    
    if tokens[0][0] == '.org':   # if .org is the first line, the offset given as parameter and we skip the first line i.e. we start at index 1
        start_index = 1
    else:                        # if .org is not the first line, the offset is 0x0000 and we start counting at index 0
        start_index = 0

    for i in range(start_index,len(tokens)):
        
        num_bytes  = 0
        
        if (tokens[i][0][-1] == ':'):                # test if label (identifies by ":" as last char)
            for item in label_list:                  # find label in list of lables
                if item[0] == tokens[i][0][0:-1]:    # label found
                    item[1] = offset             # set adress
                    break
        elif(tokens[i][0] in single_opcode_dict):   # always 1 byte
            num_bytes = 1
        elif(tokens[i][0] in double_opcode_dict):   # always 2 bytes
            num_bytes = 2
        elif(tokens[i][0] in triple_opcode_dict):   # always 3 bytes
            num_bytes = 3
        elif(tokens[i][0] == '.org'):
            if (tokens[i][1][0] =='$' and is_hex_string(tokens[i][1][1:])):
                if int(tokens[i][1][1:],16)<= 65535:
                    num_bytes = int(tokens[i][1][1:],16) - offset
                    tokens[i][1] = num_bytes        # IMPORTANT: we store the number of bytes in the .org directive - simplifies the calculation in the parser
                else:
                    print('Syntax error in line',i+1)
                    print(".org directive address out of range")
            elif tokens[i][1].isnumeric():
                if int(tokens[i][1])<= 65535:
                    num_bytes = int(tokens[i][1]) - offset
                    tokens[i][1] = num_bytes        # IMPORTANT: we store the number of bytes in the .org directive - simplifies the calculation in the parser
                else:
                    print('Syntax error in line',i+1)
                    print(".org directive address out of range")
        elif(tokens[i][0] == '.byte'):
            num_bytes = len(tokens[i][1].split(','))
        elif(tokens[i][0] == '.word'):
            num_bytes = len(tokens[i][1].split(',')) * 2
        elif(tokens[i][0] == '.text'):
            operands = tokens[i][1]
            if operands.startswith('"') and operands.endswith('"'):
                num_bytes = len(operands)-2
            else:
                print('Syntax error in line',i+1)
                print(".text directive must be surrounded by quotes")
        else:
            if(tokens[i][0] in other_opcodes):      # for other opcodes it is not clear how many bytes
                for index in range(len(label_list)):            # if the line contains a label, it is always 3 bytes
                    if (label_list[index][0] in tokens[i][1]):
                        num_bytes = 3
                if(num_bytes==0):                    # we skip this if we already found a label in line
                    ret_code = check_type(tokens[i][1], i+1)   # we check for types
                    match ret_code[0]:
                        case 1:
                            num_bytes = 3
                        case 2:
                            num_bytes = 2
                        case 3:
                            num_bytes = 2
                        case 4:
                            num_bytes = 3
                        case 5:
                            num_bytes = 3
                        case 6:
                            num_bytes = 2
                        case 7:
                            num_bytes = 2
                        case 8:
                            num_bytes = 2
                        case 9:
                            num_bytes = 2
                        case 10:
                            num_bytes = 1
                        case 11:
                            num_bytes = 3
                        case _: 
                            print('Syntax error in line',i+1)
                        
        offset = offset + num_bytes
    return label_list

# reads through the file and returns a dictionary of all location
# labels with their line numbers
def get_current_offset( tokens , offset, label_list,line):

    if tokens[0][0] == '.org':   # if .org is the first line, the offset given as parameter and we skip the first line i.e. we start at index 1
        start_index = 1
    else:                        # if .org is not the first line, the offset is 0x0000 and we start counting at index 0
        start_index = 0

    
    for i in range(start_index,line+1):   # important for counting
        num_bytes  = 0
        if(tokens[i][0] in single_opcode_dict):     # always 1 byte
            num_bytes = 1
        elif(tokens[i][0] in double_opcode_dict):   # always 2 bytes
            num_bytes = 2
            if i == line:
                return offset+2
        elif(tokens[i][0] in triple_opcode_dict):   # always 3 bytes
            num_bytes = 3
        elif(tokens[i][0] == '.org'):
            num_bytes = int(tokens[i][1])                # Remember: we stored the number of bytes in the .org directive (see get_label_offsets)
        elif(tokens[i][0] == '.byte'):
            num_bytes = len(tokens[i][1].split(','))    
        elif(tokens[i][0] == '.word'):
            num_bytes = len(tokens[i][1].split(',')) * 2      
        elif(tokens[i][0] == '.text'):
            operands = tokens[i][1]
            if operands.startswith('"') and operands.endswith('"'):
                num_bytes = len(operands)-2
            else:
                print('Syntax error in line',i+1)
                print(".text directive must be surrounded by quotes")
        else:
            if(tokens[i][0] in other_opcodes):      # for other opcodes it is not clear how many bytes
                for index in range(len(label_list)):            # if the line contains a label, it is always 3 bytes
                    if (label_list[index][0] == tokens[i][1]):
                        num_bytes = 3
                if(num_bytes==0):                    # we skip this if we already found a label in line
                    ret_code = check_type(tokens[i][1], i+1)   # we check for types
                    match ret_code[0]:
                        case 1:
                            num_bytes = 3
                        case 2:
                            num_bytes = 2
                        case 3:
                            num_bytes = 2
                        case 4:
                            num_bytes = 3
                        case 5:
                            num_bytes = 3
                        case 6:
                            num_bytes = 2
                        case 7:
                            num_bytes = 2
                        case 8:
                            num_bytes = 2
                        case 9:
                            num_bytes = 2
                        case 10:
                            num_bytes = 1
                        case 11:
                            num_bytes = 3
                        case _: 
                            print('Syntax error in line',i+1)
                        
        offset = offset + num_bytes
    return 0


def labels_to_adresses(tokens, label_offsets):
    for i in range(len(tokens)):
        for label, address in label_offsets:
            if label in tokens[i][1] and tokens[i][0] not in double_opcode_dict:
                tokens[i][1] = tokens[i][1].replace(label, f"${address:04X}")
    return tokens

def compute_relative_relative_addresses(tokens, offset, label_list):
    for i in range(len(tokens)):                       # walk through the source code    
        if (tokens[i][0] in double_opcode_dict):
            for j in range(len(label_list)):
                if (tokens[i][1] == label_list[j][0]):
                    label_offset    = label_list[j][1]
                    current_offset  = get_current_offset(tokens, offset, label_list,i)
                    offset_value    = label_offset - current_offset
                    if offset_value > 127 or offset_value < -128:
                        print('Error in line '+i+': Offset of label out of range - jump is too far')
                        break
                    if offset_value > 0:
                        byte_offset = offset_value
                    else:
                        byte_offset = 256 + (offset_value)
                    tokens[i][1] = tokens[i][1].replace(label_list[j][0], '$' + '{:02x}'.format(byte_offset))
    return tokens