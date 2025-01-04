import sys
from handles import *


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

other_opcodes = [
    'lda', 'ldx', 'ldy', 'sta', 'stx', 'sty', 'adc', 'sbc', 'inc', 'dec',
    'and', 'eor', 'ora', 'cmp', 'cpx', 'cpy', 'bit', 'asl', 'lsr', 'rol', 'ror'
]


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
                opcode_line = handle_lda(tokens, i)       
            if(tokens[i][0]=='ldx'):
                opcode_line = handle_ldx(tokens, i)
            if(tokens[i][0]=='ldy'):
                opcode_line = handle_ldy(tokens, i)
            if(tokens[i][0]=='sta'):
                opcode_line = handle_sta(tokens, i)   
            if(tokens[i][0]=='stx'):
                opcode_line = handle_stx(tokens, i)    
            if(tokens[i][0]=='sty'):
                opcode_line = handle_sty(tokens, i)      
            if(tokens[i][0]=='adc'):
                opcode_line = handle_adc(tokens, i)
            if(tokens[i][0]=='sbc'):
                opcode_line = handle_sbc(tokens, i)
            if(tokens[i][0]=='inc'):
                opcode_line = handle_inc(tokens, i)
            if(tokens[i][0]=='dec'):
                opcode_line = handle_dec(tokens, i)      
            if(tokens[i][0]=='and'):
                opcode_line = handle_and(tokens, i)     
            if(tokens[i][0]=='eor'):
                opcode_line = handle_eor(tokens, i)
            if(tokens[i][0]=='ora'):
                opcode_line = handle_ora(tokens, i)
            if(tokens[i][0]=='cmp'):
                opcode_line = handle_cmp(tokens, i)
            if(tokens[i][0]=='cpx'):
                opcode_line = handle_cpx(tokens, i)
            if(tokens[i][0]=='cpy'):
                opcode_line = handle_cpy(tokens, i)     
            if(tokens[i][0]=='bit'):
                opcode_line = handle_bit(tokens, i)
            if(tokens[i][0]=='asl'):
                opcode_line = handle_asl(tokens, i)    
            if(tokens[i][0]=='lsr'):
                opcode_line = handle_lsr(tokens, i)  
            if(tokens[i][0]=='rol'):
                opcode_line = handle_rol(tokens, i)     
            if(tokens[i][0]=='ror'):
                opcode_line = handle_ror(tokens, i)      
            if(tokens[i][0]=='jmp'):
                opcode_line = handle_jmp(tokens, i)       
            if(tokens[i][0]=='jsr'):
                opcode_line = handle_jsr(tokens, i)
            if(tokens[i][0]=='.byte'):
                opcode_line = handle_byte_directive(tokens[i][1])
            if(tokens[i][0]=='.word'):
                opcode_line = handle_word_directive(tokens[i][1])
            if(tokens[i][0]=='.text'):
                opcode_line = handle_text_directive(tokens[i][1])
            if(tokens[i][0]=='.org' and i!=0):                      # we skip the first org directive, if it exists
                opcode_line = handle_org_directive(tokens[i][1])
            if(tokens[i][0]=='.res' and i!=0):                      
                opcode_line = handle_res_directive(tokens[i][1])
            
        if (opcode_line != None):
            if type(opcode_line)==int:
                op_codes.append(opcode_line)
            else:
                for i in range(len(opcode_line)):
                    op_codes.append(opcode_line[i])
                    
    return op_codes


