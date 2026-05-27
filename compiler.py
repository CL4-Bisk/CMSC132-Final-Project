from storage import memory, register, variable
from bin_convert import HalfPrecision

operations = []
operationCodes = []

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

if __name__ == "__main__":
    print(Instruction.encodeOp("R1"))
    print(Instruction.encodeOp("B"))
    print(Instruction.encodeOp("(R1)"))
    print(Instruction.encodeOp("(B)"))
    print(Instruction.encodeOp("(R1Z)"))
    print(Instruction.encodeOp("(BZ)"))
    print(Instruction.encodeOp("(R1Y)"))
    print(Instruction.encodeOp("(BY)"))
    print(Instruction.encodeOp("(R1X)"))
    print(Instruction.encodeOp("(BX)"))
    print(Instruction.encodeOp("(R1+)"))
    print(Instruction.encodeOp("(B+)"))
    print(Instruction.encodeOp("(R1-)"))
    print(Instruction.encodeOp("(B-)"))




    

