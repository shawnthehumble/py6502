#!/usr/bin/env python

import asm6502
import sim6502
import dis6502

def go(debug=0):  
    lines = list()
    lines.append("       org $0000")
    lines.append("    JMP overthere ")
    lines.append("bhaddr:    dw &brkhandler,$0102,&another,&labels ; insert address for brkhandler")
    lines.append("l8addr:    dw &land8")
    lines.append("overthere:	      ")
    lines.append("    LDA bhaddr ")
    lines.append("    LDX 1 ")
    lines.append("    STA $FFFE ")
    lines.append("    LDA bhaddr,x ")
    lines.append("    STA $FFFF ")
    lines.append("    LDA #$10 ")
    lines.append("    ADC #$55	    ")
    lines.append("    ADC $20	        ")
    lines.append("    ADC $20,X	    ")
    lines.append("    ADC $0002	        ")
    lines.append("    ADC $0010,X	    ")
    lines.append("    ADC $0008,Y	    ")
    lines.append("    ADC ($20,X)	    ")
    lines.append("    ADC ($20),Y	    ")
    lines.append("another:   ADC ($20)	    ")
    lines.append("    AND #$55	    ")
    lines.append("    AND $20	        ")
    lines.append("    AND $20,X	    ")
    lines.append("    AND $0004	        ")
    lines.append("labels:	        ")
    lines.append("    AND $0010,X	    ")
    lines.append("    AND $0012,Y	    ")
    lines.append("    AND ($20,X)	    ")
    lines.append("    AND ($20),Y	    ")
    lines.append("    AND ($20)	    ")
    lines.append("    ASL A	        ")
    lines.append("    ASL $20	        ")
    lines.append("    ASL $20,X	    ")
    lines.append("    ASL $2233	        ")
    lines.append("    ASL $2233,X	    	    ")
    lines.append("    CLC ")
    lines.append("    BCC land1	    ")
    lines.append("    CLC ")
    lines.append("land1:	        ")
    lines.append("    SEC ")
    lines.append("    BCS land2	    ")
    lines.append("land2:	        ")
    lines.append("    BEQ land3	    ")
    lines.append("land3: ")
    lines.append("    BIT #$55	    ")
    lines.append("    BIT $20	    ")
    lines.append("    BIT $20,X	    ")
    lines.append("    BIT $2233	    ")
    lines.append("    BIT $2233,X	    ")
    lines.append("    BMI land4	    ")
    lines.append("land4: ")
    lines.append("    BNE land5	    ")
    lines.append("land5: ")
    lines.append("    BPL land6	    ")
    lines.append("land6: ")
    lines.append("    BRA land7	    ")
    lines.append("land7: ")
    lines.append("    LDA l8addr")
    lines.append("    STA $fffe")
    lines.append("    LDX #$01")
    lines.append("    LDA l8addr,x")
    lines.append("    STA $ffff")
    lines.append("    BRK	            ")
    lines.append("    BVC land8	    ")
    lines.append("land8: ")
    lines.append("    BVS land9	    ")
    lines.append("land9: ")
    lines.append("    CLC	            ")
    lines.append("    CLD	            ")
    lines.append("    CLI	            ")
    lines.append("    CLV	            ")
    lines.append("    CMP #$55	    ")
    lines.append("    CMP $20	        ")
    lines.append("    CMP $20	        ")
    lines.append("    CMP $2233	        ")
    lines.append("    CMP $2233,X	    ")
    lines.append("    CMP $2233,Y	    ")
    lines.append("    CMP ($20,X)	    ")
    lines.append("    CMP ($20),Y	    ")
    lines.append("    CMP ($20)	    ")
    lines.append("    CPX #$55	    ")
    lines.append("    CPX $20	        ")
    lines.append("    CPX $2233	        ")
    lines.append("    CPY #$55	    ")
    lines.append("    CPY $20	        ")
    lines.append("    CPY $2233	        ")
    lines.append("    DEA	            ")
    lines.append("    DEC A	            ")
    lines.append("    DEC $20	        ")
    lines.append("    DEC $20,X	    ")
    lines.append("    DEC $2233	        ")
    lines.append("    DEC $2233,X	    ")
    lines.append("    DEX	            ")
    lines.append("    DEY	            ")
    lines.append("    EOR #$55	    ")
    lines.append("    EOR $20	        ")
    lines.append("    EOR $20,X	    ")
    lines.append("    EOR $2233	        ")
    lines.append("    EOR $2233,X	    ")
    lines.append("    EOR $2233,Y	    ")
    lines.append("    EOR ($20,X)	    ")
    lines.append("    EOR ($20),Y	    ")
    lines.append("    EOR ($20)	    ")
    lines.append("    INA")
    lines.append("    INC A	            ")
    lines.append("    INC $20	        ")
    lines.append("    INC $20,X	    ")
    lines.append("    INC $2233	        ")
    lines.append("    INC $2233,X	    ")
    lines.append("    INX	            ")
    lines.append("    INY	            ")
    lines.append("    JMP jmp1	        ")
    lines.append("jmpa: dw &jmp2 ")
    lines.append("      dw &jmp3 ")
    lines.append("jmp1:")
    lines.append("    JMP (jmpa)	    ")
    lines.append("jmp2:")
    lines.append("    ldx #$02 ")
    lines.append("    JMP (jmpa,X)	    ")
    lines.append("jmp3:")
    lines.append("    JSR jsrhandler    ")
    lines.append("    LDA #$55	    ")
    lines.append("    LDA $20	        ")
    lines.append("    LDA $20,X	    ")
    lines.append("    LDA $2233	        ")
    lines.append("    LDA $2233,X	    ")
    lines.append("    LDA $2233,Y	    ")
    lines.append("    LDA ($20,X)	    ")
    lines.append("    LDA ($20),Y	    ")
    lines.append("    LDA ($20)	    ")
    lines.append("    LDX #$55	    ")
    lines.append("    LDX $20	        ")
    lines.append("    LDX $20,Y	    ")
    lines.append("    LDX $2233	        ")
    lines.append("    LDX $2233,Y	    ")
    lines.append("    LDY #$55	    ")
    lines.append("    LDY $20	        ")
    lines.append("    LDY $20,X	    ")
    lines.append("    LDY $2233	        ")
    lines.append("    LDY $2233,X	    ")
    lines.append("    LSR A	            ")
    lines.append("    LSR $20	        ")
    lines.append("    LSR $20,X	        ")
    lines.append("    LSR $2233	        ")
    lines.append("    LSR $2233,X	    ")
    lines.append("    NOP	            ")
    lines.append("    ORA #$55	        ")
    lines.append("    ORA $20	        ")
    lines.append("    ORA $20,X	        ")
    lines.append("    ORA $2233	        ")
    lines.append("    ORA $2233,X	    ")
    lines.append("    ORA $2233,Y	    ")
    lines.append("    ORA ($20,X)	    ")
    lines.append("    ORA ($20),Y	    ")
    lines.append("    ORA ($20)	        ")
    lines.append("    PHA	            ")
    lines.append("    PHP               ")
    lines.append("    PLP               ")
    lines.append("    PLX	            ")
    lines.append("    PLY	            ")
    lines.append("    ROL A	            ")
    lines.append("    ROL $20	        ")
    lines.append("    ROL $20,X	        ")
    lines.append("    ROL $2233	        ")
    lines.append("    ROL $2233,X	    ")
    lines.append("    ROR A	            ")
    lines.append("    ROR $20	        ")
    lines.append("    ROR $20,X	        ")
    lines.append("    ROR $2233	        ")
    lines.append("    ROR $2233,X	    ")
    #lines.append("    RTI	            ")
    #lines.append("    RTS	            ")
    lines.append("    SBC #$55	        ")
    lines.append("    SBC $20 	        ")
    lines.append("    SBC $20,X	        ")
    lines.append("    SBC $2233	        ")
    lines.append("    SBC $2233,X	    ")
    lines.append("    SBC $2233,Y	    ")
    lines.append("    SBC ($20,X)	    ")
    lines.append("    SBC ($20),Y	    ")
    lines.append("    SBC ($20)	        ")
    lines.append("    SEC	            ")
    lines.append("    SED	            ")
    lines.append("    SEI	            ")
    lines.append("    STA $20	        ")
    lines.append("    STA $20,X	    ")
    lines.append("    STA $2233	        ")
    lines.append("    STA $2233,X	    ")
    lines.append("    STA $2233,Y	    ")
    lines.append("    STA ($20,X)	    ")
    lines.append("    STA ($20),Y	    ")
    lines.append("    STA ($20)	    ")
    lines.append("    STX $20	        ")
    lines.append("    STX $20,Y	    ")
    lines.append("    STX $2233	        ")
    lines.append("    STY $20	        ")
    lines.append("    STY $20,X	    ")
    lines.append("    STY $2233	        ")
    lines.append("    STZ $20	        ")
    lines.append("    STZ $20,X	    ")
    lines.append("    STZ $2233	        ")
    lines.append("    STZ $2233,X	    ")
    lines.append("    TAX	            ")
    lines.append("    TAY	            ")
    lines.append("    TRB $20	        ")
    lines.append("    TRB $2233	        ")
    lines.append("    TSB $20	        ")
    lines.append("    TSB $2233	        ")
    lines.append("    TSX	            ")
    lines.append("    TXA	            ")
    lines.append("    TXS	            ")
    lines.append("    TYA")
    lines.append("; A remark")
    lines.append("    JMP $1000 ")
    lines.append("jsrhandler:")
    lines.append("    nop")
    lines.append("    nop")
    lines.append("    rts")
    lines.append("brkhandler: ")
    lines.append("    NOP ")
    lines.append("    NOP ")
    lines.append("    RTI ")
    
    lines.append("    ORG $1000")
    lines.append("start: lda #$50")
    lines.append("       sta $5000 ; blah")
    lines.append("       sta $25")
    lines.append("       clc")
    lines.append("       ROR A")
    lines.append("       adc #%10011010")
    lines.append("       sta %0101101000111100")
    lines.append("       sta %00111100")
    lines.append("       lda ($20)")
    lines.append("       adc $10,x")
    lines.append("middle:ldx $20,y")
    lines.append("       adc $3000,x")
    lines.append("       adc $3000,y")
    lines.append("       adc ($40,x) ")
    lines.append("       adc ($40),y")
    lines.append("       jmp $2000")
    lines.append("       nop")
    lines.append("       nop")
    lines.append("label:")
    lines.append("       nop")
    lines.append("       org $2000")
    lines.append("vals:  db @10,$aa,8,$cc,$dd")
    lines.append("       be")
    lines.append("       dw $1020,$3040")
    lines.append("       le")
    lines.append("       dw $1020,$3040")
    lines.append("       ddw $1020,$3040")
    lines.append("       dqw $1020,$3040")
    lines.append("       adc start")
    lines.append("       adc ($40)")
    lines.append("end:   bpl vals")
    lines.append("       db $aa,$bb,$cc,$dd")
    lines.append("       nop")
    lines.append("       org $fffc")
    lines.append("       db $00,$00")


    # Instantiate the assembler, assemble the code, grab the object_code
    a = asm6502.asm6502(debug=debug)
    a.assemble(lines)
    object_code = a.object_code[:]

    # Output IntelHex
    print "IntelHex"
    a.print_intelhex()

    #instantiate the simulator
    s = sim6502.sim6502(object_code, symbols=a.symbols)

    # Instantiate the disassembler
    d = dis6502.dis6502(object_code, symbols=a.symbols)

    # How much space to accomodate the disassembly
    status_indent = 39

    # Reset the state of the simulator
    s.reset()

    print
    print "SIMULATION START"
    print
    # Print a header for the simulator/disassembler output
    print ("LABEL      " + "ADDR HEX      INSTR").ljust(status_indent)+" PC   A  X  Y  SP   Status"

    # Print the initial state
    print " ".ljust(status_indent) + " %04x %02x %02x %02x %04x %02x" % (s.pc,s.a,s.x,s.y,s.sp,s.cc)

    # Execute 200 instructions
    for i in xrange(200):
        # Disassemble the current instruction
        distxt = d.disassemble_line(s.pc)

        # Execute that instruction
        s.execute()

        # Print out the disassembled instruction followed by the simulator state
        print distxt.ljust(status_indent) + " %04x %02x %02x %02x %04x %02x" % (s.pc,s.a,s.x,s.y,s.sp,s.cc)

go()

    
