import sys
from handles import *

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

    # TBD: Create handles for different commands and simplify the code
def parse( tokens ):
    
    op_codes = []
    
    for i in range(len(tokens)):
        
        opcode_line = None
        
        if(tokens[i][0] in single_opcode_dict):
            opcode_line = single_opcode_dict[tokens[i][0]][0]
        elif tokens[i][0] in double_opcode_dict:                  # for double opcodes
            ret_code = check_type(tokens[i][1], i+1)              # check if the adress is a byte value
            match ret_code[0]:
                case 2:                                           # if yes
                    address = '{:02x}'.format(ret_code[1])        # create hex
                    opcode_line = [double_opcode_dict[tokens[i][0]][0],int(address,16)]  # and write
                case _: 
                        print('Syntax error in line',i)
        else:
            if(tokens[i][0]=='lda'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]: 
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xad,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xa5,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xa9,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xbd,int(address[2:4],16),int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xb9,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xb5,int(address[0:2],16)]
                    case 8:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xa1,int(address[0:2],16)]
                    case 9:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xb1,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line ',(i+1))
                        print('Ret_code: ',ret_code)
                        
            if(tokens[i][0]=='ldx'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xae,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xa6,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xa2,int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xbe,int(address[2:4],16),int(address[0:2],16)]
                    case 7:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xb6,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='ldy'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xac,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xa4,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xa0,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xbc,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xb4,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='sta'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x8d,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x85,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x9d,int(address[2:4],16),int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x99,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x95,int(address[0:2],16)]
                    case 8:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x81,int(address[0:2],16)]
                    case 9:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x91,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='stx'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x8e,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x86,int(address[0:2],16)]
                    case 7:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x96,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='sty'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x8c,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x84,int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x94,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='adc'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x6d,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x65,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x69,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x7d,int(address[2:4],16),int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x79,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x75,int(address[0:2],16)]
                    case 8:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x61,int(address[0:2],16)]
                    case 9:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x71,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='sbc'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xed,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xe5,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xe9,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xfd,int(address[2:4],16),int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xf9,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xf5,int(address[0:2],16)]
                    case 8:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xe1,int(address[0:2],16)]
                    case 9:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xf1,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='inc'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xee,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xe6,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xfe,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xf6,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='dec'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xce,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xc6,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xde,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xd6,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='and'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x2d,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x25,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x29,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x3d,int(address[2:4],16),int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x39,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x35,int(address[0:2],16)]
                    case 8:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x21,int(address[0:2],16)]
                    case 9:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x31,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='eor'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x4d,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x45,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x49,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x5d,int(address[2:4],16),int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x59,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x55,int(address[0:2],16)]
                    case 8:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x41,int(address[0:2],16)]
                    case 9:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x51,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='ora'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x0d,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x05,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x09,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x1d,int(address[2:4],16),int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x19,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x15,int(address[0:2],16)]
                    case 8:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x01,int(address[0:2],16)]
                    case 9:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x11,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='cmp'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xcd,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xc5,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xc9,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xdd,int(address[2:4],16),int(address[0:2],16)]
                    case 5:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xd9,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xd5,int(address[0:2],16)]
                    case 8:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xc1,int(address[0:2],16)]
                    case 9:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xd1,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='cpx'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xec,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xe4,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xe0,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='cpy'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0xcc,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xc4,int(address[0:2],16)]
                    case 3:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0xc0,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='bit'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x2c,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x24,int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='asl'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x0e,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x06,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x1e,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x16,int(address[0:2],16)]
                    case 10:
                        opcode_line = 0x0a
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='lsr'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x4e,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x46,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x5e,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x56,int(address[0:2],16)]
                    case 10:
                        opcode_line = 0x4a
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='rol'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x2e,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x26,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x3e,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x36,int(address[0:2],16)]
                    case 10:
                        opcode_line = 0x2a
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='ror'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x6e,int(address[2:4],16),int(address[0:2],16)]
                    case 2:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x66,int(address[0:2],16)]
                    case 4:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x6a,int(address[2:4],16),int(address[0:2],16)]
                    case 6:
                        address = '{:02x}'.format(ret_code[1])
                        opcode_line = [0x7e,int(address[0:2],16)]
                    case 10:
                        opcode_line = 0x6a
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='jmp'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x4c,int(address[2:4],16),int(address[0:2],16)]
                    case 11:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x6c,int(address[2:4],16),int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='jsr'):
                ret_code = check_type(tokens[i][1], i+1)
                match ret_code[0]:
                    case 1:
                        address = '{:04x}'.format(ret_code[1])
                        opcode_line = [0x20,int(address[2:4],16),int(address[0:2],16)]
                    case _: 
                        print('Syntax error in line',i+1)
                        
            if(tokens[i][0]=='.byte'):
                opcode_line = handle_byte_directive(tokens[i][1])

            if(tokens[i][0]=='.word'):
                opcode_line = handle_word_directive(tokens[i][1])

            if(tokens[i][0]=='.text'):
                opcode_line = handle_text_directive(tokens[i][1])

            if(tokens[i][0]=='.org' and i!=0):                      # we skip the first org directive, if it exists
                opcode_line = handle_org_directive(tokens[i][1])
            
                        
        if (opcode_line != None):
            if type(opcode_line)==int:
                op_codes.append(opcode_line)
            else:
                for i in range(len(opcode_line)):
                    op_codes.append(opcode_line[i])
                    
    return op_codes


single_opcode_dict = {
    'brk': [0x00, 1], 'php': [0x08, 1], 'asl': [0x0A, 1], 'clc': [0x18, 1],
    'plp': [0x28, 1], 'rol': [0x2A, 1], 'sec': [0x38, 1], 'rti': [0x40, 1],
    'pha': [0x48, 1], 'lsr': [0x4A, 1], 'cli': [0x58, 1], 'rts': [0x60, 1],
    'pla': [0x68, 1], 'ror': [0x6A, 1], 'sei': [0x78, 1], 'dey': [0x88, 1],
    'txa': [0x8A, 1], 'tya': [0x98, 1], 'txs': [0x9A, 1], 'tay': [0xA8, 1],
    'tax': [0xAA, 1], 'clv': [0xB8, 1], 'tsx': [0xBA, 1], 'iny': [0xC8, 1],
    'dex': [0xCA, 1], 'cld': [0xD8, 1], 'inx': [0xE8, 1], 'nop': [0xEA, 1],
    'sed': [0xF8, 1]
}
double_opcode_dict = {
    'bcc': [0x90, 2], 'bcs': [0xB0, 2], 'beq': [0xF0, 2], 'bmi': [0x30, 2],
    'bne': [0xD0, 2], 'bpl': [0x10, 2], 'bvc': [0x50, 2], 'bvs': [0x70, 2]
}
triple_opcode_dict = {
    'jmp': [0x4C, 3], 'jsr': [0x20, 3]
}
other_opcodes = ['lda','ldx','ldy','sta','stx','sty','adc','sbc','inc','dec','and','eor','ora','cmp','cpx','cpy','bit','asl','lsr','rol','ror']
