from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
import numbers
from pathlib import PurePath
from typing import IO
from typing import Any
from typing import Literal
from typing import Self
from typing import TypedDict
from typing import TypeVar
from typing import overload

from _typeshed import Incomplete
from ase.atom import Atom
from ase.calculators.calculator import Calculator
from ase.cell import Cell
from ase.constraints import FixConstraint
from ase.outputs import Properties
from ase.symbols import Symbols
import numpy as np
from numpy.random import BitGenerator
from numpy.random import RandomState
import numpy.typing as npt
from typing_extensions import Unpack

class Atoms:
    ase_objtype: str
    arrays: Incomplete
    info: Incomplete
    def __init__(
        self,
        symbols: str | Atoms | Sequence[str | Atom] | None = ...,
        positions: npt.ArrayLike[numbers.Real] | None = ...,
        numbers: npt.ArrayLike[numbers.Integral] | None = ...,
        tags: npt.ArrayLike[numbers.Integral] | None = ...,
        momenta: npt.ArrayLike[numbers.Real] | None = ...,
        masses: npt.ArrayLike[numbers.Real] | None = ...,
        magmoms: npt.ArrayLike[numbers.Real] | None = ...,
        charges: npt.ArrayLike[numbers.Real] | None = ...,
        scaled_positions: npt.ArrayLike[numbers.Real] | None = ...,
        cell: npt.ArrayLike[numbers.Real] | None = ...,
        pbc: bool | None = ...,
        celldisp: npt.ArrayLike[numbers.Real] | None = ...,
        constraint: FixConstraint | None = ...,
        calculator: Calculator | None = ...,
        info: dict | None = ...,
        velocities: npt.ArrayLike[numbers.Real] | None = ...,
    ) -> None: ...
    @property
    def symbols(self) -> Symbols: ...
    def set_calculator(self, calc: Calculator | None = ...) -> None: ...
    def get_calculator(self) -> Calculator | None: ...
    @property
    def calc(self) -> Calculator | None: ...
    @property
    def number_of_lattice_vectors(self) -> int: ...
    def set_constraint(
        self,
        constraint: FixConstraint
        | tuple[FixConstraint]
        | list[FixConstraint]
        | None = ...,
    ) -> None: ...
    constraints: list[FixConstraint]
    def set_cell(
        self,
        cell: npt.ArrayLike[numbers.Real] | None,
        scale_atoms: bool = ...,
        apply_constraint: bool = ...,
    ) -> None: ...
    def set_celldisp(self, celldisp: npt.ArrayLike[numbers.Real]) -> None: ...
    def get_celldisp(self) -> npt.NDArray[np.float_]: ...
    def get_cell(self, complete: bool = ...) -> Cell: ...
    def get_cell_lengths_and_angles(self) -> npt.NDArray[np.float_]: ...
    def get_reciprocal_cell(self) -> Cell: ...
    @property
    def pbc(self) -> npt.NDArray[np.bool_]: ...
    def set_pbc(self, pbc: npt.NDArray[np.bool_]) -> None: ...
    def get_pbc(self) -> npt.NDArray[np.bool_]: ...
    @overload
    def new_array(
        self,
        name: Any,
        a: npt.ArrayLike,
        dtype: type = ...,
        shape: tuple[int, ...] | None = ...,
    ) -> None: ...
    @overload
    def new_array(
        self,
        name: Any,
        a: npt.NDArray,
        dtype: Any = ...,
        shape: tuple[int, ...] | None = ...,
    ) -> None: ...
    def get_array(self, name: Any, copy: bool = ...) -> npt.NDArray: ...
    @overload
    def set_array(
        self,
        name: Any,
        a: npt.ArrayLike,
        dtype: type = ...,
        shape: tuple[int, ...] | None = ...,
    ) -> None: ...
    @overload
    def set_array(
        self,
        name: Any,
        a: npt.NDArray,
        dtype: Any = ...,
        shape: tuple[int, ...] | None = ...,
    ) -> None: ...
    def has(self, name: Any) -> bool: ...
    def set_atomic_numbers(self, numbers: npt.ArrayLike[numbers.Integral]) -> None: ...
    def get_atomic_numbers(self) -> npt.NDArray[np.int_]: ...
    def get_chemical_symbols(self) -> list[str]: ...
    def set_chemical_symbols(
        self, symbols: str | Iterable[str | numbers.Integral]
    ) -> None: ...
    def get_chemical_formula(
        self,
        mode: Literal['all', 'reduce', 'hill', 'metal'] = ...,
        empirical: bool = ...,
    ) -> str: ...
    def set_tags(self, tags: int | npt.ArrayLike[numbers.Integral]) -> None: ...
    def get_tags(self) -> npt.NDArray[np.int_]: ...
    def set_momenta(
        self,
        momenta: npt.ArrayLike[numbers.Real],
        apply_constraint: bool = ...,
    ) -> None: ...
    def set_velocities(self, velocities: npt.ArrayLike[numbers.Real]) -> None: ...
    def get_momenta(self) -> npt.NDArray[np.float_]: ...
    def set_masses(
        self,
        masses: Literal['defaults']
        | Literal['most_common']
        | Iterable[numbers.Real | None]
        | None = ...,
    ) -> None: ...
    def get_masses(self) -> npt.NDArray[np.float_]: ...
    def set_initial_magnetic_moments(
        self,
        magmoms: npt.ArrayLike[numbers.Real] | None = ...,
    ) -> None: ...
    def get_initial_magnetic_moments(self) -> npt.NDArray[np.float_]: ...
    def get_magnetic_moments(self) -> npt.NDArray[np.float_] | None: ...
    def get_magnetic_moment(self) -> numbers.Real | None: ...
    def set_initial_charges(
        self, charges: npt.ArrayLike[numbers.Real] | None = ...
    ) -> None: ...
    def get_initial_charges(self) -> npt.NDArray[np.float_]: ...
    def get_charges(self) -> npt.NDArray[np.float_] | None: ...
    def set_positions(
        self,
        newpositions: npt.ArrayLike[numbers.Real],
        apply_constraint: bool = ...,
    ) -> None: ...
    def get_positions(
        self,
        wrap: bool = ...,
        **wrap_kw: Unpack[
            TypedDict(
                'wrap_kw',
                {
                    'pbc': bool | npt.ArrayLike[bool | np.bool_],
                    'center': npt.ArrayLike[numbers.Real],
                    'pretty_translation': bool,
                    'eps': float,
                },
                total=False,
            )
        ],
    ) -> npt.NDArray[np.float_]: ...
    def get_potential_energy(
        self, force_consistent: bool = ..., apply_constraint: bool = ...
    ) -> numbers.Real | None: ...
    def get_properties(self, properties: list[str] | tuple[str]) -> Properties: ...
    def get_potential_energies(self) -> npt.NDArray[np.float_] | None: ...
    def get_kinetic_energy(self) -> numbers.Real: ...
    def get_velocities(self) -> npt.NDArray[np.float_]: ...
    def get_total_energy(self) -> numbers.Real: ...
    def get_forces(
        self, apply_constraint: bool = ..., md: bool = ...
    ) -> npt.NDArray[np.float_] | None: ...
    def get_stress(
        self,
        voigt: bool = ...,
        apply_constraint: bool = ...,
        include_ideal_gas: bool = ...,
    ) -> npt.NDArray[np.float_] | None: ...
    def get_stresses(
        self, include_ideal_gas: bool = ..., voigt: bool = ...
    ) -> npt.NDArray[np.float_] | None: ...
    def get_dipole_moment(self) -> npt.NDArray[np.float_] | None: ...
    def copy(self) -> Self: ...
    def todict(self) -> dict: ...
    @classmethod
    def fromdict(cls, dct: dict) -> Self: ...
    def __len__(self) -> int: ...
    def get_number_of_atoms(self) -> int: ...
    def get_global_number_of_atoms(self) -> int: ...
    def __add__(self, other: Atom | Atoms) -> Self: ...
    def extend(self, other: Atom | Atoms) -> None: ...
    def __iadd__(self, other: Atom | Atoms) -> Self: ...
    def append(self, atom: Atom | Atoms) -> None: ...
    def __iter__(self) -> Iterator[Atom]: ...
    @overload
    def __getitem__(self, i: numbers.Integral) -> Atom: ...
    @overload
    def __getitem__(self, i: slice | npt.ArrayLike[numbers.Integral]) -> Self: ...
    def __delitem__(
        self,
        i: numbers.Integral
        | slice
        | list[numbers.Integral]
        | npt.NDArray[np.bool_]
        | npt.NDArray[np.integer],
    ) -> None: ...
    def pop(self, i: int = ...) -> Atom: ...
    def __imul__(self, m: int | npt.ArrayLike[numbers.Integral]) -> Self: ...
    def repeat(self, rep: int | npt.ArrayLike[numbers.Integral]) -> Self: ...
    def __mul__(self, rep: int | npt.ArrayLike[numbers.Integral]) -> Self: ...
    def translate(
        self, displacement: numbers.Real | npt.ArrayLike[numbers.Real]
    ) -> None: ...
    def center(
        self,
        vacuum: numbers.Real | None = ...,
        axis: int | Iterable[numbers.Integral] = ...,
        about: npt.ArrayLike[numbers.Real] | None = ...,
    ) -> None: ...
    def get_center_of_mass(self, scaled: bool = ...) -> npt.NDArray[np.float_]: ...
    def set_center_of_mass(
        self, com: npt.ArrayLike[numbers.Real], scaled: bool = ...
    ) -> None: ...
    @overload
    def get_moments_of_inertia(
        self, vectors: Literal[True] = ...
    ) -> tuple[npt.NDArray[np.float_], npt.NDArray[np.float_]]: ...
    @overload
    def get_moments_of_inertia(
        self, vectors: Literal[False] = ...
    ) -> npt.NDArray[np.float_]: ...
    def get_angular_momentum(self) -> npt.NDArray[np.float_]: ...
    def rotate(
        self,
        a: Literal['x']
        | Literal['-x', 'y', '-y', 'z', '-z']
        | numbers.Real
        | npt.NDArray[np.float_],
        v: Literal['-x', 'y', '-y', 'z', '-z'] | npt.NDArray[np.float_],
        center: str | npt.ArrayLike[numbers.Real] = ...,
        rotate_cell: bool = ...,
    ) -> None: ...
    def euler_rotate(
        self,
        phi: numbers.Real = ...,
        theta: numbers.Real = ...,
        psi: numbers.Real = ...,
        center: npt.ArrayLike[numbers.Real] = ...,
    ) -> None: ...
    def get_dihedral(
        self,
        a0: numbers.Integral,
        a1: numbers.Integral,
        a2: numbers.Integral,
        a3: numbers.Integral,
        mic: bool = ...,
    ) -> float: ...
    def get_dihedrals(
        self, indices: npt.ArrayLike[float], mic: bool = ...
    ) -> npt.NDArray[np.float_]: ...
    def set_dihedral(
        self,
        a1: numbers.Integral,
        a2: numbers.Integral,
        a3: numbers.Integral,
        a4: numbers.Integral,
        angle: numbers.Real,
        mask: Sequence[bool] | None = ...,
        indices: Iterable[bool] | None = ...,
    ) -> None: ...
    def rotate_dihedral(
        self,
        a1: numbers.Integral,
        a2: numbers.Integral,
        a3: numbers.Integral,
        a4: numbers.Integral,
        angle: numbers.Real,
        mask: Sequence[bool] | None = ...,
        indices: Iterable[bool] | None = ...,
    ) -> None: ...
    def get_angle(
        self,
        a1: numbers.Integral,
        a2: numbers.Integral,
        a3: numbers.Integral,
        mic: bool = ...,
    ) -> float: ...
    def get_angles(
        self, indices: npt.ArrayLike[numbers.Integral], mic: bool = ...
    ) -> npt.NDArray[np.float_]: ...
    def set_angle(
        self,
        a1: numbers.Integral,
        a2: numbers.Integral | None = ...,
        a3: numbers.Integral | None = ...,
        angle: numbers.Real | None = ...,
        mask: Sequence[bool] | None = ...,
        indices: Iterable[bool] | None = ...,
        add: bool = ...,
    ) -> None: ...
    def rattle(
        self,
        stdev: numbers.Real = ...,
        seed: numbers.Integral
        | npt.ArrayLike[numbers.Integral]
        | BitGenerator
        | None = ...,
        rng: RandomState | None = ...,
    ) -> None: ...
    @overload
    def get_distance(
        self,
        a0: numbers.Integral,
        a1: numbers.Integral,
        mic: bool = ...,
        vector: Literal[True] = ...,
    ) -> npt.NDArray[np.float_]: ...
    @overload
    def get_distance(
        self,
        a0: numbers.Integral,
        a1: numbers.Integral,
        mic: bool = ...,
        vector: Literal[False] = ...,
    ) -> numbers.Real: ...
    def get_distances(
        self,
        a: numbers.Integral,
        indices: list[numbers.Integral] | slice | None,
        mic: bool = ...,
        vector: bool = ...,
    ) -> npt.NDArray[np.float_]: ...
    def get_all_distances(
        self, mic: bool = ..., vector: bool = ...
    ) -> npt.NDArray[np.float_]: ...
    def set_distance(
        self,
        a0: numbers.Integral,
        a1: numbers.Integral,
        distance: numbers.Real,
        fix: float = ...,
        mic: bool = ...,
        mask: Sequence[bool] | None = ...,
        indices: Iterable[bool] | None = ...,
        add: bool = ...,
        factor: bool = ...,
    ) -> None: ...
    def get_scaled_positions(self, wrap: bool = ...) -> npt.NDArray[np.float_]: ...
    def set_scaled_positions(self, scaled: npt.ArrayLike[numbers.Real]) -> None: ...
    def wrap(
        self,
        **wrap_kw: Unpack[
            TypedDict(
                'wrap_kw',
                {
                    'pbc': bool | npt.ArrayLike[bool],
                    'center': npt.ArrayLike[numbers.Real],
                    'pretty_translation': bool,
                    'eps': numbers.Real,
                },
                total=False,
            )
        ],
    ) -> None: ...
    def get_temperature(self) -> numbers.Real: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def get_volume(self) -> float: ...
    positions: np.array[numbers.Real]
    numbers: np.array[int]
    @property
    def cell(self) -> Cell: ...
    def write(
        self, filename: str | PurePath | IO, format: str | None = ..., **kwargs
    ) -> None: ...
    def iterimages(self) -> Iterator[Self]: ...
    def edit(self) -> None: ...

def string2vector(v: str | npt.ArrayLike[float]) -> npt.NDArray[np.float_]: ...
@overload
def default(data: None, dflt: Any) -> None: ...
@overload
def default(data: list | tuple, dflt: Any) -> list | None: ...
@overload
def default(data: TypeVar('T'), dflt: Any) -> TypeVar('T'): ...
