from _typeshed import Incomplete
from ase.data import atomic_masses as atomic_masses, atomic_numbers as atomic_numbers, chemical_symbols as chemical_symbols

names: Incomplete

def atomproperty(name, doc): ...
def abcproperty(index): ...
def xyzproperty(index): ...

class Atom:
    data: Incomplete
    index: Incomplete
    atoms: Incomplete
    def __init__(self, symbol: str = ..., position=..., tag: Incomplete | None = ..., momentum: Incomplete | None = ..., mass: Incomplete | None = ..., magmom: Incomplete | None = ..., charge: Incomplete | None = ..., atoms: Incomplete | None = ..., index: Incomplete | None = ...) -> None: ...
    @property
    def scaled_position(self): ...
    def cut_reference_to_atoms(self) -> None: ...
    def get_raw(self, name): ...
    def get(self, name): ...
    def set(self, name, value) -> None: ...
    def delete(self, name) -> None: ...
    symbol: Incomplete
    number: Incomplete
    position: Incomplete
    tag: Incomplete
    momentum: Incomplete
    mass: Incomplete
    magmom: Incomplete
    charge: Incomplete
    x: Incomplete
    y: Incomplete
    z: Incomplete
    a: Incomplete
    b: Incomplete
    c: Incomplete
