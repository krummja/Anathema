from anathema.lib.ecstremity import Component


class Eyes(Component):

    def __init__(self, sight_range: int = 12) -> None:
        self.sight_range = sight_range
