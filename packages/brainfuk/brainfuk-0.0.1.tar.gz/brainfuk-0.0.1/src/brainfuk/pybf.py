# PyBrainfuck
# My implementation of a Brainfuck interpreter in Python
# Has come cool thingies added onto it so its just simply better


# Imports
from __future__ import annotations

import argparse
from collections import OrderedDict

from naters_utils.objects import isntinstance


# Definitions
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import sys
        import tty

    def __call__(self):
        import sys
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

class AsciiInt(int):
    """An integer that has a range of 0-255"""
    
    # Modify addition and subtraction
    
    def __add__(self, other: int) -> int:
        res = super(AsciiInt, self).__add__(other)
        return self.__class__(min(max(res, 0), 255))
    
    
    def __sub__(self, other: int) -> int:
        res = super(AsciiInt, self).__sub__(other)
        return self.__class__(min(max(res, 0), 255))
    
    
    # Disable other operators
    
    def __mul__(self, other: int) -> int:
        raise TypeError("Can't multiply AsciiInt")
    
    
    def __truediv__(self, other: int) -> int:
        raise TypeError("Can't divide AsciiInt")
    
    
    def __floordiv__(self, other: int) -> int:
        raise TypeError("Can't divide AsciiInt")
    
    
    def __mod__(self, other: int) -> int:
        raise TypeError("Can't mod AsciiInt")
    
    
    def __pow__(self, other: int) -> int:
        raise TypeError("Can't pow AsciiInt")


class Memory:
    """A custom memory class for brainfuck"""
    
    def __init__(self) -> None:
        self.cells = {}
        self.pointer = 0
    
    
    # Subscripting
    
    def __getitem__(self, index: int | None) -> AsciiInt:
        # Run with pointer value if None is passed
        if index is None:
            index = self.pointer
        
        # Make sure index is an integer
        if isntinstance(index, int):
            raise TypeError("Memory index must be an integer")
        
        # Try to return the value from memory
        try:
            return self.cells[index]
        
        # Initialize the value and return 0 if no value set
        except KeyError:
            self.cells[index] = AsciiInt(0)
            return self.cells[index]
    
    
    def __setitem__(self, index: int, value: AsciiInt) -> None:
        # Run with pointer value if None is passed
        if index is None:
            index = self.pointer
        
        # Make sure index is an integer
        if isntinstance(index, int):
            raise TypeError("Memory index must be an integer")
        
        # Make sure value is an integer
        if isntinstance(value, AsciiInt):
            raise TypeError("Memory value must be an AsciiInt")
        
        # Set the value
        self.cells[index] = value
    
    
    # Operations
    
    def __iadd__(self, other: int) -> Memory:
        # Make sure other is an integer
        if isntinstance(other, int):
            raise TypeError("Other value must be an int")
        
        # Add the value to the cell at the pointer
        self[None] += other
        
        # Return the memory object
        return self
    
    
    def __isub__(self, other: int) -> Memory:
        # Make sure other is an integer
        if isntinstance(other, int):
            raise TypeError("Other value must be an int")
        
        # Subtract the value from the cell at the pointer
        self[None] -= other
        
        # Return the memory object
        return self
    
    
    def __lshift__(self, other: int) -> Memory:
        # Make sure other is an integer
        if isntinstance(other, int):
            raise TypeError("Other value must be an int")
        
        # Subtract the pointer value
        self.pointer -= other
        self.pointer = max(self.pointer, 0)
        
        # Return the memory object
        return self
    
    
    def __rshift__(self, other: int) -> Memory:
        # Make sure other is an integer
        if isntinstance(other, int):
            raise TypeError("Other value must be an int")
        
        # Add the pointer value
        self.pointer += other
        
        # Return the memory object
        return self
    
    
    # Output
    
    def __str__(self) -> str:
        # Convert every cell to a string
        cells = self.cells.copy()
        for n in range(max([*self.cells.keys(), self.pointer + 1])):
            try:
                _ = cells[n]
            except KeyError:
                cells[n] = AsciiInt(0)
        
        cells = OrderedDict(sorted(cells.items()))
        strings = []
        for index, value in cells.items():
            strings.append(f"{'>' if index == self.pointer else '|'} {str(value)}{''.join([' ' for _ in range(3 - len(str(value)))])} {'<' if index == self.pointer else '|'}")
        
        # Return the string
        return ''.join(strings)


def interpret(code: str, memory: Memory, loop_limit: int, recursion_depth: int = 0) -> None:
    """Interpret the code"""
    
    if recursion_depth == 0:
        code = ''.join(filter(lambda x: x in "+-<>.,[]#?", code))
    
    # Strip code before loop start
    if recursion_depth != 0:
        code = code[(code.find("[") + 1):]
    
    # Match characters
    index = 0
    while index < len(code):
        match code[index]:
            case '+':
                memory += 1
            case '-':
                memory -= 1
            case '<':
                memory << 1
            case '>':
                memory >> 1
            case '.':
                print(chr(int(memory[None])), end='')
            case ',':
                memory[None] = AsciiInt(ord(getch()))
            case '[':
                loop_amount = 0
                while memory[None] != 0:
                    interpret(code, memory, loop_limit, recursion_depth + 1)
                    loop_amount += 1
                    if loop_amount >= loop_limit:
                        raise RuntimeError("Loop limit reached")
                    
                code = ''.join(' ' for _ in range(code.find(']'))) + code[(code.find("]") + 1):]
            case ']':
                if recursion_depth != 0:
                    return
            case '#':
                print("\n" + str(memory))
            case '?':
                print(str(memory[None] == 0))
            case ' ':
                pass
            
        index += 1


def main(f: str, e: str, l: int) -> None:
    """Execute PyBrainfuck"""
    
        
    # Set memory and pointer
    memory = Memory()
    
    # Interpret a file
    if f is not None:
        with open(f, 'r') as file:
            c = file.read()
        interpret(c, memory, l)
    
    # Interpret a string
    elif e is not None:
        interpret(e, memory, l)


# Run
if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="PyBrainfuck interpreter")
    parser.add_argument("-f", help="File to interpret", type=str, default=None)
    parser.add_argument("-e", help="Evaluate a string", type=str, default=None)
    parser.add_argument("-l", help="Set the loop limit", type=int, default=1000)
    args = parser.parse_args()

    # Run main function
    main(**args.__dict__)