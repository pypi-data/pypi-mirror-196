"""Methods to change nuclide abundance in compositions."""
from typing import Generator, Iterable, Tuple

import pandas as pd

from mckit_nuclides.nuclides import NUCLIDES_TABLE


def convert_to_atomic_fraction(
    composition: pd.DataFrame, fraction_column: str = "fraction"
) -> pd.DataFrame:
    """Change fractions by mass to fractions by atoms.

    Args:
        composition: DataFrame indexed by MultipleIndex (atomic_number, mass_number)
        fraction_column: name of column presenting fraction

    Returns:
        DataFrame: df with modified column "fraction"
    """
    composition[fraction_column] /= (
        NUCLIDES_TABLE.loc[composition.index, ["nuclide_mass"]].to_numpy().flatten()
    )
    return composition


def expand_natural_presence(
    zaf: Iterable[Tuple[int, int, float]]
) -> Generator[Tuple[int, int, float], None, None]:
    """Convert sequence of nuclide-fraction specification with natural presence.

    Substitute a sequence of nuclides when mass number is specified as 0.
    This means natural presence.

    Args:
        zaf: sequence of atomic number, mass number and fraction

    Yields:
        atomic number, mass_number, and corrected atomic fraction
    """  # DAR401
    for z, a, f in zaf:
        if a != 0:
            yield z, a, f
        else:
            isotopic_compositions: pd.Series = NUCLIDES_TABLE.loc[z].isotopic_composition
            isotopic_compositions = isotopic_compositions[0 < isotopic_compositions]
            for _a, _ic in isotopic_compositions.items():
                yield z, _a, f * _ic
