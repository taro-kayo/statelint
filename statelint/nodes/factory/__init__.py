from abc import ABC, abstractmethod
from typing import Any, Optional

from ..node import Node, StatePath


class NodeFactory(ABC):
    @abstractmethod
    def get(self, parent: Node, state_path: StatePath, state: Any) -> Optional[Node]:
        pass  # pragma: no cover
