"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0x00] * 0xFF
        self.PC = 0x00
        self.reg = [0x00] * 0x08
        self.fl = 0x00
        self.branchtable = {}

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.RAM[address] = instruction
            address += 1

    def ram_read(self, MAR):
        return self.RAM[MAR]

    def ram_write(self, MAR, MDR):
        self.RAM[MAR] = MDR & 0xFF

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            self.IR = self.ram_read(self.PC)
            operand_A = self.ram_read(self.PC + 1)
            operand_B = self.ram_read(self.PC + 2)
            if self.IR in self.branchtable:
                op = self.branchtable[self.IR]
                if self.IR & 0x80 >> 7:
                    self.PC += 3
                    self.alu(op, operand_A, operand_B)
                elif self.IR & 0x40 >> 6:
                    self.PC += 2
                    self.alu(op, operand_A, 0x00)
                else:
                    self.PC += 1
                    self.alu(op, 0x00, 0x00)
            elif self.IR == 0x01:
                break
            elif self.IR == 0x82:
                self.PC += 3
                self.reg[operand_A] = operand_B
            elif self.IR == 0x47:
                self.PC += 2
                print(self.reg[operand_A])

            self.PC &= 0xFF
if __name__ == "__main__":
    cpu = CPU()
    cpu.load()
    cpu.run()
