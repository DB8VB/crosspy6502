import sys

def is_hex_string(string):
    return all(c in '0123456789abcdefABCDEF' for c in string)


def check_type(params, line):
    
    # test if zero page or absolute address in decimal
    if isinstance(params, int):
        if (int(params) >=0 and int(params) < 256):
            return [2, int(params)]                            # zero page
        if (int(params) >=256 and int(params) <= 65535):
            return [1, int(params)]                            # absolute
        else:
            print ("Line ", line,": Memory address out of range...\n" )
            sys.exit(1)
            
            
    # test if zero page or absolute address in hexadecimal
    if (params[0]=='$' and ',' not in params and is_hex_string(params[1:])):
        if (int(params[1:],16) >=0 and int(params[1:],16) < 256):
            return [2, int(params[1:],16)]                            # zero page
        if (int(params[1:],16) >=256 and int(params[1:],16) <= 65535):
            return [1, int(params[1:],16)]                            # absolute
        else:
            print( "Line ", line,": Memory address out of range...\n" )
            sys.exit(1)
            
            
            
    # test if immediate decimal
    if (params[0]=='#' and params[1:].isnumeric()):
        if (int(params[1:]) >=0 and int(params[1:]) < 256):
            return [3, int(params[1:])]
        else:
            print( "Line ", line,": Value out of bounds (register size is 0-255 / $00-$FF)\n" )
            sys.exit(1)
            
            
    # test if immediate hexadecimal
    if (params[0]=='#' and params[1]=='$' and is_hex_string(params[2:])):
            if (int(params[2:],16) >=0 and int(params[2:],16) < 256):
                return [3, int(params[2:],16)]
            else:
                print( "Line ", line,": Value out of bounds (register size is 0-255 / $00-$FF)\n" )
                sys.exit(1)
        
    # test if absolute or zero page indexed, x in decimal
    
    if params[-2:] == ',x':
        addr = params.split(',')[0]
        
        if addr.isnumeric():
            if (int(addr) >=0 and int(addr) < 256):
                return [6, int(addr)]                           # zero page
            if (int(addr) >=256 and int(addr) <= 65535):
                return [4, int(addr)]                           # absolute
            else:
                print ("Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
            
            
    # test if absolute or zero page indexed, x in hexadecimal
    if params[-2:] == ',x':
        addr = params.split(',')[0]
        
        if (params[0]=='$' and is_hex_string(addr[1:])):
            if (int(addr[1:],16) >=0 and int(addr[1:],16) < 256):
                return [6, int(addr[1:],16)]                            # zero page
            if (int(addr[1:],16) >=256 and int(addr[1:],16) <= 65535):
                return [4, int(addr[1:],16)]                            # absolute
            else:
                print( "Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
                
                
                
    # test if absolute or zero page indexed, y in decimal
    
    if params[-2:] == ',y':
        addr = params.split(',')[0]
        
        if addr.isnumeric():
            if (int(addr) >=0 and int(addr) < 256):
                return 7                            # zero page
            if (int(addr) >=256 and int(addr) <= 65535):
                return 5                            # absolute
            else:
                print ("Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
            
            
    # test if absolute or zero page indexed, y in hexadecimal
    if params[-2:] == ',y':
        addr = params.split(',')[0]
        
        if (params[0]=='$' and is_hex_string(addr[1:])):
            if (int(addr[1:],16) >=0 and int(addr[1:],16) < 256):
                return [7, int(addr[1:],16)]                            # zero page
            if (int(addr[1:],16) >=256 and int(addr[1:],16) <= 65535):
                return [5, int(addr[1:],16)]                           # absolute
            else:
                print( "Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
                
    
    # test if indexed indirect in decimal
    
    if params[0] == '(' and params[-3:] == ',x)':
        addr = params.split(',')[0][1:]
        
        if addr.isnumeric():
            if (int(addr) >=0 and int(addr) < 256):
                return [8,int(addr)]                           
            else:
                print ("Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
            
            
    # test if indexed indirect in hexadecimal
    if params[0] == '(' and params[-3:] == ',x)':
        addr = params.split(',')[0][1:]
        
        if (params[1]=='$' and is_hex_string(addr[1:])):
            if (int(addr[1:],16) >=0 and int(addr[1:],16) < 256):
                return [8, int(addr[1:],16)]                            # zero page
            else:
                print( "Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
                
    # opt 9: ($aa),y   - indirect indexed
    
    # test if indirect indexed in decimal
    
    if params[0] == '(' and params[-3:] == '),y':
        addr = params.split(')')[0][1:]
        
        if addr.isnumeric():
            if (int(addr) >=0 and int(addr) < 256):
                return [9, int(addr)]                           
            else:
                print ("Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
            
            
    # test if indirect indexed  in hexadecimal
    if params[0] == '(' and params[-3:] == '),y':
        addr = params.split(')')[0][1:]
        
        if (params[1]=='$' and is_hex_string(addr[1:])):
            if (int(addr[1:],16) >=0 and int(addr[1:],16) < 256):
                return [9, int(addr[1:],16)]                            # zero page
            else:
                print( "Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
                
    # test if accumulator
    
    if params == "A":
        return [10]                        

       
    # test if indirect jump addr is hexadecimal
    if params[0:2]=='($' and params[-1:]==')':
        addr = params[2:-1]
        if is_hex_string(addr):
            if (int(addr,16) >=0 and int(addr,16) <= 65535):
                return [11,int(addr,16)]
            else:
                print( "Line ", line,": Memory address out of range...\n" )
                sys.exit(1)
                
          
    # test if indirect jump addr is decimal
    if params[0:1]=='(' and params[-1:]==')' :
        addr = params[1:-1]
        if addr.isnumeric():
            if (int(addr) >=0 and int(addr) <= 65535):
                return [11,int(addr)]
            else:
                print( "Line ", line,": Memory address out of range...\n" )
                sys.exit(1)


def handle_lda(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xad, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xa5, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0xa9, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0xbd, int(address[2:4], 16), int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0xb9, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0xb5, int(address[0:2], 16)]
        case 8:
            address = '{:02x}'.format(ret_code[1])
            return [0xa1, int(address[0:2], 16)]
        case 9:
            address = '{:02x}'.format(ret_code[1])
            return [0xb1, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', (i + 1))
            print('Ret_code:', ret_code)
            return []


def handle_ldx(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xae, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xa6, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0xa2, int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0xbe, int(address[2:4], 16), int(address[0:2], 16)]
        case 7:
            address = '{:02x}'.format(ret_code[1])
            return [0xb6, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []
        
def handle_ldy(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xac, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xa4, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0xa0, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0xbc, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0xb4, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_sta(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x8d, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x85, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x9d, int(address[2:4], 16), int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0x99, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x95, int(address[0:2], 16)]
        case 8:
            address = '{:02x}'.format(ret_code[1])
            return [0x81, int(address[0:2], 16)]
        case 9:
            address = '{:02x}'.format(ret_code[1])
            return [0x91, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_stx(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x8e, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x86, int(address[0:2], 16)]
        case 7:
            address = '{:02x}'.format(ret_code[1])
            return [0x96, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_sty(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x8c, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x84, int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x94, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_adc(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x6d, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x65, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0x69, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x7d, int(address[2:4], 16), int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0x79, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x75, int(address[0:2], 16)]
        case 8:
            address = '{:02x}'.format(ret_code[1])
            return [0x61, int(address[0:2], 16)]
        case 9:
            address = '{:02x}'.format(ret_code[1])
            return [0x71, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_sbc(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xed, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xe5, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0xe9, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0xfd, int(address[2:4], 16), int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0xf9, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0xf5, int(address[0:2], 16)]
        case 8:
            address = '{:02x}'.format(ret_code[1])
            return [0xe1, int(address[0:2], 16)]
        case 9:
            address = '{:02x}'.format(ret_code[1])
            return [0xf1, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_inc(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xee, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xe6, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0xfe, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0xf6, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_dec(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xce, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xc6, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0xde, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0xd6, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_and(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x2d, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x25, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0x29, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x3d, int(address[2:4], 16), int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0x39, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x35, int(address[0:2], 16)]
        case 8:
            address = '{:02x}'.format(ret_code[1])
            return [0x21, int(address[0:2], 16)]
        case 9:
            address = '{:02x}'.format(ret_code[1])
            return [0x31, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_eor(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x4d, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x45, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0x49, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x5d, int(address[2:4], 16), int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0x59, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x55, int(address[0:2], 16)]
        case 8:
            address = '{:02x}'.format(ret_code[1])
            return [0x41, int(address[0:2], 16)]
        case 9:
            address = '{:02x}'.format(ret_code[1])
            return [0x51, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_ora(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x0d, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x05, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0x09, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x1d, int(address[2:4], 16), int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0x19, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x15, int(address[0:2], 16)]
        case 8:
            address = '{:02x}'.format(ret_code[1])
            return [0x01, int(address[0:2], 16)]
        case 9:
            address = '{:02x}'.format(ret_code[1])
            return [0x11, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []
        
def handle_cmp(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xcd, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xc5, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0xc9, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0xdd, int(address[2:4], 16), int(address[0:2], 16)]
        case 5:
            address = '{:04x}'.format(ret_code[1])
            return [0xd9, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0xd5, int(address[0:2], 16)]
        case 8:
            address = '{:02x}'.format(ret_code[1])
            return [0xc1, int(address[0:2], 16)]
        case 9:
            address = '{:02x}'.format(ret_code[1])
            return [0xd1, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_cpx(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xec, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xe4, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0xe0, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_cpy(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0xcc, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0xc4, int(address[0:2], 16)]
        case 3:
            address = '{:02x}'.format(ret_code[1])
            return [0xc0, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_bit(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x2c, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x24, int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_asl(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x0e, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x06, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x1e, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x16, int(address[0:2], 16)]
        case 10:
            return 0x0a
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_lsr(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x4e, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x46, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x5e, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x56, int(address[0:2], 16)]
        case 10:
            return 0x4a
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_rol(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x2e, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x26, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x3e, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x36, int(address[0:2], 16)]
        case 10:
            return 0x2a
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_ror(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x6e, int(address[2:4], 16), int(address[0:2], 16)]
        case 2:
            address = '{:02x}'.format(ret_code[1])
            return [0x66, int(address[0:2], 16)]
        case 4:
            address = '{:04x}'.format(ret_code[1])
            return [0x7e, int(address[2:4], 16), int(address[0:2], 16)]
        case 6:
            address = '{:02x}'.format(ret_code[1])
            return [0x76, int(address[0:2], 16)]
        case 10:
            return 0x6a
        case _:
            print('Syntax error in line', i + 1)
            return []

def handle_jmp(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x4c, int(address[2:4], 16), int(address[0:2], 16)]
        case 11:
            address = '{:04x}'.format(ret_code[1])
            return [0x6c, int(address[2:4], 16), int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []
        
def handle_jsr(tokens, i):
    ret_code = check_type(tokens[i][1], i + 1)
    match ret_code[0]:
        case 1:
            address = '{:04x}'.format(ret_code[1])
            return [0x20, int(address[2:4], 16), int(address[0:2], 16)]
        case _:
            print('Syntax error in line', i + 1)
            return []


def handle_byte_directive(operands):
    # Split the values by commas
    byte_values = operands.split(',')

    memory = []
    
    # Remove possible spaces and convert the values
    for value in byte_values:
        value = value.strip()  # Remove spaces
        
        # Check for hex values
        if value.startswith('0x'):  # Hex with 0x
            byte_value = int(value[2:], 16)
        elif value.startswith('$'):  # Hex with $
            byte_value = int(value[1:], 16)
        else:  # Otherwise treat as decimal
            byte_value = int(value, 10)
        
        # Insert the byte value into memory (here simply a list)
        memory.append(byte_value)
        
    return memory

def handle_word_directive(operands):
    # Split the values by commas
    word_values = operands.split(',')

    memory = []
    
    # Remove possible spaces and convert the values
    for value in word_values:
        value = value.strip()  # Remove spaces
        
        # Check for hex values
        if value.startswith('0x'):  # Hex with 0x
            word_value = int(value[2:], 16)
        elif value.startswith('$'):  # Hex with $
            word_value = int(value[1:], 16)
        else:  # Otherwise treat as decimal
            word_value = int(value, 10)
        
        # Insert the word value into memory (here simply a list)
        # Little endian: low byte first
        memory.append(word_value & 0xFF)  # low byte
        memory.append((word_value >> 8) & 0xFF)  # high byte
        
    return memory

def handle_text_directive(operands):
    # Remove the surrounding quotes
    if operands.startswith('"') and operands.endswith('"'):
        operands = operands[1:-1]
    
    memory = []
    
    # Convert each character to its ASCII value
    for char in operands:
        memory.append(ord(char))
        
    return memory

def handle_org_directive(operands):
    
    memory = []
    
    # Convert each character to its ASCII value
    for i in range(int(operands)):
        memory.append(0x00)
        
    return memory
