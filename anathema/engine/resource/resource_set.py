from __future__ import annotations
from typing import *

from dataclasses import dataclass
import itertools
from collections.abc import Mapping
from . import T
from .resource import Resource
from .tag import Tag
from .resource_query import ResourceQuery
from .query_key import QueryKey

if TYPE_CHECKING:
    pass


@dataclass
class ResourceData:
    name: str = ""
    depth: int = 0
    start_depth: int = 0
    end_depth: int = 0
    start_freq: float = 0
    end_freq: float = 0
    tags: str = ""


class ResourceSet(Generic[T]):

    def __init__(self) -> None:
        self._tags: Mapping[str, Tag[T]] = {}
        self._resources: Mapping[str, Resource[T]] = {}
        self._queries: Map[QueryKey, ResourceQuery[T]] = {}

    @property
    def is_empty(self) -> bool:
        return bool(self._resources)

    @property
    def is_not_empty(self) -> bool:
        return not self.is_empty

    @property
    def all_resources(self) -> Iterable[T]:
        return [_ for _ in self._resources.values()]

    def add(
            self,
            obj: T,
            name: str = str(len(self._resources)),
            depth: int = 1,
            frequency: float = 1.0,
            tags: str = ""
        ) -> None:
        self._add(obj, name, depth, depth, frequency, frequency, tags)

    def add_ranged(
            self,
            obj: T,
            name: str = str(len(self._resources)),
            start: int = 1,
            end: int = -1,
            start_freq: float = 1.0,
            end_freq: float = -1,
            tags: str = ""
        ) -> None:
        self._add(obj, name, start, end, start_freq, end_freq, tags)

    def _add(
            self,
            obj: T,
            name: str = str(len(self._resources)),
            start_depth: int = 1,
            end_depth: int = -1,
            start_freq: float = 1.0,
            end_freq: float = -1,
            tags: str = ""
        ) -> None:
        end_depth = end_depth if end_depth > -1 else start_depth
        end_freq = end_freq if end_freq > -1 else start_freq

        if name in self._resources.keys():
            raise ArgumentError(f"Already have a resource named {name}")
        resource = Resource(obj, start_depth, end_depth, start_freq, end_freq)
        self._resources[name] = resource

        if tags != "":
            for tag_name in tags.split(" "):
                tag = self._tags[tag_name]
                if tag is None:
                    raise ArgumentError(f"Unknown tag {tag_name}")
                resource.tags.add(tag)

    def define_tags(self, paths: str) -> None:
        for path in paths.split(" "):
            parent: Optional[Tag[T]] = None
            for name in path.split("/"):
                tag = self._tags[name]
                if tag is None:
                    tag = Tag[T](name, parent)
                    self._tags[name] = tag
                parent = tag

    def find(self, name: str) -> T:
        resource = self._resources[name]
        if resource is None:
            raise ArgumentError(f"Unknown resource {name}")
        return resource.obj

    def try_find(self, name: str) -> T | None:
        resource = self._resources[name]
        if resource is None:
            return None
        return resource.obj

    def has_tag(self, name: str, tag_name: str) -> bool:
        """Returns whether the resource with [name] has [tag_name] as one of
        its immediate tags or one of their parents.
        """
        resource = self._resources[name]
        if resource is None:
            raise ArgumentError(f"Unknown resource {name}")
        tag = self._tags[tag_name]
        if tag is None:
            raise ArgumentError(f"Unknown tag {tag_name}")
        return any([this_tag.contains(tag) for this_tag in resource.tags])

    def get_tags(self, name: str) -> Iterable[str]:
        """Get the names of the tags for the resource [name]."""
        resource = self._resources[name]
        if resource is None:
            raise ArgumentError(f"Unknown resource {name}")
        return [tag.name for tag in resource.tags]

    def tag_exists(self, tag_name: str) -> bool:
        return tag_name in self._tags.keys()

    def try_choose(
            self,
            depth: int,
            tag: Optional[str] = None,
            include_parents: bool = True
        ) -> T | None:
        if tag is None:
            return self._run_query("", depth, (lambda _: 1.0))
        goal_tag = self._tags[tag]
        assert goal_tag is not None

        label = goal_tag.name
        if not include_parents:
            label += " (only)"

        def _scale(resource: Resource[T]) -> float:
            scale = 1.0

            this_tag = goal_tag
            while this_tag is not None:
                for resource_tag in resource.tags:
                    if resource_tag.contains(this_tag):
                        return scale
                this_tag = this_tag.parent
                scale = scale / 10.0
            return 0.0

        return self._run_query(label, depth, _scale)

    def try_choose_matching(self, depth: int, tags: Iterable[str]) -> T | None:
        tag_objects = []
        for name in tags:
            _tag = self._tags[name]
            if _tag is None:
                raise ArgumentError(f"Unknown tag {name}")
            tag_objects.append(tag)

        tag_names = list(tags)
        tag_names.sort()

        def _scale(resource: Resource[T]) -> float:
            for resource_tag in resource.tags:
                if any([tag.contains(resource_tag) for tag in tag_objects]):
                    return 1.0
                return 0.0

        return self._run_query(f"{'|'.join(tag_names)} (match)", depth, _scale)

    def _run_query(
            self,
            name: str,
            depth: int,
            scale: Callable[[Resource[T]], float]
        ) -> T | None:
        key = QueryKey(name, depth)
        query = self._queries[key]
        if query is None:
            resources: List[Resource[T]] = []
            chances: List[float] = []
            total_chance: float = 0.0

            for resource in self._resources.values():
                chance = scale(resource)
                if chance == 0.0:
                    continue
                chance *= resource.frequency_at_depth(depth) * resource.chance_at_depth(depth)
                chance = max(0.0000001, chance)
                total_chance += chance
                resources.add(resource)
                chances.add(total_chance)

            query: ResourceQuery[T] = ResourceQuery(depth, resources, chances, total_chance)
            self._queries[key] = query
        return query.choose()
