from storage import memory, register, variable
from bin_convert import HalfPrecision

class Access:
    @staticmethod
    def data(addr, flow):
        pass
    @staticmethod
    def store(typ, addr, value):
        pass

class AddressingMode:
    @staticmethod
    def immediate(var):
        pass
    
    @staticmethod
    def relative(displace):
        pass
    
    @staticmethod
    def based(displace):
        pass
    
    @staticmethod
    def indexed(displace):
        pass
    
    @staticmethod
    def register(reg_addr):
        pass
    
    @staticmethod
    def register_indirect(reg_addr):
        pass
    
    @staticmethod
    def direct(var_addr):
        pass
    
    @staticmethod
    def indirect(var_addr):
        pass
    
    @staticmethod
    def autoinc(reg_addr):
        pass
    
    @staticmethod
    def autodec(reg_addr):
        pass