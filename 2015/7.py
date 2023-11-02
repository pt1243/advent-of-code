from __future__ import annotations

from typing import ClassVar
from enum import auto, Enum
from functools import cache

class ConnectionType(Enum):
    Const = auto()
    And = auto()
    Or = auto()
    Not = auto()
    Lshift = auto()
    Rshift = auto()

class Wire:
    lookup: ClassVar[dict[str, Wire]] = {}

    def __init__(self, s: str) -> None:
        self.name = s.split(" -> ")[1]
        # print(f"setting name to {self.name}")
        arrow_index = s.index("-")
        self.lookup[self.name] = self
        self.eval_type: ConnectionType

        if "AND" in s:
            self.eval_type = ConnectionType.And
            dep1 = s[0:s.index("AND")-1]
            dep2 = s[s.index("AND")+4:arrow_index-1]
            try:
                dep1 = int(dep1)
            except ValueError:
                pass
            try:
                dep2 = int(dep2)
            except ValueError:
                pass
            self.dependencies = (dep1, dep2)
        
        elif "OR" in s:
            self.eval_type = ConnectionType.Or
            dep1 = s[0:s.index("OR")-1]
            dep2 = s[s.index("OR")+3:arrow_index-1]
            self.dependencies = (dep1, dep2)

        elif "NOT" in s:
            self.eval_type = ConnectionType.Not
            self.dependencies = s[4:arrow_index-1]
        
        elif "LSHIFT" in s:
            self.eval_type = ConnectionType.Lshift
            dep1 = s[0:s.index("LSHIFT")-1]
            dep2 = int(s[s.index("LSHIFT")+7:arrow_index-1])
            self.dependencies = (dep1, dep2)

        elif "RSHIFT" in s:
            self.eval_type = ConnectionType.Rshift
            dep1 = s[0:s.index("RSHIFT")-1]
            dep2 = int(s[s.index("RSHIFT")+7:arrow_index-1])
            self.dependencies = (dep1, dep2)
            
        else:
            self.eval_type = ConnectionType.Const
            source = s.split(" -> ")[0]
            try:
                dep = int(source)
            except ValueError:
                dep = source
            self.dependencies = dep
    
    @cache
    def evaluate(self) -> int:
        # print(f"evaluating {self}")
        if self.eval_type is ConnectionType.And:
            dep1, dep2 = self.dependencies
            if isinstance(dep1, str) and isinstance(dep2, str):
                return self.lookup[dep1].evaluate() & self.lookup[dep2].evaluate()
            elif isinstance(dep1, str):  # dep2 is an int
                return self.lookup[dep1].evaluate() & dep2
            else:  # dep1 is an int
                return dep1 & self.lookup[dep2].evaluate()
        
        if self.eval_type is ConnectionType.Or:
            dep1, dep2 = self.dependencies
            return self.lookup[dep1].evaluate() | self.lookup[dep2].evaluate()
        
        if self.eval_type is ConnectionType.Not:
            return 65535 - self.lookup[self.dependencies].evaluate()
        
        if self.eval_type is ConnectionType.Lshift:
            dep, shift = self.dependencies
            return self.lookup[dep].evaluate() << shift

        if self.eval_type is ConnectionType.Rshift:
            dep, shift = self.dependencies
            return self.lookup[dep].evaluate() >> shift
        
        if isinstance(self.dependencies, int):
            return self.dependencies
        return self.lookup[self.dependencies].evaluate()
    
    def __str__(self) -> str:
        return f"Wire {self.name}"
    
    def __repr__(self) -> str:
        return str(self)


def problem_1():
    with open('./2015/resources/7.txt') as f:
        connections = [line.strip() for line in f]

    for connection in connections:
        Wire(connection)
    
    print(Wire.lookup["a"].evaluate())

def problem_2():
    with open('./2015/resources/7.txt') as f:
        connections = [line.strip() for line in f]

    for connection in connections:
        Wire(connection)
    
    Wire(f"{Wire.lookup["a"].evaluate()} -> b")
    for wire in Wire.lookup.values():
        wire.evaluate.cache_clear()

    print(Wire.lookup["a"].evaluate())