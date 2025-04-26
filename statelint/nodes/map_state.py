from typing import Any, Optional

from ..fields import (
    ITEM_BATCHER,
    ITEM_PROCESSOR,
    ITEM_READER,
    ITEMS,
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
    QueryLanguage,
)
from ..fields.container import OneOfField
from ..problem import Problem
from .container_state import ContainerState
from .factory import NodeFactory
from .mixins import (
    ArgumentsMixin,
    AssignMixin,
    BatchInputMixin,
    CatchMixin,
    ItemSelectorMixin,
    NextXorEndMixin,
    OutputMixin,
    ParametersMixin,
    ResultPathMixin,
    ResultSelectorMixin,
    RetryMixin,
    TimeoutSecondsMixin,
)
from .node import NameAndPath, Node, StatePath
from .state import State


class MapConfig(ParametersMixin, ArgumentsMixin):
    @property
    def required_fields(self) -> list[Field]:
        return [*super().required_fields, RESOURCE]


class ReaderConfig(Node):
    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, OneOfField(MAX_ITEMS, MAX_ITEMS_PATH)]


class ItemReader(MapConfig):
    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, READER_CONFIG]

    def validate(self) -> list[Problem]:
        problems = super().validate()
        config = self._state.get(READER_CONFIG.name)
        if not isinstance(config, dict):
            return problems

        return (
            problems
            + ReaderConfig(
                self.state_path.make_child(READER_CONFIG), config, self.query_language
            ).validate()
        )


class ResultWriter(MapConfig):
    pass


class ItemProcessor(ContainerState):
    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, PROCESSOR_CONFIG]


class ItemBatcher(BatchInputMixin):
    @property
    def optional_fields(self) -> list[Field]:
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
    OutputMixin,
    AssignMixin,
    State,
):
    def __init__(
        self,
        node_factory: NodeFactory,
        state_path: StatePath,
        state: dict[str, Any],
        current_query_language: QueryLanguage,
    ) -> None:
        super().__init__(state_path, state, current_query_language)
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
    def required_fields(self) -> list[Field]:
        return [*super().required_fields, OneOfField(ITERATOR, ITEM_PROCESSOR)]

    @property
    def optional_fields(self) -> list[Field]:
        fields = [
            *super().optional_fields,
            ITEM_READER,
            RESULT_WRITER,
            ITEM_BATCHER,
        ]
        if self.query_language == QueryLanguage.JSONata:
            return [
                *fields,
                ITEMS,
                MAX_CONCURRENCY,
                TOLERATED_FAILURE_COUNT,
                TOLERATED_FAILURE_PERCENTAGE,
            ]
        return [
            *fields,
            ITEMS_PATH,
            OneOfField(MAX_CONCURRENCY, MAX_CONCURRENCY_PATH),
            OneOfField(TOLERATED_FAILURE_COUNT, TOLERATED_FAILURE_COUNT_PATH),
            OneOfField(TOLERATED_FAILURE_PERCENTAGE, TOLERATED_FAILURE_PERCENTAGE_PATH),
        ]

    def get_children(self) -> list[NameAndPath]:
        if not self._iterator:
            return []
        return list(self._iterator.get_children())

    def validate(self) -> list[Problem]:
        return super().validate() + [y for x in self._validators for y in x.validate()]

    def _get_iterator(self, state: dict[str, Any]) -> Optional[ContainerState]:
        iterator = state.get(ITERATOR.name)
        item_processor = state.get(ITEM_PROCESSOR.name)
        if isinstance(iterator, dict):
            return ContainerState(
                self._node_factory,
                self.state_path.make_child(ITERATOR),
                iterator,
                self.query_language,
            )
        if isinstance(item_processor, dict):
            return ItemProcessor(
                self._node_factory,
                self.state_path.make_child(ITEM_PROCESSOR),
                item_processor,
                self.query_language,
            )
        return None

    def _get_item_reader(self, state: dict[str, Any]) -> Optional[ItemReader]:
        item_reader = state.get(ITEM_READER.name)
        if isinstance(item_reader, dict):
            return ItemReader(
                self.state_path.make_child(ITEM_READER),
                item_reader,
                self.query_language,
            )
        return None

    def _get_result_writer(self, state: dict[str, Any]) -> Optional[ResultWriter]:
        result_writer = state.get(RESULT_WRITER.name)
        if isinstance(result_writer, dict):
            return ResultWriter(
                self.state_path.make_child(RESULT_WRITER),
                result_writer,
                self.query_language,
            )
        return None

    def _get_item_batcher(self, state: dict[str, Any]) -> Optional[ItemBatcher]:
        item_batcher = state.get(ITEM_BATCHER.name)
        if isinstance(item_batcher, dict):
            return ItemBatcher(
                self.state_path.make_child(ITEM_BATCHER),
                item_batcher,
                self.query_language,
            )
        return None
