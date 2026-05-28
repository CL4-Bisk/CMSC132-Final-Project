from storage import memory, register, variable
from bin_convert import HalfPrecision, Length

operations = [
    # Execute=1, Write=1
    ["MOD", "ADD", "CB", "CF", "SUB", "CMP", "MUL", "DIV"],
    # Execute=1, Write=0
    ["JEQ", "JNE", "JLT", "JLE", "JGT", "JGE", "JMP"],
    # Execute=0, Write=1
    ["MOV", "ADDPC", "CALL", "RET", "SCAN"],
    # Execute=0, Write=0
    ["PRNT", "EOP", "FUNC"],
]

operationCodes = [
    # First group: Execute+Write bits per group (matches group index above)
    ["11", "10", "01", "00"],

    # Second group: Category Codes per member position inside their group
    ["000", "001", "001", "001", "010", "010", "011", "100",   # Execute=1, Write=1
     "000", "001", "010", "011", "100", "101", "110",          # Execute=1, Write=0
     "000", "000", "001", "010", "011",                        # Execute=0, Write=1
     "000", "001", "001"],                                     # Execute=0, Write=0
]

# General Addressing Modes
REGISTER_DIRECT     = "000"
REGISTER_INDIRECT   = "001"
DIRECT              = "010"
INDIRECT            = "011"
INDEXED_MEMREG_DISP = "100"
INDEXED_INT_DISP    = "101"
AUTO_INCREMENT      = "110"
AUTO_DECREMENT      = "111" 

# Addressing Mode when RELATIVE bit is 1 (For second operand only)
BASED_REG           = "000"
BASED_MEM           = "001"
BASED_POS           = "010"
BASED_NEG           = "011"
RELATIVE_REG        = "100"
RELATIVE_MEM        = "101"
RELATIVE_POS        = "110"
RELATIVE_NEG        = "111"

# Registers
REGISTER_NAME = [
    "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8",
    "BR", "XR", "ACC", "IR", "PC", "JR", "CR"
]

class Instruction:
    @staticmethod
    def decodeMSG(msg):
        """Converts each dash to space, underscore to tab, dash+underscore to newline. Also converts the
        word minus to dash, and the word under to underscore."""
        msg = msg.replace('-_', '\n')
        msg = msg.replace('-', ' ')
        msg = msg.replace('_', '\t')
        msg = msg.replace('minus', '-')
        msg = msg.replace('under', '_')
        return msg

    @staticmethod
    def encodeOp(operand):
        if isinstance(operand, (int, float)):
            return HalfPrecision.hpdec2bin(operand)

        if isinstance(operand, str) and (operand.startswith("(") and operand.endswith(")")):
            operand = operand.replace("(", "").replace(")", "")
            addressOperand = None
            
            if (operand.endswith("Z")):
                operand = operand[:-1]
                negative = operand.startswith("-")
                operand = operand.lstrip("-")

                if (operand.isdigit()):
                    addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(int(operand)), 7)
                    return f"{RELATIVE_POS}{addressOperand}" if (not negative) else f"{RELATIVE_NEG}{addressOperand}"
                else:                 
                    addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(variable.load(operand)), 7)
                    return f"{RELATIVE_REG}{addressOperand}" if (operand in REGISTER_NAME) else f"{RELATIVE_MEM}{addressOperand}"


            if (operand.endswith("Y")):
                operand = operand[:-1]
                negative = operand.startswith("-")
                operand = operand.lstrip("-")

                if (operand.isdigit()):
                    addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(int(operand)), 7)                    
                    return f"{BASED_POS}{addressOperand}" if (not negative) else f"{BASED_NEG}{addressOperand}"
                else:                 
                    addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(variable.load(operand)), 7)
                    return f"{BASED_REG}{addressOperand}" if (operand in REGISTER_NAME) else f"{BASED_MEM}{addressOperand}"


            if (operand.endswith("X")):
                operand = operand[:-1]
                negative = operand.startswith("-")
                operand = operand.lstrip("-")

                if (operand.isdigit()):
                    addressOperand = f"{'0' if not negative else '1'}{HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(int(operand)), 6)}"
                    return f"{INDEXED_INT_DISP}{addressOperand}"
                else:                 
                    addressOperand = f"{'0' if operand in REGISTER_NAME else '1'}{HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(variable.load(operand)), 6)}"
                    return f"{INDEXED_MEMREG_DISP}{addressOperand}"

            if (operand.endswith("+")):
                operand = operand[:-1]
                if (operand.isdigit()):
                    addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(int(operand)), 7)
                else: 
                    addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(variable.load(operand)), 7)               
                return f"{AUTO_INCREMENT}{addressOperand}"
            
            if (operand.endswith("-")):
                operand = operand[:-1]
                if (operand.isdigit()):
                    addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(int(operand)), 7)
                else: 
                    addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(variable.load(operand)), 7)              
                return f"{AUTO_DECREMENT}{addressOperand}"

            else:
                addressOperand = HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(variable.load(operand)), 7)
                if (operand in REGISTER_NAME):
                    return f"{REGISTER_INDIRECT}{addressOperand}"
                else:
                    return f"{INDIRECT}{addressOperand}"

        elif isinstance(operand, str):
            if (operand in REGISTER_NAME):
                return f"{REGISTER_DIRECT}{HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(variable.load(operand)), 7)}"
            else:
                return f"{DIRECT}{HalfPrecision.hpbin2bin(HalfPrecision.hpdec2bin(variable.load(operand)), 7)}"
        else:
            raise ValueError("Invalid operand type")
    
    @staticmethod
    def encode(inst):
        # helper to convert token string into int/float when appropriate
        def parse_token(tok):
            if isinstance(tok, (int, float)):
                return tok
            if not isinstance(tok, str):
                return tok
            
            # for negative integers, else returns a string token instead of an int 
            t = tok
            if t.lstrip('-').isdigit():
                return int(t)
            try:
                f = float(t)
                return f
            except Exception:
                return t

        # actual code
        try:
            instruction = {
                "opcode"    : "00000",
                "ib"        : "0",
                "op1mode"   : "000",
                "op1addr"   : "0000000",
                "rb"        : "0",
                "op2mode"   : "000",
                "op2addr"   : "0000000",
                "immediate" : "000000000000000"
            }

            #instruction parsing
            decodeMSG = Instruction.decodeMSG(inst)
            parts = inst.strip().replace(',', ' ').split()
            if len(parts) == 0:
                raise ValueError("Empty instruction")
            
            #operation parsing
            operation = parts[0].upper()
            group_index = None
            column_index = None
        
            if (operation == "FUNC"): return '0' * 32
            for i in range(len(operations)):
                if operation in operations[i]:
                    group_index = i
                    column_index = operations[i].index(operation)
                    break
            else:
                raise ValueError(f"Unknown operation {operation}")
            # Calculate flat index for operationCodes[1] by offsetting column_index by previous group sizes
            flat_cat_index = column_index + sum(len(operations[j]) for j in range(group_index))
            instruction["opcode"] = operationCodes[0][group_index] + operationCodes[1][flat_cat_index]

            # operand parsing
            operands = parts[1:]
            if len(operands) >= 1:
                p1 = parse_token(operands[0])
                enc1 = Instruction.encodeOp(p1)
            

                if (isinstance(enc1, str) and len(enc1) == 10):
                    # check for special case for each instruction if it allows or does not allow
                    NO_RELATIVE_AND_BASED_CASE = ((operation in ["MOD", "ADD", "SUB", "MUL", "DIV", "MOV", "ADDPC"]) and
                            (operands[0].replace("(", "").replace(")", "").strip()[-1] in ["Y", "Z"]))

                    ONLY_B_VARS = ((operation in ["CB"]) and not
                        (len(p1) == 2 and p1[0] == "B" and p1[1] in ["1", "2", "3", "4", "5", "6", "7", "8"]))     
                        
                    ONLY_F_VARS = ((operation in ["CF", "CALL"]) and not
                        (len(p1) == 2 and p1[0] == "F" and p1[1] in ["1", "2", "3", "4"]))    
                    
                    ONLY_B_OR_F_VARS = ((operation in ["JEQ", "JNE", "JLT", "JLE", "JGT", "JGE", "JMP"]) and not (
                        (len(p1) == 2 and p1[0] == "B" and p1[1] in ["1", "2", "3", "4", "5", "6", "7", "8"]) or
                        (len(p1) == 2 and p1[0] == "F" and p1[1] in ["1", "2", "3", "4"])))
                        
                    # an error has been detected
                    if (NO_RELATIVE_AND_BASED_CASE or ONLY_B_VARS or ONLY_F_VARS or ONLY_B_OR_F_VARS):
                        raise ValueError(f"Invalid first operand {p1} for instruction {operation}")
                    else: 
                        instruction["op1mode"] = enc1[:3]
                        instruction["op1addr"] = enc1[3:10]

                elif (isinstance(enc1, str) and len(enc1) == Length.precision):
                    raise ValueError(f"Immediate value not allowed as first operand {p1}")
                else:
                    raise ValueError(f"Invalid encoding for first operand {p1}")


            if len(operands) >= 2:
                p2 = parse_token(operands[1])
                enc2 = Instruction.encodeOp(p2)

                if isinstance(p2, (int, float)):
                    instruction["ib"] = '1'
                    instruction["immediate"] = HalfPrecision.hpbin2bin(enc2, 15)
                elif isinstance(p2, str) and len(enc2) == 10:
                    
                    # Check for special cases for second operand if it allows or does not allow
                    MEMREG_DIRECT_OR_IMMEDIATE_ONLY = ((operation in ["ADDPC"]) and not (enc2[:3] == REGISTER_DIRECT or enc2[:3] == DIRECT or instruction["ib"] == '1'))    
                    # Didn't put SCAN AND PRINT yet since me no habla PDF
                    
                    if (MEMREG_DIRECT_OR_IMMEDIATE_ONLY):
                        raise ValueError(f"Invalid second operand {p2} for instruction {operation}")
                    else:
                        instruction["op2mode"] = enc2[:3]
                        instruction["op2addr"] = enc2[3:10]
                    
                    # checking of addressing mode for RB bit
                    p2 = p2.replace("(", "").replace(")", "").strip()
                    if (instruction["op2mode"] in {BASED_REG, BASED_MEM, BASED_POS, BASED_NEG,
                                RELATIVE_REG, RELATIVE_MEM, RELATIVE_POS, RELATIVE_NEG} and p2[-1] in ["Y", "Z"]):
                        instruction["rb"] = '1'
                    else:
                        instruction["rb"] = '0'
        
            # return the instruction as a 32-bit binary string
            inst = (instruction["opcode"] + 
                        instruction["ib"] + 
                        instruction["op1mode"] +
                        instruction["op1addr"] +
                        instruction["rb"])

            if instruction["ib"] == '1':
                inst += instruction["immediate"]
            else:
                inst += (instruction["op2mode"] +
                        instruction["op2addr"] +
                        "00000")        
            return inst  
                    
        except (ValueError, KeyError) as e:
            print(f"Error: {str(e)}")

    @staticmethod
    def encodeProgram(program):
        try: 
            br_address = variable.load("BR")
            instructions = []
            block_counter = 0 
            multiline_comment = False
            block_register_operand = None
            program_address = br_address

            if not program: 
                raise ValueError("Empty program")
            
            for line in program:
                # dealing with whitespaces and blank lines
                line_stripped = line.strip()
                if not line_stripped or all(c in ' \t' for c in line_stripped):
                    continue

                # working with comments
                if line_stripped[0] == 'z':
                    multiline_comment = not multiline_comment
                    continue            

                if multiline_comment: 
                    continue

                if line_stripped[0] == 'x':
                    continue
            
                # working with instructions
                parts = line_stripped.split()
                if not parts: 
                    continue
                operation = parts[0].upper()
                
                #checks if operation creates a block variable
                if (operation in ["CB", "CF"]):
                    block_operand = parts[1]
                    variable.store(block_operand, HalfPrecision.hpdec2bin(program_address)) 
                    encoded_inst = Instruction.encode(line_stripped)
                    if encoded_inst:
                        instructions.insert(block_counter, encoded_inst)
                        block_counter += 1
                else:
                    encoded_inst = Instruction.encode(line_stripped)
                    instructions.append(encoded_inst) 
                
                program_address += 1


            register.store("BR", block_counter)
            current_address = br_address
            print(instructions)
            for inst in instructions:
                memory.store(current_address, inst)
                current_address += 1
        
        except (ValueError, KeyError) as e: 
            print(f"Error: {str(e)}")

        
        

if __name__ == "__main__":

    

    

