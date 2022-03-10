from .species_data import SpeciesData


class Species:
    HUMAN = SpeciesData(
        name = "Human",
    )


def get_species_data(name: str) -> SpeciesData:
    return getattr(Species, name.upper())

