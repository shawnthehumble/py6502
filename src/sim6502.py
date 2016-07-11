#!/usr/bin/env python

#
# The 65C02 Simulator
#
class sim6502:
    def __init__(self,object_code, symbols=None):
        self.pc = 0x0000
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.sp = 0x0100
        self.cc = 0x00
        self.object_code = object_code[:]
        for i in xrange(len(self.object_code)):
            if self.object_code[i] < 0:
                self.object_code[i] = 0x00
        self.build_opcode_table()
        
        if symbols==None:
            self.have_symbols = False
        else:
            self.have_symbols = True
            
            self.symbols = symbols
            self.labels = dict()
            for label in self.symbols:
                offset = self.symbols[label]
                self.labels[offset]=label

    def build_opcode_table(self):
        self.hexcodes=dict()
        self.hexcodes[0x00] = ("brk","implicit")
        self.hexcodes[0x10] = ("bpl","relative")
        self.hexcodes[0x20] = ("jsr","absolute")
        self.hexcodes[0x30] = ("bmi","relative")
        self.hexcodes[0x40] = ("rti","implicit")
        self.hexcodes[0x50] = ("bvc","relative")
        self.hexcodes[0x60] = ("rts","implicit")
        self.hexcodes[0x70] = ("bvs","relative")
        self.hexcodes[0x80] = ("bra","relative")
        self.hexcodes[0x90] = ("bcc","relative")
        self.hexcodes[0xA0] = ("ldy","immediate")
        self.hexcodes[0xB0] = ("bcs","relative")
        self.hexcodes[0xC0] = ("cpy","immediate")
        self.hexcodes[0xD0] = ("bne","relative")
        self.hexcodes[0xE0] = ("cpx","immediate")
        self.hexcodes[0xF0] = ("beq","relative")
        
        self.hexcodes[0x01] = ("ora","zeropageindexedindirectx")
        self.hexcodes[0x11] = ("ora","zeropageindexedindirecty")
        self.hexcodes[0x21] = ("and","zeropageindexedindirectx")
        self.hexcodes[0x31] = ("and","zeropageindexedindirecty")
        self.hexcodes[0x41] = ("eor","zeropageindexedindirectx")
        self.hexcodes[0x51] = ("eor","zeropageindexedindirecty")
        self.hexcodes[0x61] = ("adc","zeropageindexedindirectx")
        self.hexcodes[0x71] = ("adc","zeropageindexedindirecty")
        self.hexcodes[0x81] = ("sta","zeropageindexedindirectx")
        self.hexcodes[0x91] = ("sta","zeropageindexedindirecty")
        self.hexcodes[0xA1] = ("lda","zeropageindexedindirectx")
        self.hexcodes[0xB1] = ("lda","zeropageindexedindirecty")
        self.hexcodes[0xC1] = ("cmp","zeropageindexedindirectx")
        self.hexcodes[0xD1] = ("cmp","zeropageindexedindirecty")
        self.hexcodes[0xE1] = ("sbc","zeropageindexedindirectx")
        self.hexcodes[0xF1] = ("sbc","zeropageindexedindirecty")
        
        self.hexcodes[0x02] = ("","")
        self.hexcodes[0x12] = ("ora","zeropageindirect")
        self.hexcodes[0x22] = ("","")
        self.hexcodes[0x32] = ("and","zeropageindirect")
        self.hexcodes[0x42] = ("","")
        self.hexcodes[0x52] = ("eor","zeropageindirect")
        self.hexcodes[0x62] = ("","")
        self.hexcodes[0x72] = ("adc","zeropageindirect")
        self.hexcodes[0x82] = ("","")
        self.hexcodes[0x92] = ("sta","zeropageindirect")
        self.hexcodes[0xA2] = ("ldx","immediate")
        self.hexcodes[0xB2] = ("lda","zeropageindirect")
        self.hexcodes[0xC2] = ("","")
        self.hexcodes[0xD2] = ("cmp","zeropageindirect")
        self.hexcodes[0xE2] = ("","")
        self.hexcodes[0xF2] = ("sbc","zeropageindirect")
        
        self.hexcodes[0x03] = ("","")
        self.hexcodes[0x13] = ("","")
        self.hexcodes[0x23] = ("","")
        self.hexcodes[0x33] = ("","")
        self.hexcodes[0x43] = ("","")
        self.hexcodes[0x53] = ("","")
        self.hexcodes[0x63] = ("","")
        self.hexcodes[0x73] = ("","")
        self.hexcodes[0x83] = ("","")
        self.hexcodes[0x93] = ("","")
        self.hexcodes[0xA3] = ("","")
        self.hexcodes[0xB3] = ("","")
        self.hexcodes[0xC3] = ("","")
        self.hexcodes[0xD3] = ("","")
        self.hexcodes[0xE3] = ("","")
        self.hexcodes[0xF3] = ("","")
        
        self.hexcodes[0x04] = ("tsb","zeropage")
        self.hexcodes[0x14] = ("trb","zeropage")
        self.hexcodes[0x24] = ("bit","zeropage")
        self.hexcodes[0x34] = ("bit","zeropagex")
        self.hexcodes[0x44] = ("","")
        self.hexcodes[0x54] = ("","")
        self.hexcodes[0x64] = ("stz","zeropage")
        self.hexcodes[0x74] = ("stz","zeropagex")
        self.hexcodes[0x84] = ("sty","zeropage")
        self.hexcodes[0x94] = ("sty","zeropagex")
        self.hexcodes[0xA4] = ("ldy","zeropage")
        self.hexcodes[0xB4] = ("ldy","zeropagex")
        self.hexcodes[0xC4] = ("cpy","zeropage")
        self.hexcodes[0xD4] = ("","")
        self.hexcodes[0xE4] = ("cpx","zeropage")
        self.hexcodes[0xF4] = ("","")
        
        self.hexcodes[0x05] = ("ora","zeropage")
        self.hexcodes[0x15] = ("ora","zeropagex")
        self.hexcodes[0x25] = ("and","zeropage")
        self.hexcodes[0x35] = ("and","zeropagex")
        self.hexcodes[0x45] = ("eor","zeropage")
        self.hexcodes[0x55] = ("eor","zeropagex")
        self.hexcodes[0x65] = ("adc","zeropage")
        self.hexcodes[0x75] = ("adc","zeropagex")
        self.hexcodes[0x85] = ("sta","zeropage")
        self.hexcodes[0x95] = ("sta","zeropagex")
        self.hexcodes[0xA5] = ("lda","zeropage")
        self.hexcodes[0xB5] = ("lda","zeropagex")
        self.hexcodes[0xC5] = ("cmp","zeropage")
        self.hexcodes[0xD5] = ("cmp","zeropagex")
        self.hexcodes[0xE5] = ("sbc","zeropage")
        self.hexcodes[0xF5] = ("sbc","zeropagex")
        
        self.hexcodes[0x06] = ("asl","zeropage")
        self.hexcodes[0x16] = ("asl","zeropagex")
        self.hexcodes[0x26] = ("rol","zeropage")
        self.hexcodes[0x36] = ("rol","zeropagex")
        self.hexcodes[0x46] = ("lsr","zeropage")
        self.hexcodes[0x56] = ("lsr","zeropagex")
        self.hexcodes[0x66] = ("ror","zeropage")
        self.hexcodes[0x76] = ("ror","zeropagex")
        self.hexcodes[0x86] = ("stx","zeropage")
        self.hexcodes[0x96] = ("stx","zeropagey")
        self.hexcodes[0xA6] = ("ldx","zeropage")
        self.hexcodes[0xB6] = ("ldx","zeropagey")
        self.hexcodes[0xC6] = ("dec","zeropage")
        self.hexcodes[0xD6] = ("dec","zeropagex")
        self.hexcodes[0xE6] = ("inc","zeropage")
        self.hexcodes[0xF6] = ("inc","zeropagex")
        
        self.hexcodes[0x07] = ("","")
        self.hexcodes[0x17] = ("","")
        self.hexcodes[0x27] = ("","")
        self.hexcodes[0x37] = ("","")
        self.hexcodes[0x47] = ("","")
        self.hexcodes[0x57] = ("","")
        self.hexcodes[0x67] = ("","")
        self.hexcodes[0x77] = ("","")
        self.hexcodes[0x87] = ("","")
        self.hexcodes[0x97] = ("","")
        self.hexcodes[0xA7] = ("","")
        self.hexcodes[0xB7] = ("","")
        self.hexcodes[0xC7] = ("","")
        self.hexcodes[0xD7] = ("","")
        self.hexcodes[0xE7] = ("","")
        self.hexcodes[0xF7] = ("","")
        
        self.hexcodes[0x08] = ("php","implicit")
        self.hexcodes[0x18] = ("clc","implicit")
        self.hexcodes[0x28] = ("plp","implicit")
        self.hexcodes[0x38] = ("sec","implicit")
        self.hexcodes[0x48] = ("pha","implicit")
        self.hexcodes[0x58] = ("cli","implicit")
        self.hexcodes[0x68] = ("pla","implicit")
        self.hexcodes[0x78] = ("sei","implicit")
        self.hexcodes[0x88] = ("dey","implicit")
        self.hexcodes[0x98] = ("tya","implicit")
        self.hexcodes[0xA8] = ("tay","implicit")
        self.hexcodes[0xB8] = ("clv","implicit")
        self.hexcodes[0xC8] = ("iny","implicit")
        self.hexcodes[0xD8] = ("cld","implicit")
        self.hexcodes[0xE8] = ("inx","implicit")
        self.hexcodes[0xF8] = ("sed","implicit")
        
        self.hexcodes[0x09] = ("ora","immediate")
        self.hexcodes[0x19] = ("ora","absolutey")
        self.hexcodes[0x29] = ("and","immediate")
        self.hexcodes[0x39] = ("and","absolutey")
        self.hexcodes[0x49] = ("eor","immediate")
        self.hexcodes[0x59] = ("eor","absolutey")
        self.hexcodes[0x69] = ("adc","immediate")
        self.hexcodes[0x79] = ("adc","absolutey")
        self.hexcodes[0x89] = ("bit","immediate")
        self.hexcodes[0x99] = ("sta","absolutey")
        self.hexcodes[0xA9] = ("lda","immediate")
        self.hexcodes[0xB9] = ("lda","absolutey")
        self.hexcodes[0xC9] = ("cmp","immediate")
        self.hexcodes[0xD9] = ("cmp","absolutey")
        self.hexcodes[0xE9] = ("sbc","immediate")
        self.hexcodes[0xF9] = ("sbc","absolutey")
        
        self.hexcodes[0x0A] = ("asl","accumulator")
        self.hexcodes[0x1A] = ("ina","accumulator")
        self.hexcodes[0x2A] = ("rol","accumulator")
        self.hexcodes[0x3A] = ("dea","accumulator")
        self.hexcodes[0x4A] = ("lsr","accumulator")
        self.hexcodes[0x5A] = ("phy","implicit")
        self.hexcodes[0x6A] = ("ror","accumulator")
        self.hexcodes[0x7A] = ("ply","implicit")
        self.hexcodes[0x8A] = ("txa","implicit")
        self.hexcodes[0x9A] = ("txs","implicit")
        self.hexcodes[0xAA] = ("tax","implicit")
        self.hexcodes[0xBA] = ("tsx","implicit")
        self.hexcodes[0xCA] = ("dex","implicit")
        self.hexcodes[0xDA] = ("phx","implicit")
        self.hexcodes[0xEA] = ("nop","implicit")
        self.hexcodes[0xFA] = ("plx","implicit")
        
        self.hexcodes[0x0B] = ("","")
        self.hexcodes[0x1B] = ("","")
        self.hexcodes[0x2B] = ("","")
        self.hexcodes[0x3B] = ("","")
        self.hexcodes[0x4B] = ("","")
        self.hexcodes[0x5B] = ("","")
        self.hexcodes[0x6B] = ("","")
        self.hexcodes[0x7B] = ("","")
        self.hexcodes[0x8B] = ("","")
        self.hexcodes[0x9B] = ("","")
        self.hexcodes[0xAB] = ("","")
        self.hexcodes[0xBB] = ("","")
        self.hexcodes[0xCB] = ("","")
        self.hexcodes[0xDB] = ("","")
        self.hexcodes[0xEB] = ("","")
        self.hexcodes[0xFB] = ("","")

        self.hexcodes[0x0C] = ("tsb","absolute")
        self.hexcodes[0x1C] = ("trb","absolute")
        self.hexcodes[0x2C] = ("bit","absolute")
        self.hexcodes[0x3C] = ("bit","absolutex")
        self.hexcodes[0x4C] = ("jmp","absolute")
        self.hexcodes[0x5C] = ("","")
        self.hexcodes[0x6C] = ("jmp","absoluteindirect")
        self.hexcodes[0x7C] = ("jmp","absoluteindexedindirect")
        self.hexcodes[0x8C] = ("sty","absolute")
        self.hexcodes[0x9C] = ("stz","absolute")
        self.hexcodes[0xAC] = ("ldy","absolute")
        self.hexcodes[0xBC] = ("ldy","absolutex")
        self.hexcodes[0xCC] = ("cpy","absolute")
        self.hexcodes[0xDC] = ("","")
        self.hexcodes[0xEC] = ("cpx","absolute")
        self.hexcodes[0xFC] = ("","")
        
        self.hexcodes[0x0D] = ("ora","absolute")
        self.hexcodes[0x1D] = ("ora","absolutex")
        self.hexcodes[0x2D] = ("and","absolute")
        self.hexcodes[0x3D] = ("and","absolutex")
        self.hexcodes[0x4D] = ("eor","absolute")
        self.hexcodes[0x5D] = ("eor","absolutex")
        self.hexcodes[0x6D] = ("adc","absolute")
        self.hexcodes[0x7D] = ("adc","absolutex")
        self.hexcodes[0x8D] = ("sta","absolute")
        self.hexcodes[0x9D] = ("sta","absolutex")
        self.hexcodes[0xAD] = ("lda","absolute")
        self.hexcodes[0xBD] = ("lda","absolutex")
        self.hexcodes[0xCD] = ("cmp","absolute")
        self.hexcodes[0xDD] = ("cmp","absolutex")
        self.hexcodes[0xED] = ("sbc","absolute")
        self.hexcodes[0xFD] = ("sbc","absolutex")
        
        self.hexcodes[0x0E] = ("asl","absolute")
        self.hexcodes[0x1E] = ("asl","absolutex")
        self.hexcodes[0x2E] = ("rol","absolute")
        self.hexcodes[0x3E] = ("rol","absolutex")
        self.hexcodes[0x4E] = ("lsr","absolute")
        self.hexcodes[0x5E] = ("lsr","absolutex")
        self.hexcodes[0x6E] = ("ror","absolute")
        self.hexcodes[0x7E] = ("ror","absolutex")
        self.hexcodes[0x8E] = ("stx","absolute")
        self.hexcodes[0x9E] = ("stz","absolutex")
        self.hexcodes[0xAE] = ("ldx","absolute")
        self.hexcodes[0xBE] = ("ldx","absolutey")
        self.hexcodes[0xCE] = ("dec","absolute")
        self.hexcodes[0xDE] = ("dec","absolutex")
        self.hexcodes[0xEE] = ("inc","absolute")
        self.hexcodes[0xFE] = ("inc","absolutex")
        
        self.hexcodes[0x0F] = ("","")
        self.hexcodes[0x1F] = ("","")
        self.hexcodes[0x2F] = ("","")
        self.hexcodes[0x3F] = ("","")
        self.hexcodes[0x4F] = ("","")
        self.hexcodes[0x5F] = ("","")
        self.hexcodes[0x6F] = ("","")
        self.hexcodes[0x7F] = ("","")
        self.hexcodes[0x8F] = ("","")
        self.hexcodes[0x9F] = ("","")
        self.hexcodes[0xAF] = ("","")
        self.hexcodes[0xBF] = ("","")
        self.hexcodes[0xCF] = ("","")
        self.hexcodes[0xDF] = ("","")
        self.hexcodes[0xEF] = ("","")
        self.hexcodes[0xFF] = ("","")

    def reset(self):
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.sp = 0x0100
        lowaddr = self.object_code[0xfffc]
        highaddr = self.object_code[0xfffd]
        if (lowaddr != None) and (lowaddr > -1) and (highaddr != None) and (highaddr > -1):
            address = (lowaddr & 0xff) | ((highaddr << 8) & 0xff00)
            self.pc = address
            return True
        else:
            print("ERROR: Bad reset vector 0x"+str(self.object_code[0xfffc])+",0x"+str(self.object_code[0xfffd]))
            return False

    def nmi(self):
        # Read the NMI vector
        lowaddr = self.object_code[0xfffe]
        highaddr = self.object_code[0xffff]
        if (lowaddr != None) and (lowaddr > -1) and (highaddr != None) and (highaddr > -1):
            address = (lowaddr & 0xff) | ((highaddr << 8) & 0xff00)
        else:
            return False

        # push PC and status on stack
        self.object_code[self.sp] = ((self.pc >> 8) & 0xff)
        self.object_code[self.sp+1] = (self.pc & 0xff)
        self.object_code[self.sp+2] = self.cc | 0x20
        self.sp += 3

        # Set PC to the NMI vector
        self.pc = address
        return True

    def irq(self):
        # Read the IRQ vector
        lowaddr = self.object_code[0xfffa]
        highaddr = self.object_code[0xfffb]
        if (lowaddr != None) and (lowaddr > -1) and (highaddr != None) and (highaddr > -1):
            address = (lowaddr & 0xff) | ((highaddr << 8) & 0xff00)
        else:
            return False

        # push PC and status on stack
        self.object_code[self.sp] = ((self.pc >> 8) & 0xff)
        self.object_code[self.sp+1] = (self.pc & 0xff)
        self.object_code[self.sp+2] = self.cc
        self.sp += 3

        # Set PC to the NMI vector
        self.pc = address
        return True

    def make_flags_nz(self,result):
        # N Flag, bit 7
        if result & 0x80 == 0x80:
            self.cc = self.cc | 0x80
        else:
            self.cc = self.cc & 0x7f

        # Z 
        if result==0x00:
            self.cc = self.cc | 0x02
        else:
            self.cc = self.cc & 0xfd

    def make_flags_v(self, acc, operand, carryin, result, carryout):
        # V Flag, bit 6
        self.set_v(((acc^result) & (operand^result) & 0x80) == 0x80)

    def get_operand(self,addrmode,opcode,operand8,operand16):
        # Get the operand based on the address mode
        #print get operand addrmode="+str(addrmode)+" opcode:"+str(opcode)+" op8:"+str(operand8)
        if addrmode == "zeropageindexedindirectx":
            indirectaddr = operand8 + self.x
            addr = (self.object_code[indirectaddr+1] << 8) + self.object_code[indirectaddr]
            operand = self.object_code[addr]
            length = 2 
        elif addrmode == "zeropageindexedindirecty":
            indirectaddr = operand8
            addr = (self.object_code[indirectaddr+1] << 8) + self.object_code[indirectaddr]
            addr = addr + self.x
            operand = self.object_code[addr]
            length = 2           
        elif addrmode == "zeropageindirect":
            indirectaddr = operand8
            addr = (self.object_code[indirectaddr+1] << 8) + self.object_code[indirectaddr]
            operand = self.object_code[addr]
            length = 2  
        elif addrmode == "zeropage":
            addr = operand8
            operand = self.object_code[addr]
            length = 2
        elif addrmode == "zeropagex":
            addr = operand8 + self.x
            operand = self.object_code[addr]
            length = 2
        elif addrmode == "zeropagey":
            addr = operand8 + self.y
            operand = self.object_code[addr]
            length = 2
        elif addrmode == "immediate":
            addr = None
            operand = operand8
            length = 2
        elif addrmode == "absolutey":
            addr = operand16 + self.y
            operand = self.object_code[addr]
            length = 3
        elif addrmode == "absolute":
            addr = operand16
            operand = self.object_code[addr]
            length = 3
        elif addrmode == "absolutex":
            addr = operand16 + self.x
            operand = self.object_code[addr]
            length = 3
        elif addrmode == "indirect":
            indirectaddr = operand16
            addr = (self.object_code[addr+1] << 8) + self.object_code[addr]
            operand = self.object_code[addr] | (self.object_code[addr+1] << 8)
            length = 3
        elif addrmode == "accumulator":
            addr = None
            operand = self.a
            length = 1
        elif addrmode == "implicit":
            addr = None
            operand = operand8
            length = 2
        else:
            print "ERROR: Address mode %s not found" % addrmode
            print "     : PC = 0x%04x" % self.pc
            exit()
        return (operand,addr,length)

    def get_operand16(self,addrmode,opcode,operand8,operand16):
        # Get the operand based on the address mode
        if addrmode == "absolute":
            addr = operand16
            length = 3
        elif addrmode == "indirect":
            indirectaddr = operand16
            addr = (self.object_code[indirectaddr+1] << 8) + self.object_code[indirectaddr]
            length=3
        elif addrmode == "absoluteindexedindirect":
            indirectaddr = operand16+self.x
            addr = (self.object_code[indirectaddr+1] << 8) + self.object_code[indirectaddr]
            length=3
        elif addrmode == "absoluteindirect":
            indirectaddr = operand16
            addr = (self.object_code[indirectaddr+1] << 8) + self.object_code[indirectaddr]
            length=3
        else:
            print "ERROR: Address mode %s not found for JMP or JSR" % addrmode
            print "     : PC = 0x%04x" % self.pc
            exit()
        operand = self.object_code[addr]
        return (operand,addr,length)

    # Execute the instruction at the current program counter location.
    # Converts hex opcode to instruction three letter name and address mode
    # turns instruction name into a method - e.g.  instr_lda()
    # Then calls the method and passes in the operands

    def execute(self,address=None):
        if address==None:
            address = self.pc
        opcode = self.object_code[address]
        operand8 = self.object_code[(address+1)% 65536]
        hi = self.object_code[(address+2) % 65536] 
        operand16 = operand8 + ((hi << 8) & 0xff00)

        if (opcode >= 0) and (opcode < 256):
            instruction,addrmode = self.hexcodes[opcode]
            if (instruction != ""):
                methodname="instr_"+instruction
                #print "METHODNAME:"+methodname
                method = getattr(self, methodname, lambda: "nothing")         
                method(addrmode,opcode,operand8,operand16)
        else:
            print "ERROR: Out in the weeds. Opcode = %d" % opcode
    
    def none_or_byte(self,thebyte):
        if thebyte == None:
            thestr = "None"
        else:
            thestr = "0x%02x" % thebyte
        return thestr
        
    def show_state(self):
        str_pc = self.none_or_byte(self.pc)
        str_a  = self.none_or_byte(self.a)
        str_x  = self.none_or_byte(self.x)
        str_y  = self.none_or_byte(self.y)
        str_sp = self.none_or_byte(self.sp)
        str_cc = self.none_or_byte(self.cc)
        if (self.have_symbols) and (self.pc in self.labels):
            label = self.labels[self.pc]
            label = label.ljust(10)
            print label+" PC:"+str_pc+" A:"+str_a+" X:"+str_x+" Y:"+str_y+" SP:"+str_sp+" STATUS:"+str_cc

        else:
            print "           PC:"+str_pc+" A:"+str_a+" X:"+str_x+" Y:"+str_y+" SP:"+str_sp+" STATUS:"+str_cc

            
    # Utility routines to change the flags
    # So you don't need to remember the bit positions
    #
    
    # 7	        6	        5	    4	    3	    2	        1	    0
    # Negative	Overflow	(S)     Break	Decimal	Interrupt	Zero	Carry
    # N	        V	        -	    B	    D	    I	        Z	    C
    # -	        -	        -	    -	    -	    -	        -	    -

    def set_c(self,truth):
        if truth:
            self.cc = self.cc | 0x01
        else:
            self.cc = self.cc & 0xfe

    def set_z(self,truth):
        if truth:
            self.cc = self.cc | 0x02
        else:
            self.cc = self.cc & 0xfd

    def set_i(self,truth):
        if truth:
            self.cc = self.cc | 0x04
        else:
            self.cc = self.cc & 0xfb

    def set_d(self,truth):
        if truth:
            self.cc = self.cc | 0x08
        else:
            self.cc = self.cc & 0xf7

    def set_b(self,truth):
        if truth:
            self.cc = self.cc | 0x10
        else:
            self.cc = self.cc & 0xef

    def set_s(self,truth):
        if truth:
            self.cc = self.cc | 0x20
        else:
            self.cc = self.cc & 0xdf
                        
    def set_v(self,truth):
        if truth:
            self.cc = self.cc | 0x40
        else:
            self.cc = self.cc & 0xbf

    def set_n(self,truth):
        if truth:
            self.cc = self.cc | 0x80
        else:
            self.cc = self.cc & 0x7f

    def push(self,value):
        self.object_code[self.pc] = value
        self.pc -= 1
        
    def pushaddr(self,addr):
        low = addr & 0xff
        high = ((addr & 0xff00) >> 8) & 0xff
        self.object_code[self.pc] = high
        self.pc -= 1
        self.object_code[self.pc] = low
        self.pc -= 1

    def pull(self):
        self.pc +=1
        value = self.object_code[self.pc]
        return value
        
    def pulladdr(self):
        self.pc += 1
        low = self.object_code[self.pc]
        self.pc += 1
        high = self.object_code[self.pc]
        
        addr = low + (high << 8)
        return addr
                
    # Instruction ADC
    # 69 55    adc #$55      
    # 65 20    adc $20       
    # 75 20    adc $20,X     
    # 6D 33 22 adc $2233     
    # 7D 33 22 adc $2233,X   
    # 79 33 22 adc $2233,Y   
    # 61 20    adc ($20,X)   
    # 71 20    adc ($20),Y   
    # 72 20    adc ($20)
    def instr_adc(self,addrmode,opcode,operand8,operand16):
        carryin = 0
        if self.cc & 0x01 == 0x01 : # if carry set
            carryin = 1
        else:
            carryin = 0

        # Get the operand based on the address mode
        operand,addr,length = self.get_operand(addrmode, opcode, operand8, operand16)

        # Do the add
        # Compute the carry
        # Put the result in A
        # Compute the flags

        result = (self.a + operand + carryin)
        if result > 255:
            carryout = 1
            self.cc = self.cc | 0x01
        else:
            carryout = 0
            self.cc = self.cc & 0xfe

        result = result % 256

        acc = self.a
        self.a = result
        self.make_flags_nz(result)
        #self.make_flags_v(self.a, operand, carryin, result, carryout)
        self.set_v(((acc^result) & (operand^result) & 0x80) == 0x80)
        self.pc += length
 
    # Instruction AND
    # 29 55    and #$55      
    # 25 20    and $20       
    # 35 20    and $20,X     
    # 2D 33 22 and $2233     
    # 3D 33 22 and $2233,X   
    # 39 33 22 and $2233,Y   
    # 21 20    and ($20,X)   
    # 31 20    and ($20),Y   
    # 32 20    and ($20) 

    def instr_and(self,addrmode,opcode,operand8,operand16):
        # Get the operand based on the address mode
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)

        # Do the an
        # Put the result in A
        # Compute the flags

        result = (self.a & operand)

        self.a = result
        self.make_flags_nz(result)
        self.pc += length

    # Instruction ASL
    # 0A       asl A         
    # 06 20    asl $20       
    # 16 20    asl $20,X     
    # 0E 33 22 asl $2233     
    # 1E 33 22 asl $2233,X   
    def instr_asl(self,addrmode,opcode,operand8,operand16):
        if addrmode == "accumulator":
            result = self.a << 1
            if (self.a & 0x80) == 0x80:
                self.cc = self.cc | 0x1
            else:
                self.cc = self.cc | 0xfe
            self.a = result
            self.pc += 1
        else:
            # Get the operand based on the address mode
            operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
            result = operand << 1
            if (operand & 0x80) == 0x80:
                self.cc = self.cc | 0x1
            else:
                self.cc = self.cc | 0xfe

            self.object_code[addr] = result
            self.pc += length

    # Instruction BCC
    # 90 55    bcc $55        
    def instr_bcc(self,addrmode,opcode,operand8,operand16):
        if (self.cc & 0x01)==0:
            addr = (self.pc + operand8) % 256
            self.pc = addr
        else:
            self.pc += 2

    # Instruction BCS
    # B0 55    bcs $55       
    def instr_bcs(self,addrmode,opcode,operand8,operand16):
        if (self.cc & 0x01)==1:
            addr = (self.pc + operand8) % 256
            self.pc = addr
        else:
            self.pc += 2

    # Instruction BEQ
    # F0 55    beq $55     
    def instr_beq(self,addrmode,opcode,operand8,operand16):
        if (self.cc & 0x02)==0x2:
            addr = (self.pc + operand8) % 256
            self.pc = addr
        else:
            self.pc += 2

    # Instruction BIT
    # 89 55    bit #$55      
    # 24 20    bit $20       
    # 34 20    bit $20,X     
    # 2C 33 22 bit $2233     
    # 3C 33 22 bit $2233,X   
    def instr_bit(self,addrmode,opcode,operand8,operand16):
        # Get the operand, immediate or from memory
        if addrmode=="immediate":
            operand = operand8
            length = 2
        else:
            operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)

        # Do the test.
        test = self.a & operand
        self.set_z(test==0x00)
        
        # V is set to bit 6 of the operand
        self.set_v(operand & 0x40 == 0x40)
        self.pc += length

    # Instruction BMI
    # 30 55    bmi $55
    def instr_bmi(self,addrmode,opcode,operand8,operand16):
        if (self.cc & 0x80)==0x80:
            addr = (self.pc + operand8) % 256
            self.pc = addr
        else:
            self.pc += 2

    # Instruction BNE
    # D0 55    bne $55
    def instr_bne(self,addrmode,opcode,operand8,operand16):
        if (self.cc & 0x02)==0x00:
            addr = (self.pc + operand8) % 256
            self.pc = addr
        else:
            self.pc += 2

    # Instruction BPL
    # 10 55    bpl $55  
    def instr_bpl(self,addrmode,opcode,operand8,operand16):
        if (self.cc & 0x80)==0x00:
            addr = (self.pc + operand8) % 256
            self.pc = addr
        else:
            self.pc += 2

    # Instruction BRA
    # 80 55    bra $55  
    def instr_bra(self,addrmode,opcode,operand8,operand16):
        addr = (self.pc + operand8) % 256
        self.pc = addr
    
    # Instruction BRK
    # 00       brk  
    def instr_brk(self,addrmode,opcode,operand8,operand16):
        self.pushaddr(self.pc+3)
        self.push(self.cc)
        low = self.object_code[0xfffe]
        high = self.object_code[0xffff]
        self.pc = low+(high << 8)
        self.set_b(True)


    # Instruction BVC
    # 50 55    bvc $55       
    def instr_bvc(self,addrmode,opcode,operand8,operand16):
        if (self.cc & 0x40)==0x00:
            addr = (self.pc + operand8) % 256
            self.pc = addr
        else:
            self.pc += 2

    # Instruction BVS
    # 70 55    bvs $55 
    def instr_bvs(self,addrmode,opcode,operand8,operand16):
        if (self.cc & 0x40)==0x040:
            addr = (self.pc + operand8) % 256
            self.pc = addr
        else:
            self.pc += 2

    # Instruction CLC
    # 18        clc 
    def instr_clc(self,addrmode,opcode,operand8,operand16):
        self.set_c(False)
        self.pc += 1

    # Instruction CLD
    # D8        cld 
    def instr_cld(self,addrmode,opcode,operand8,operand16):
        self.set_d(False)
        self.pc += 1

    # Instruction CLI
    # 58        cli 
    def instr_cli(self,addrmode,opcode,operand8,operand16):
        self.set_i(False)
        self.pc += 1

    # Instruction CLV
    # 57        clv 
    def instr_clv(self,addrmode,opcode,operand8,operand16):
        self.set_v(False)
        self.pc += 1

    # Instruction CMP
    # C9 55    cmp #$55      
    # C5 20    cmp $20       
    # CD 33 22 cmp $2233     
    # DD 33 22 cmp $2233,X   
    # D9 33 22 cmp $2233,Y   
    # C1 20    cmp ($20,X)   
    # D1 20    cmp ($20),Y   
    # D2 20    cmp ($20)     
    def instr_cmp(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        test = (self.a - operand) % 256
        self.make_flags_nz(test)
        self.pc += length


    # Instruction CMP
    # E0 55    cpx #$55      
    # E4 20    cpx $20       
    # EC 33 22 cpx $2233     
    # C0 55    cpy #$55      
    # C4 20    cpy $20       
    # CC 33 22 cpy $2233 
    def instr_cpx(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        test = (self.a - operand) % 256
        self.make_flags_nz(test)
        self.pc += length
 
    # Instruction CPY
    # C0 55    cpy #$55      
    # C4 20    cpy $20       
    # CC 33 22 cpy $2233
    def instr_cpy(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        test = (self.y - operand) % 256
        self.make_flags_nz(test)
        self.pc += length

    # Instruction DEA aka DEC A
    # 3A       dea 
    def instr_dea(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        test = (self.a - 1) % 256
        self.make_flags_nz(test)
        self.pc += length

    # Instruction DEC
    # C6 20    dec $20       
    # D6 20    dec $20,X     
    # CE 33 22 dec $2233     
    # DE 33 22 dec $2233,X 
    def instr_dec(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        result = (operand - 1) % 256
        self.make_flags_nz(result)
        self.pc += length


    # Instruction DEX
    # CA       dex
    def instr_dex(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        result = (self.x - 1) % 256
        self.make_flags_nz(result)
        self.x = result
        self.pc += length
              
    # Instruction DEY
    # 88       dey 
    def instr_dex(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        result = (self.y - 1) % 256
        self.make_flags_nz(result)
        self.y = result
        self.pc += length

    # Instruction EOR
    # 49 55    eor #$55      
    # 45 20    eor $20       
    # 55 20    eor $20,X     
    # 4D 33 22 eor $2233     
    # 5D 33 22 eor $2233,X   
    # 59 33 22 eor $2233,Y   
    # 41 20    eor ($20,X)   
    # 51 20    eor ($20),Y   
    # 52 20    eor ($20)   
    def instr_eor(self,addrmode,opcode,operand8,operand16):
        # Get the operand based on the address mode
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)

        # Do the an
        # Put the result in A
        # Compute the flags

        result = (self.a ^ operand)

        self.a = result
        self.make_flags_nz(result)
        self.pc += length

    # Instruction INA aka INC A
    # 1A       ina
    def instr_ina(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        test = (self.a + 1) % 256
        self.make_flags_nz(test)
        self.pc += length

    # Instruction INC
    # E6 20    inc $20       
    # F6 20    inc $20,X     
    # EE 33 22 inc $2233     
    # FE 33 22 inc $2233,X
    def instr_inc(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        result = (operand + 1) % 256
        self.make_flags_nz(result)
        self.pc += length
 
    # Instruction INX
    # E8       inx
    def instr_inx(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        result = (self.x + 1) % 256
        self.make_flags_nz(result)
        self.x = result
        self.pc += length
              
    # Instruction INY
    # C8       iny 
    def instr_iny(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        result = (self.y + 1) % 256
        self.make_flags_nz(result)
        self.y = result
        self.pc += length

    # Instruction JMP
    # 4C 33 22 jmp $2233     
    # 6C 33 22 jmp ($2233)   
    # 7C 33 22 jmp ($2233,X) 
    def instr_jmp(self,addrmode,opcode,operand8,operand16):
        #print "INSTR_JMP CALLED addrmode = %s opcode=%02x operand8=%02x operand16=%04x" % (addrmode,opcode,operand8,operand16)
        operand,addr,length = self.get_operand16(addrmode,opcode,operand8,operand16)
        #print "INSTR_JMP operand   = %04x addr=%04x length=%d" % (operand,addr, length)
        #print "INSTR_JMP operand16 = %04x " % operand16
        self.pc = addr    
    
    # Instruction JSR
    # 20 33 22 jsr $2233     
    def instr_jsr(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand16(addrmode,opcode,operand8,operand16)
        self.pushaddr(self.pc + 3)
        self.pc = operand      

    # Instruction LDA
    # A9 55    lda #$55      
    # A5 20    lda $20       
    # B5 20    lda $20,X     
    # AD 33 22 lda $2233     
    # BD 33 22 lda $2233,X   
    # B9 33 22 lda $2233,Y   
    # A1 20    lda ($20,X)   
    # B1 20    lda ($20),Y   
    # B2 20    lda ($20)    
    def instr_lda(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        #print "LDA : addrmode:"+str(addrmode)+" operand:"+str(operand)+" operand8 "+str(operand8)
        self.a = operand
        self.pc += length

    # Instruction LDX
    # A9 55    lda #$55      
    # A2 55    ldx #$55      
    # A6 20    ldx $20       
    # B6 20    ldx $20,Y     
    # AE 33 22 ldx $2233     
    # BE 33 22 ldx $2233,Y 
    def instr_ldx(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        self.x = operand
        self.pc += length

    # Instruction LDY
    # A0 55    ldy #$55      
    # A4 20    ldy $20       
    # B4 20    ldy $20,X     
    # AC 33 22 ldy $2233     
    # BC 33 22 ldy $2233,X   
    def instr_ldy(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        self.y = operand
        self.pc += length

    # Instruction LSR
    # 4A       lsr A         
    # 46 20    lsr $20       
    # 56 20    lsr $20,X     
    # 4E 33 22 lsr $2233     
    # 5E 33 22 lsr $2233,X
    def instr_lsr(self,addrmode,opcode,operand8,operand16):
        if (addrmode=="accumulator"):
            result = self.a >> 1
            self.pc += 1
        else:
            operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
            result = (operand >> 1) % 256
            self.pc += length
        self.a = result
        self.make_flags_nz(result)

    # Instruction LSR
    # EA       nop
    def instr_nop(self,addrmode,opcode,operand8,operand16):
        self.pc += 1

    # Instruction ORA
    # 09 55    ora #$55      
    # 05 20    ora $20       
    # 15 20    ora $20,X     
    # 0D 33 22 ora $2233     
    # 1D 33 22 ora $2233,X   
    # 19 33 22 ora $2233,Y   
    # 01 20    ora ($20,X)   
    # 11 20    ora ($20),Y   
    # 12 20    ora ($20)
    def instr_ora(self,addrmode,opcode,operand8,operand16):
        operand,addr,length =self.get_operand(addrmode,opcode,operand8,operand16)
        result = (operand | self.a)
        self.a = result
        self.make_flags_nz(result)
        self.pc += length

    # Instruction PHA and other Pxx stack instructions
    # 08       php
    # 28       plp
    # 48       pha    
    # DA       phx           
    # 5A       phy           
    # 68       pla           
    # FA       plx           
    # 7A       ply
    def instr_php(self,addrmode,opcode,operand8,operand16):
        self.object_code[0x100+self.sp] = self.cc
        self.sp = (self.sp - 1 ) % 256
        self.pc += 1
    def instr_pha(self,addrmode,opcode,operand8,operand16):
        self.object_code[0x100+self.sp] = self.a
        self.sp = (self.sp - 1 ) % 256
        self.pc += 1
    def instr_phx(self,addrmode,opcode,operand8,operand16):
        self.object_code[0x100+self.sp] = self.x
        self.sp = (self.sp - 1 ) % 256
        self.pc += 1
    def instr_phy(self,addrmode,opcode,operand8,operand16):
        self.object_code[0x100+self.sp] = self.y
        self.sp = (self.sp - 1 ) % 256
        self.pc += 1
    def instr_plp(self,addrmode,opcode,operand8,operand16):
        self.sp = (self.sp + 1 ) % 256
        self.cc = self.object_code[0x100+self.sp]
        self.pc += 1
    def instr_pla(self,addrmode,opcode,operand8,operand16):
        self.sp = (self.sp + 1 ) % 256
        self.a = self.object_code[0x100+self.sp]
        self.pc += 1
    def instr_plx(self,addrmode,opcode,operand8,operand16):
        self.sp = (self.sp + 1 ) % 256
        self.x = self.object_code[0x100+self.sp]
        self.pc += 1
    def instr_ply(self,addrmode,opcode,operand8,operand16):
        self.sp = (self.sp + 1 ) % 256
        self.y = self.object_code[0x100+self.sp]
        self.pc += 1

    # Instruction ROL
    # 2A       rol A         
    # 26 20    rol $20       
    # 36 20    rol $20,X     
    # 2E 33 22 rol $2233     
    # 3E 33 22 rol $2233,X
    def instr_rol(self,addrmode,opcode,operand8,operand16):
        if (addrmode=="accumulator"):
            if ((self.a & 0x80) == 0x80):
                carryout = True
            else:
                carryout = False
            if ((self.cc & 0x01) == 0x01):
                carryin = 0x01
            else:
                carryin = 0x01
            result = ((self.a << 1) % 256) | carryin
            self.a = result
            self.set_c(carryin)
            self.pc += 1
        else:
            operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
            if ((operand & 0x80) == 0x80):
                carryout = True
            else:
                carryout = False
                
            if ((self.cc & 0x01) == 0x01):
                carryin = 0x01
            else:
                carryin = 0x01
                
            result = ((operand << 1) % 256) | carryin
            self.set_c(carryout)
            self.object_code[addr] = result
            self.pc += length
        self.make_flags_nz(result)   

    # Instruction ROR
    # 6A       ror A         
    # 66 20    ror $20       
    # 76 20    ror $20,X     
    # 6E 33 22 ror $2233     
    # 7E 33 22 ror $2233,X   
    def instr_ror(self,addrmode,opcode,operand8,operand16):
        if (addrmode=="accumulator"):
            if ((self.cc & 0x01) == 0x01):
                carry = 0x80
            else:
                carry = 0
                
            if ((self.a & 0x01) == 0x01):
                carryout = True
            else:
                carryout = False
            result = (self.a >> 1) | carry
            self.a = result
            self.set_c(carryout)
            self.pc += 1
        else:
            operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
            if ((self.cc & 0x01) == 0x01):
                carry = 0x80
            else:
                carry = 0
                
            if ((operand & 0x01) == 0x01):
                carryout = True
            else:
                carryout = False
            result = ((operand >> 1) % 256) | carry
            self.object_code[addr]=result
            self.set_c(carryout)
            self.pc += length
        self.make_flags_nz(result)   

    # Instruction RTI
    # 40       rti  
    def instr_rti(self,addrmode,opcode,operand8,operand16):
        self.cc = self.pull()
        self.pc = self.pulladdr()
        self.set_i(False)
        
    # Instruction RTS
    # 60       rts
    def instr_rti(self,addrmode,opcode,operand8,operand16):
        self.pc = self.pulladdr()        

    # Instruction SBC
    # E9 55    sbc #$55      
    # E5 20    sbc $20       
    # F5 20    sbc $20,X     
    # ED 33 22 sbc $2233     
    # FD 33 22 sbc $2233,X   
    # F9 33 22 sbc $2233,Y   
    # E1 20    sbc ($20,X)   
    # F1 20    sbc ($20),Y   
    # F2 20    sbc ($20)
    def instr_sbc(self,addrmode,opcode,operand8,operand16):
        if self.cc & 0x01 == 0x01 : # if carry set
            carryin = 1
        else:
            carryin = 0
        # Get the operand based on the address mode
        operand,addr,length = self.get_operand(addrmode, opcode,operand8, operand16)

        # Do the subtract
        # Compute the carry
        # Put the result in A
        # Compute the flags

        result = (self.a - operand - carryin)
        if result < 0:
            carryout = 1
            self.cc = self.cc | 0x01
        else:
            carryout = 0
            self.cc = self.cc & 0xfe

        result = result % 256

        self.a = result
        self.make_flags_nz(result)
        self.make_flags_v(self.a, operand, carryin, result, carryout)
        self.pc += length
    
    # Instruction SEC    
    # 38       sec
    def instr_sec(self,addrmode,opcode,operand8,operand16):
        self.set_c(True)
        self.pc += 1
    
    # Instruction SED    
    # F8       sed
    def instr_sed(self,addrmode,opcode,operand8,operand16):
        self.set_d(True)
        self.pc += 1    
    
    # Instruction SEI
    # 78       sei
    def instr_sei(self,addrmode,opcode,operand8,operand16):
        self.set_i(True)
        self.pc += 1
    
    # Instruction STA
    # 85 20    sta $20       
    # 95 20    sta $20,X     
    # 8D 33 22 sta $2233     
    # 9D 33 22 sta $2233,X   
    # 99 33 22 sta $2233,Y   
    # 81 20    sta ($20,X)   
    # 91 20    sta ($20),Y   
    # 92 20    sta ($20)
    def instr_sta(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        self.object_code[addr] = self.a
        self.pc += length

    # Instruction STX
    # 86 20    stx $20       
    # 96 20    stx $20,Y     
    # 8E 33 22 stx $2233
    def instr_stx(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        self.object_code[addr] = self.x
        self.pc += length
        
    # Instruction STY
    # 84 20    sty $20       
    # 94 20    sty $20,X     
    # 8C 33 22 sty $2233 
    def instr_sty(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        self.object_code[addr] = self.y
        self.pc += length

    # Instruction STZ
    # 64 20    stz $20       
    # 74 20    stz $20,X     
    # 9C 33 22 stz $2233     
    # 9E 33 22 stz $2233,X 
    def instr_stz(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        self.object_code[addr] = 0x00
        self.pc += length
    
    # Instruction TAX    
    # AA       tax
    def instr_tax(self,addrmode,opcode,operand8,operand16):
        self.x = self.a
        self.pc += 1
        
    # Instruction TAY
    # A8       tay
    def instr_tay(self,addrmode,opcode,operand8,operand16):
        self.y = self.a
        self.pc += 1
        
    # Instruction TRB
    # 14 20    trb $20       
    # 1C 33 22 trb $2233     
    # 04 20    tsb $20       
    # 0C 33 22 tsb $2233
    def instr_trb(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        result = operand & (self.a ^ 0xff)
        self.object_code[addr]=result
        self.set_z((operand & self.a) == 0x00)
        self.pc += length

    def instr_tsb(self,addrmode,opcode,operand8,operand16):
        operand,addr,length = self.get_operand(addrmode,opcode,operand8,operand16)
        result = operand + self.a
        self.object_code[addr]=result
        self.set_z((operand & self.a) == 0x00)
        self.pc += length
 
    # BA       tsx  
    def instr_tsx(self,addrmode,opcode,operand8,operand16):
        self.x = self.sp
        self.pc += 1    
        
    # 8A       txa     
    def instr_txa(self,addrmode,opcode,operand8,operand16):
        self.a = self.x
        self.pc += 1   
        
    # 9A       txs      
    def instr_txs(self,addrmode,opcode,operand8,operand16):
        self.sp = self.x
        self.pc += 1
        
    # 98       tya
    def instr_tya(self,addrmode,opcode,operand8,operand16):
        self.a = self.y
        self.pc += 1    

