"""CPU functionality."""

import sys
import msvcrt
from datetime import datetime
from branchtable import branchtable, ALU

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0x00] * 0xFF
        self.PC = 0x00
        self.REG = [0x00] * 0x07 + [0xF4]
        self.FL = 0x00
        self.INT = False
        self.branchtable = branchtable
        self.ALU = ALU

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) < 2:
            print("Error: No program path given.")
            raise ValueError()
        address = 0
        with open(sys.argv[1], 'r') as f:
            program = []
            for line in f.read().split("\n"):
                if line.strip() != "" and line.strip()[0] != "#":
                    program.append(int(line.split(" ")[0], 2))
        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.RAM[address] = instruction
        #     address += 1
        self.RAM[:len(program)] = program

    def ram_read(self, MAR):
        return self.RAM[MAR]

    def ram_write(self, MAR, MDR):
        self.RAM[MAR] = MDR & 0xFF

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.REG[reg_a] += self.REG[reg_b]
        elif op == "SUB":
            pass
        elif op == "MUL":
            self.REG[reg_a] *= self.REG[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        self.REG[reg_a] &= 0xFF

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X %02X | %02X %02X %02X |" % (
            self.PC,
            self.FL,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.REG[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        last = datetime.now().second
        while True:
            key = msvcrt.kbhit()
            if key:
                self.RAM[0xF4] = ord(msvcrt.getch())
                self.REG[0x06] |= 0x02

            if self.REG[0x05] & 0x01 and datetime.now().second > last:
                last = datetime.now().second
                self.REG[0x06] |= 0x01

            if self.REG[0x05] > 0 and not self.INT:
                maskedInterrupts = self.REG[0x05] & self.REG[0x06]
                for i in range(8):
                    interruptHappened = ((maskedInterrupts >> i) & 1) == 1
                    if interruptHappened:
                        interruptLocation = i
                        break
                if interruptHappened:
                    self.INT = True
                    self.REG[0x06] &= ~(1 << interruptLocation)
                    cpu.REG[0x07] -= 1
                    cpu.RAM[cpu.REG[0x07]] = cpu.PC
                    cpu.REG[0x07] -= 1
                    cpu.RAM[cpu.REG[0x07]] = cpu.FL
                    for i in range(7):
                        cpu.REG[0x07] -= 1
                        cpu.RAM[cpu.REG[0x07]] = cpu.REG[i]
                    cpu.PC = cpu.RAM[0xF8 + interruptLocation]
            self.IR = self.ram_read(self.PC)
            operand_A = self.ram_read(self.PC + 1)
            operand_B = self.ram_read(self.PC + 2)
            if self.IR == 0x01:
                break
            if self.IR >> 5 & 0x01:
                op = self.ALU[self.IR]
            else:
                op = self.branchtable[self.IR]
            operands = (self, operand_A, operand_B)
            op(*operands[:1 + (self.IR >> 6)])
            self.PC += (self.IR >> 4 & 0x01 ^ 0x01) * (1 + (self.IR >> 6))
if __name__ == "__main__":
    cpu = CPU()
    cpu.load()
    cpu.run()
