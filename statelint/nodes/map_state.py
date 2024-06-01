from typing import Any, Dict, List, Optional

from ..fields import (
    ITEM_BATCHER,
    ITEM_PROCESSOR,
    ITEM_READER,
    ITEMS_PATH,
    ITERATOR,
    MAX_CONCURRENCY,
    MAX_CONCURRENCY_PATH,
    MAX_INPUT_BYTES_PER_BATCH,
    MAX_INPUT_BYTES_PER_BATCH_PATH,
    MAX_ITEMS,
    MAX_ITEMS_PATH,
    MAX_ITEMS_PER_BATCH,
    MAX_ITEMS_PER_BATCH_PATH,
    PROCESSOR_CONFIG,
    READER_CONFIG,
    RESOURCE,
    RESULT_WRITER,
    TOLERATED_FAILURE_COUNT,
    TOLERATED_FAILURE_COUNT_PATH,
    TOLERATED_FAILURE_PERCENTAGE,
    TOLERATED_FAILURE_PERCENTAGE_PATH,
    Field,
)
from ..fields.container import OneOfField
from ..problem import Problem
from .container_state import ContainerState
from .factory import NodeFactory
from .mixins import (
    BatchInputMixin,
    CatchMixin,
    ItemSelectorMixin,
    NextXorEndMixin,
    ParametersMixin,
    ResultPathMixin,
    ResultSelectorMixin,
    RetryMixin,
    TimeoutSecondsMixin,
)
from .node import NameAndPath, Node, StatePath
from .state import State


class MapConfig(ParametersMixin):
    @property
    def required_fields(self) -> List[Field]:
        return [*super().required_fields, RESOURCE]


class ReaderConfig(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, OneOfField(MAX_ITEMS, MAX_ITEMS_PATH)]


class ItemReader(MapConfig):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, READER_CONFIG]

    def validate(self) -> List[Problem]:
        problems = super().validate()
        config = self._state.get(READER_CONFIG.name)
        if not isinstance(config, dict):
            return problems

        return (
            problems
            + ReaderConfig(self.state_path.make_child(READER_CONFIG), config).validate()
        )


class ResultWriter(MapConfig):
    pass


class ItemProcessor(ContainerState):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, PROCESSOR_CONFIG]


class ItemBatcher(BatchInputMixin):
    @property
    def optional_fields(self) -> List[Field]:
        return [
            *super().optional_fields,
            OneOfField(MAX_ITEMS_PER_BATCH, MAX_ITEMS_PER_BATCH_PATH),
            OneOfField(MAX_INPUT_BYTES_PER_BATCH, MAX_INPUT_BYTES_PER_BATCH_PATH),
        ]


class MapState(
    NextXorEndMixin,
    ResultPathMixin,
    ItemSelectorMixin,
    ResultSelectorMixin,
    TimeoutSecondsMixin,
    CatchMixin,
    RetryMixin,
    State,
):
    def __init__(
        self, node_factory: NodeFactory, state_path: StatePath, state: Dict[str, Any]
    ) -> None:
        super().__init__(state_path, state)
        self._node_factory = node_factory
        self._iterator = self._get_iterator(state)
        self._validators = (
            x
            for x in (
                self._iterator,
                self._get_item_reader(state),
                self._get_result_writer(state),
                self._get_item_batcher(state),
            )
            if x
        )

    @property
    def required_fields(self) -> List[Field]:
        return [*super().required_fields, OneOfField(ITERATOR, ITEM_PROCESSOR)]

    @property
    def optional_fields(self) -> List[Field]:
        return [
            *super().optional_fields,
            ITEMS_PATH,
            OneOfField(MAX_CONCURRENCY, MAX_CONCURRENCY_PATH),
            OneOfField(TOLERATED_FAILURE_COUNT, TOLERATED_FAILURE_COUNT_PATH),
            OneOfField(TOLERATED_FAILURE_PERCENTAGE, TOLERATED_FAILURE_PERCENTAGE_PATH),
            ITEM_READER,
            RESULT_WRITER,
            ITEM_BATCHER,
        ]

    def get_children(self) -> List[NameAndPath]:
        if not self._iterator:
            return []
        return list(self._iterator.get_children())

    def validate(self) -> List[Problem]:
        return super().validate() + [y for x in self._validators for y in x.validate()]

    def _get_iterator(self, state: Dict[str, Any]) -> Optional[ContainerState]:
        iterator = state.get(ITERATOR.name)
        item_processor = state.get(ITEM_PROCESSOR.name)
        if isinstance(iterator, dict):
            return ContainerState(
                self._node_factory, self.state_path.make_child(ITERATOR), iterator
            )
        if isinstance(item_processor, dict):
            return ItemProcessor(
                self._node_factory,
                self.state_path.make_child(ITEM_PROCESSOR),
                item_processor,
            )
        return None

    def _get_item_reader(self, state: Dict[str, Any]) -> Optional[ItemReader]:
        item_reader = state.get(ITEM_READER.name)
        if isinstance(item_reader, dict):
            return ItemReader(self.state_path.make_child(ITEM_READER), item_reader)
        return None

    def _get_result_writer(self, state: Dict[str, Any]) -> Optional[ResultWriter]:
        result_writer = state.get(RESULT_WRITER.name)
        if isinstance(result_writer, dict):
            return ResultWriter(
                self.state_path.make_child(RESULT_WRITER), result_writer
            )
        return None

    def _get_item_batcher(self, state: Dict[str, Any]) -> Optional[ItemBatcher]:
        item_batcher = state.get(ITEM_BATCHER.name)
        if isinstance(item_batcher, dict):
            return ItemBatcher(self.state_path.make_child(ITEM_BATCHER), item_batcher)
        return None
