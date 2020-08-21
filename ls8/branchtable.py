import sys

def RET(cpu):
    cpu.PC = cpu.RAM[cpu.REG[0x07]]
    cpu.REG[0x07] += 1

def IRET(cpu):
    for i in range(7):
        POP(cpu, 6 - i)
    cpu.FL = cpu.RAM[cpu.REG[0x07]]
    cpu.REG[0x07] += 1
    RET(cpu)
    cpu.INT = False

def PUSH(cpu, register):
    cpu.REG[0x07] -= 1
    cpu.RAM[cpu.REG[0x07]] = cpu.REG[register]

def POP(cpu, register):
    cpu.REG[register] = cpu.RAM[cpu.REG[0x07]]
    cpu.REG[0x07] += 1

def PRN(cpu, register):
    print(cpu.REG[register])

def PRA(cpu, register):
    print('\n' * (cpu.REG[register] == 13), end=chr(cpu.REG[register]), flush=True)

def CALL(cpu, register):
    cpu.REG[0x07] -= 1
    cpu.RAM[cpu.REG[0x07]] = cpu.PC + 2
    cpu.PC = cpu.REG[register]

def JMP(cpu, register):
    cpu.PC = cpu.REG[register]

def JLT(cpu, register):
    cpu.PC = (cpu.PC + 2) * ((cpu.FL >> 2) & 0x01 ^ 0x01) + cpu.REG[register] * ((cpu.FL >> 2) & 0x01)

def JGT(cpu, register):
    cpu.PC = cpu.PC + 2 if cpu.FL & 0x02 == 0 else cpu.REG[register]

def INC(cpu, register):
    cpu.REG[register] += 1
    cpu.REG[register] &= 0xFF

def LDI(cpu, register, immediate):
    cpu.REG[register] = immediate

def LD(cpu, registerA, registerB):
    cpu.REG[registerA] = cpu.RAM[cpu.REG[registerB]]

def ST(cpu, registerA, registerB):
    cpu.RAM[cpu.REG[registerA]] = cpu.REG[registerB]

def ADD(cpu, registerA, registerB):
    cpu.REG[registerA] += cpu.REG[registerB]
    cpu.REG[registerA] &= 0xFF

def SUB(cpu, registerA, registerB):
    pass

def MUL(cpu, registerA, registerB):
    cpu.REG[registerA] *= cpu.REG[registerB]
    cpu.REG[registerA] &= 0xFF

def CMP(cpu, registerA, registerB):
    cpu.FL &= 0x00
    cpu.FL |= (cpu.REG[registerA] < cpu.REG[registerB]) * 0x04
    cpu.FL |= (cpu.REG[registerA] > cpu.REG[registerB]) * 0x02
    cpu.FL |= (cpu.REG[registerA] == cpu.REG[registerB]) * 0x01

def SHL(cpu, registerA, registerB):
    cpu.REG[registerA] <<= cpu.REG[registerB]
    cpu.REG[registerA] &= 0xFF

branchtable = {
    0x11: RET,
    0x13: IRET,
    0x45: PUSH,
    0x46: POP,
    0x47: PRN,
    0x48: PRA,
    0x50: CALL,
    0x54: JMP,
    0x57: JGT,
    0x58: JLT,
    0x82: LDI,
    0x83: LD,
    0x84: ST
}

ALU = {
    0x65: INC,
    0xA0: ADD,
    0xA2: MUL,
    0xA7: CMP,
    0xAC: SHL
}
