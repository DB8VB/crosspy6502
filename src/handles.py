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
