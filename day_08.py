import operator as op
import re
from collections import deque
from functools import reduce
from pprint import pprint

from parsy import (
    any_char,
    char_from,
    digit,
    eof,
    generate,
    letter,
    peek,
    regex,
    seq,
    string,
    string_from,
    whitespace,
)

from utils import puzzle_input

example = "\n".join(
    [
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",  # part 2: -> nop -4
        "acc +6",
    ]
)


class CpuException(Exception):
    pass


class IllegalInstruction(CpuException):
    pass


class IllegalMemoryAddress(CpuException):
    pass


class LoopException(CpuException):
    pass


class HandheldCpu:
    def __init__(self, program):
        self._program = program
        self._ip = 0
        self._acc = 0
        self._debug = {"seen_ips": set()}

    def run(self):
        try:
            while True:
                self.debug()
                if self._ip >= len(self._program):
                    raise IllegalMemoryAddress(
                        "Runoff ip={} acc={}".format(self._ip, self._acc)
                    )
                opcode, operand = self._program[self._ip]
                next_ip = self._ip + 1

                if opcode == "nop":
                    pass
                elif opcode == "acc":
                    self._acc += operand
                elif opcode == "jmp":
                    next_ip = self._ip + operand
                else:
                    raise IllegalInstruction(
                        "Illegal instruction ip={} acc={}".format(self._ip, self._acc)
                    )

                self._ip = next_ip
        except Exception as e:
            # print(f'Error: {e}')
            return (e, self._ip, self._acc)

    def debug(self):
        if self._ip in self._debug["seen_ips"]:
            raise LoopException(
                "Loop detected: ip={} acc={}".format(self._ip, self._acc)
            )
        else:
            self._debug["seen_ips"].add(self._ip)


# Parsing Combinators
optional_whitespace = regex(r"\s*")
word = regex(r"\w+")
number = regex(r"[-+]?\d+").map(int)

instruction = seq(word, whitespace >> number)
program = instruction.sep_by(string("\n")) << string("\n").optional()


with puzzle_input(8, example, False) as f:
    data, remain = program.parse_partial(f.read())
    # pprint(data)
    print("\n\n\nremaining:", repr(remain))

    # pprint(data)

    # Part 1
    handheld = HandheldCpu(data)
    print(handheld.run())

    # Part 2 - brute force
    # Because the language is quite limited, it may be possible to trace
    # the executiong backwards and build a graph(/dag?) of looping sections
    # and .... the problems space is small enough for a brute force :D
    for i in range(len(data)):
        opcode, _ = data[i]
        if opcode == "jmp":
            data[i][0] = "nop"  # patch
            handheld = HandheldCpu(data)
            r = handheld.run()
            if isinstance(r[0], IllegalMemoryAddress):
                print(r)
            data[i][0] = "jmp"  # restore
        elif opcode == "nop":
            data[i][0] = "jmp"  # patch
            handheld = HandheldCpu(data)
            r = handheld.run()
            if isinstance(r[0], IllegalMemoryAddress):
                print(r)
            data[i][0] = "nop"  # restore
