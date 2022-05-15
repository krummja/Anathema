from anathema.lib.ecstremity import Component


class Eyes(Component):

    def __init__(self, sight_range: int = 16) -> None:
        self.sight_range = sight_range
