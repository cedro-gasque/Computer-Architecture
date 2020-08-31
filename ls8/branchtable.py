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

def JEQ(cpu, register):
    cpu.PC = (cpu.PC + 2) * (cpu.FL & 0x01 ^ 0x01) + cpu.REG[register] * (cpu.FL & 0x01)

def JNE(cpu, register):
    cpu.PC = (cpu.PC + 2) * (cpu.FL & 0x01) + cpu.REG[register] * (cpu.FL & 0x01 ^ 0x01)

def JLT(cpu, register):
    cpu.PC = (cpu.PC + 2) * ((cpu.FL >> 2) & 0x01 ^ 0x01) + cpu.REG[register] * ((cpu.FL >> 2) & 0x01)

def JGT(cpu, register):
    cpu.PC = (cpu.PC + 2) * ((cpu.FL >> 1) & 0x01 ^ 0x01) + cpu.REG[register] * ((cpu.FL >> 1) & 0x01)

def INC(cpu, register):
    cpu.REG[register] += 1
    cpu.REG[register] &= 0xFF

def NOT(cpu, register):
    cpu.REG[register] = ~cpu.REG[register] & 0xFF

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
    cpu.REG[registerA] -= cpu.REG[registerB]
    cpu.REG[registerA] &= 0xFF

def MUL(cpu, registerA, registerB):
    cpu.REG[registerA] *= cpu.REG[registerB]
    cpu.REG[registerA] &= 0xFF

def MOD(cpu, registerA, registerB):
    cpu.REG[registerA] %= cpu.REG[registerB]
    cpu.REG[registerA] &= 0xFF

def CMP(cpu, registerA, registerB):
    cpu.FL &= 0x00
    cpu.FL |= (cpu.REG[registerA] < cpu.REG[registerB]) * 0x04
    cpu.FL |= (cpu.REG[registerA] > cpu.REG[registerB]) * 0x02
    cpu.FL |= (cpu.REG[registerA] == cpu.REG[registerB]) * 0x01

def AND(cpu, registerA, registerB):
    cpu.REG[registerA] &= cpu.REG[registerB]

def OR(cpu, registerA, registerB):
    cpu.REG[registerA] |= cpu.REG[registerB]

def XOR(cpu, registerA, registerB):
    cpu.REG[registerA] ^= cpu.REG[registerB]

def SHL(cpu, registerA, registerB):
    cpu.REG[registerA] <<= cpu.REG[registerB]
    cpu.REG[registerA] &= 0xFF

def SHR(cpu, registerA, registerB):
    cpu.REG[registerA] >>= cpu.REG[registerB]
    cpu.REG[registerA] &= 0xFF

# EXTENSION INSTRUCTIONS
def ADDI(cpu, register, immediate):
    cpu.REG[register] += immediate
    cpu.REG[register] &= 0xFF

branchtable = {
    0x11: RET,
    0x13: IRET,
    0x45: PUSH,
    0x46: POP,
    0x47: PRN,
    0x48: PRA,
    0x50: CALL,
    0x54: JMP,
    0x55: JEQ,
    0x56: JNE,
    0x57: JGT,
    0x58: JLT,
    0x82: LDI,
    0x83: LD,
    0x84: ST
}

ALU = {
    0x65: INC,
    0x69: NOT,
    0xA0: ADD,
    0xA2: MUL,
    0xA4: MOD,
    0xA7: CMP,
    0xA8: AND,
    0xAA: OR,
    0xAB: XOR,
    0xAC: SHL,
    0xAD: SHR,
    0xAE: ADDI
}
