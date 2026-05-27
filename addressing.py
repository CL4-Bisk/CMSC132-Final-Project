from storage import memory, register, variable
from bin_convert import HalfPrecision

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
    def immediate(var):
        return HalfPrecision.hpbin2dec(var)
    
    @staticmethod
    def relative(displace):
        pc = Access.data("PC", ["var","reg"])
        effective_addr = pc + displace
        value = memory.load(effective_addr)
        return value
    
    @staticmethod
    def based(displace):
        br = Access.data("BR", ["var","reg"])
        effective_addr = br + displace
        value = memory.load(effective_addr)
        return value

    @staticmethod
    def indexed(displace):
        xr = Access.data("XR", ["var","reg"])
        effective_addr = xr + displace
        value = memory.load(effective_addr)
        return effective_addr, value
    
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