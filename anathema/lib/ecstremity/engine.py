from __future__ import annotations
from typing import *

from .component_registry import ComponentRegistry
from .prefab_registry import PrefabRegistry
from .world import World

if TYPE_CHECKING:
    from .component import Component


class Client:
    """Stub class to define the engine-internal Client type."""


C = TypeVar("Client")


class Engine(Generic[C]):

    def __init__(self, client: Optional[C] = None):
        self.client = client
        self.components: ComponentRegistry = ComponentRegistry(self)
        self.prefabs: PrefabRegistry = PrefabRegistry(self)

    def register_component(self, component: Component) -> None:
        """Add a component to the component registry."""
        self.components.register(component)

    def create_world(self) -> World:
        """Create a new World instance."""
        return World(self)

    @staticmethod
    def destroy_world(world: World) -> None:
        """Destroy an existing World instance."""
        world.destroy()
