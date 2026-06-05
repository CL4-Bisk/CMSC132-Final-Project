from storage import memory, register, variable
from bin_convert import HalfPrecision

def _to_int(value):
    return int(float(value))


class Access:
    @staticmethod
    def data(addr, flow):
        current = addr
        
        for step in flow:
            if step == "var":
                current = variable.load(current)
            elif step == "reg":
                current = register.load(current)
            elif step == "mem":
                current = memory.load(current)
            else:
                raise ValueError(f"Invalid flow step: {step}")
            
        return current

    @staticmethod
    def store(typ, addr, value):
        if typ == "mem":
            memory.store(addr, value)
        elif typ == "reg":
            register.store(addr, value)
        else:
            raise ValueError(f"Invalid storage type: {typ}")

class AddressingMode:
    @staticmethod
    def operand(addr, value, typ):
        return {"addr": addr, "value": value, "typ": typ}

    @staticmethod
    def immediate(var):
        return int(var, 2)

    @classmethod
    def resolve(cls, mode, addr_bits, relative_based=False):
        if relative_based:
            return cls.resolve_relative_based(mode, addr_bits)
        return cls.resolve_regular(mode, addr_bits)

    @classmethod
    def resolve_regular(cls, mode, addr_bits):
        addr = int(addr_bits, 2)

        if mode == "000":  # register direct
            value = register.load(addr)
            return cls.operand(addr, value, "reg")
        if mode == "001":  # register indirect
            effective_addr = _to_int(register.load(addr))
            value = memory.load(effective_addr)
            return cls.operand(effective_addr, value, "mem")
        if mode == "010":  # direct
            value = memory.load(addr)
            return cls.operand(addr, value, "mem")
        if mode == "011":  # indirect
            effective_addr = _to_int(memory.load(addr))
            value = memory.load(effective_addr)
            return cls.operand(effective_addr, value, "mem")
        if mode == "100":  # indexed (reg/mem displacement)
            disp_type = int(addr_bits[0], 2)
            disp_addr = int(addr_bits[1:], 2)
            displacement = register.load(disp_addr) if disp_type == 0 else memory.load(disp_addr)
            return cls.indexed(displacement)
        if mode == "101":  # indexed (integer displacement)
            sign_bit = int(addr_bits[0], 2)
            displacement = int(addr_bits[1:], 2)
            displacement = -displacement if sign_bit else displacement
            return cls.indexed(displacement)
        if mode == "110":  # auto-increment
            effective_addr, value = cls.autoinc(addr)
            return cls.operand(effective_addr, value, "mem")
        if mode == "111":  # auto-decrement
            effective_addr, value = cls.autodec(addr)
            return cls.operand(effective_addr, value, "mem")

        raise ValueError(f"Unknown addressing mode: {mode}")

    @classmethod
    def resolve_relative_based(cls, mode, addr_bits):
        addr = int(addr_bits, 2)

        if mode == "000":  # based register
            return cls.based(register.load(addr))
        if mode == "001":  # based memory
            return cls.based(memory.load(addr))
        if mode == "010":  # based positive
            return cls.based(addr)
        if mode == "011":  # based negative
            return cls.based(-addr)
        if mode == "100":  # relative register
            return cls.relative(register.load(addr))
        if mode == "101":  # relative memory
            return cls.relative(memory.load(addr))
        if mode == "110":  # relative positive
            return cls.relative(addr)
        if mode == "111":  # relative negative
            return cls.relative(-addr)

        raise ValueError(f"Unknown relative/based mode: {mode}")
    
    @staticmethod
    def relative(displace):
        pc = Access.data("PC", ["var","reg"])
        effective_addr = pc + displace
        value = memory.load(effective_addr)
        return AddressingMode.operand(_to_int(effective_addr), value, "mem")
    
    @staticmethod
    def based(displace):
        br = Access.data("BR", ["var","reg"])
        effective_addr = br + displace
        value = memory.load(effective_addr)
        return AddressingMode.operand(_to_int(effective_addr), value, "mem")

    @staticmethod
    def indexed(displace):
        xr = Access.data("XR", ["var","reg"])
        effective_addr = xr + displace
        value = memory.load(effective_addr)
        return AddressingMode.operand(_to_int(effective_addr), value, "mem")
    
    @staticmethod
    def register(reg_addr):
        effective_addr = HalfPrecision.hpbin2dec(reg_addr)
        value = register.load(reg_addr)
        return effective_addr, value, register
    
    @staticmethod
    def register_indirect(reg_addr):
        effective_addr = register.load(reg_addr)
        value = memory.load(effective_addr)
        return effective_addr, value
    
    @staticmethod
    def direct(var_addr):
        effective_addr = HalfPrecision.hpbin2dec(var_addr)
        value = memory.load(effective_addr)
        return effective_addr, value
    
    @staticmethod
    def indirect(var_addr):
        effective_addr = memory.load(var_addr)
        value = memory.load(effective_addr)
        return effective_addr, value
    
    @staticmethod
    def autoinc(reg_addr):
        effective_addr = register.load(reg_addr)
        value = memory.load(effective_addr)
        register.store(reg_addr, effective_addr + 1)
        return effective_addr, value
        
    
    @staticmethod
    def autodec(reg_addr):
        effective_addr = register.load(reg_addr) - 1
        register.store(reg_addr, effective_addr)
        value = memory.load(effective_addr)
        return effective_addr, value
