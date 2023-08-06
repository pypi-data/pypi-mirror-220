import ntpath

from _typeshed import Incomplete
from ase.cell import Cell as Cell
from ase.geometry import complete_cell as complete_cell
from ase.geometry.minkowski_reduction import (
    minkowski_reduce as minkowski_reduce,
)
from ase.utils import pbc2pbc as pbc2pbc
import numpy as np
import numpy.typing as npt

def translate_pretty(fractional, pbc): ...
def wrap_positions(
    positions,
    cell,
    pbc: bool | npt.ArrayLike[bool] = ...,
    center: ntpath.ArrayLike[float] = ...,
    pretty_translation: bool = ...,
    eps: float = ...,
): ...
def get_layers(atoms, miller, tolerance: float = ...): ...
def naive_find_mic(
    v: npt.ArrayLike[float | np.floating], cell: npt.ArrayLike[float | np.floating]
) -> tuple[
    np.ndarray[float | np.floating], np.floating | np.ndarray[float | np.floating]
]: ...
def general_find_mic(
    v: npt.ArrayLike[float | np.floating],
    cell: npt.ArrayLike[float | np.floating],
    pbc: bool = ...,
) -> tuple[
    np.ndarray[float | np.floating], np.floating | np.ndarray[float | np.floating]
]: ...
def find_mic(
    v: npt.ArrayLike[float | np.floating],
    cell: npt.ArrayLike[float | np.floating],
    pbc: bool = ...,
) -> tuple[
    np.ndarray[float | np.floating], np.floating | np.ndarray[float | np.floating]
]: ...
def conditional_find_mic(
    vectors: npt.ArrayLike[float | np.floating],
    cell: npt.ArrayLike[float | np.floating],
    pbc,
) -> tuple[
    list[np.ndarray[float | np.floating]],
    tuple[float | np.floating] | np.ndarray[float | np.floating],
]: ...
def get_angles(v0, v1, cell: Incomplete | None = ..., pbc: Incomplete | None = ...): ...
def get_angles_derivatives(
    v0, v1, cell: Incomplete | None = ..., pbc: Incomplete | None = ...
): ...
def get_dihedrals(
    v0, v1, v2, cell: Incomplete | None = ..., pbc: Incomplete | None = ...
): ...
def get_dihedrals_derivatives(
    v0, v1, v2, cell: Incomplete | None = ..., pbc: Incomplete | None = ...
): ...
def get_distances(
    p1,
    p2: Incomplete | None = ...,
    cell: Incomplete | None = ...,
    pbc: Incomplete | None = ...,
) -> tuple[np.ndarray[float | np.floating], np.ndarray[float | np.floating]]: ...
def get_distances_derivatives(
    v0, cell: Incomplete | None = ..., pbc: Incomplete | None = ...
): ...
def get_duplicate_atoms(atoms, cutoff: float = ..., delete: bool = ...): ...
def permute_axes(atoms, permutation): ...
