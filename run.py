from __future__ import annotations

import argparse
from pathlib import Path

from compiler import Instruction
from storage import memory, register, variable
from addressing import Access, AddressingMode


class Except:
    def __init__(self, msg, occur=True):
        self.message = msg
        self.occur = occur
        self.ret = None

    def dispMSG(self):
        print(self.message)

    def isOccur(self):
        return self.occur

    def setReturn(self, value):
        self.ret = value

    def getReturn(self):
        return self.ret


class Program:
    def __init__(self, program):
        Instruction.encodeProgram(program)

    @staticmethod
    def exception(name, value):
        if name == "DivByZero":
            lhs, rhs = value
            exc = Except("Division by zero", True)
            if rhs == 0 and lhs == 0:
                exc.setReturn("Infinity")
            elif rhs == 0:
                exc.setReturn("undefined")
            else:
                exc.setReturn(None)
                exc.occur = False
            return exc
        return Except(f"Unknown exception: {name}", False)

    @classmethod
    def write(cls, dest, src, movecode=0):
        if movecode == 1:
            pc_value = Access.data("PC", ["var", "reg"])
            Access.store("reg", int(variable.load("CR")), pc_value)
        elif movecode == 2:
            cr_value = Access.data("CR", ["var", "reg"])
            Access.store("reg", int(variable.load("PC")), cr_value)
        elif movecode == 3:
            src = input("SCAN> ")

        if not dest:
            return
        Access.store(dest["typ"], int(dest["addr"]), src)

    @classmethod
    def execute(cls, result, opcode):
        lhs, rhs = result
        execute_bit = opcode[0]
        write_bit = opcode[1]
        cat = opcode[2:5]

        if execute_bit == "1" and write_bit == "1":
            if cat == "000":
                return lhs % rhs
            if cat == "001":
                return lhs + rhs
            if cat == "010":
                return lhs - rhs
            if cat == "011":
                return lhs * rhs
            if cat == "100":
                if rhs == 0:
                    exc = cls.exception("DivByZero", (lhs, rhs))
                    return exc.getReturn()
                return lhs / rhs
            return lhs

        if execute_bit == "1" and write_bit == "0":
            jr = Access.data("JR", ["var", "reg"])
            if cat == "000":
                return jr == 0
            if cat == "001":
                return jr != 0
            if cat == "010":
                return jr < 0
            if cat == "011":
                return jr <= 0
            if cat == "100":
                return jr > 0
            if cat == "101":
                return jr >= 0
            if cat == "110":
                return True
            return False

        return result

    @staticmethod
    def _to_int(value):
        return int(float(value))

    @classmethod
    def getOp(cls, inscode, immediate=False, relative_based=False):
        if immediate:
            return AddressingMode.operand(None, AddressingMode.immediate(inscode), None)

        mode = inscode[:3]
        addr_bits = inscode[3:]
        return AddressingMode.resolve(mode, addr_bits, relative_based=relative_based)

    @classmethod
    def run(cls):
        while True:
            ir_reg_addr = int(variable.load("IR"))
            pc_reg_addr = int(variable.load("PC"))
            ins_address = cls._to_int(register.load(ir_reg_addr))
            instruction = memory.load(ins_address)

            if not isinstance(instruction, str) or len(instruction) != 32 or set(instruction) == {"0"}:
                break

            opcode = instruction[:5]
            immediate_bit = instruction[5]
            op1code = instruction[6:16]
            relative_based_bit = instruction[16]

            op1 = cls.getOp(op1code)
            op2 = None
            if immediate_bit == "1":
                op2 = cls.getOp(instruction[17:32], immediate=True)
            else:
                op2 = cls.getOp(instruction[17:27], relative_based=(relative_based_bit == "1"))

            execute_bit = opcode[0]
            write_bit = opcode[1]
            cat = opcode[2:5]

            if execute_bit == "1":
                if write_bit == "1":
                    if op2["value"] is not None:
                        result = cls.execute((op1["value"], op2["value"]), opcode)
                        cls.write(op1, result)
                    elif cat == "010":
                        jr_value = Access.data("JR", ["var", "reg"])
                        Access.store("reg", int(variable.load("JR")), jr_value - op1["value"])
                else:
                    should_jump = cls.execute((op1["value"], 0), opcode)
                    if should_jump:
                        target = op1["addr"] if op1["addr"] is not None else op1["value"]
                        Access.store("reg", pc_reg_addr, target)
            elif write_bit == "1":
                if cat == "000":
                    cls.write(op1, op2["value"])
                elif cat == "001":  # CALL
                    cls.write(None, None, movecode=1)
                    target = op1["addr"] if op1["addr"] is not None else op1["value"]
                    Access.store("reg", pc_reg_addr, target)
                elif cat == "010":  # RET
                    cls.write(None, None, movecode=2)
                    Access.store("reg", int(variable.load("ACC")), op1["value"])
                elif cat == "011":  # SCAN
                    cls.write(op1, None, movecode=3)
            else:
                if cat == "000":  # PRNT
                    if op2 and op2["value"] is not None:
                        print(op2["value"])
                    else:
                        print(op1["value"])
                elif cat == "001":  # EOP / FUNC
                    break

            next_pc = cls._to_int(register.load(pc_reg_addr))
            register.store(ir_reg_addr, next_pc)
            register.store(pc_reg_addr, next_pc + 1)


def _load_program_lines(path: Path):
    return path.read_text(encoding="utf-8").splitlines()


def main():
    parser = argparse.ArgumentParser(description="Run CMSC132 ISA program")
    parser.add_argument("program_file", help="Path to the source instruction file")
    args = parser.parse_args()

    lines = _load_program_lines(Path(args.program_file))
    Program(lines)
    Program.run()


if __name__ == "__main__":
    main()
