from storage import memory, register, variable
from bin_convert import HalfPrecision

operations = []
operationCodes = []

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

    # @staticmethod
    # def encodeOp(operand):
    #     if (type(operand)==type(int())):
    #         return HalfPrecision.hpdec2bin(operand)
    #     if (type(operand)==type(str())):
    #         if (operand.startswith("M:")):
    #             variable.data["MSG"].append()

if __name__ == "__main__":
    pass    

    

