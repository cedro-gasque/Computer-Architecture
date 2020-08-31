    LDI R0,0x06
    LDI R1,0x00
    LDI R2,0x01
    LDI R3,0x00
    LDI R4,Loop

Loop:
    LDI R3,0x00
    PUSH R4
    PUSH R0
    LDI R0,0x2A
    LDI R4,Print
    CALL R4
    POP R0
    INC R1
    LDI R4,End
    CMP R1,R0
    JGT R4
    LDI R4,0x0D
    PRA R4
    LDI R4,0x01
    SHL R2,R4
    POP R4
    JMP R4

Print:
    PRA R0
    INC R3
    CMP R3,R2
    JLT R4
    RET

End:
    HLT
