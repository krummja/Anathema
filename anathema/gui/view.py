from __future__ import annotations
from typing import *
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from gui.screen import Screen
    from tcod.event import KeyboardEvent


class View:
    
    def __init__(self, parent: Optional[View] = None) -> None:
        self.screen: Screen | None = None
        self.is_responder: bool = False
        self.parent = parent
        self.children: List[View] = []
        self._bounds: Rect = Rect(Point(0, 0), Size(0, 0))

    @property
    def bounds(self) -> Rect:
        """Rect object that defines the position and dimensions of the View."""
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        """Set the Rect object that defines the position and dimension of
        the View.

        Customize this in subclasses to have dynamic bounds calculation.
        """
        self._bounds = value

    @property
    def leftmost_leaf(self) -> View:
        """Return the leftmost leaf of the View hierarchy."""
        if self.children:
            return self.children[0].leftmost_leaf
        return self

    @property
    def postorder_traversal(self) -> Generator[View, Any, None]:
        """Depth-first post-order traversal of the View hierarchy."""
        for child in self.children:
            yield from child.postorder_traversal
        yield self

    @property
    def ancestors(self) -> Generator[View, Any, None]:
        """Traverse up the hierarchy yielding each View."""
        view = self.parent
        while view:
            yield view
            view = view.parent

    @property
    def can_become_responder(self) -> bool:
        """Override this to permit a subclass to enter the Responder queue."""
        return False
    
    @property
    def can_resign_responder(self) -> bool:
        """Override this to permit a subclass to exit the Responder queue. """
        return False

    def on_become_responder(self) -> None:
        """Hook invoked when a View becomes an active Responder."""
        self.is_responder = True

    def on_resign_responder(self) -> None:
        """Hook invoked when a View resigns active Responder."""
        self.is_responder = False

    def add_child(self, view: View) -> None:
        """Add a View as a child of the current View."""
        self.children.append(view)

    def remove_child(self, view: View) -> None:
        """Remove a View from this View's hierarchy."""
        self.children.remove(view)

    def remove_child_at_index(self, index: int) -> None:
        """Pop a view by index from this View's children."""
        self.children.pop(index)

    def draw(self) -> None:
        self.perform_draw()
        for child in self.children:
            child.perform_draw()

    def perform_draw(self) -> None:
        """Override in subclasses to give the View its appearance in the console."""
        pass

    def update(self) -> None:
        pass

    def handle_input(self, event: KeyboardEvent) -> bool:
        """Override in subclasses to handle inputs from the core input event bus."""
        return False
