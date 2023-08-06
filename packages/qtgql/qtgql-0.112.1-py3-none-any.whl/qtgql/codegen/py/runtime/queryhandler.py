from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generic, NamedTuple, Optional, TypeVar

from PySide6.QtCore import QObject, Signal
from PySide6.QtQuick import QQuickItem

from qtgql.codegen.py.runtime.environment import get_gql_env
from qtgql.tools import qproperty, slot

if TYPE_CHECKING:
    from qtgql.gqltransport.client import GqlClientMessage

T_QObject = TypeVar("T_QObject", bound=QObject)


class SelectionConfig(NamedTuple):
    selections: Dict[str, Optional[SelectionConfig]] = {}
    choices: Dict[str, SelectionConfig] = {}


class OperationMetaData(NamedTuple):
    operation_name: str
    selections: SelectionConfig


class QSingletonMeta(type(QObject)):  # type: ignore
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance


class BaseQueryHandler(Generic[T_QObject], QObject, metaclass=QSingletonMeta):
    """Each handler will be exposed to QML and."""

    instance: ClassVar[Optional[BaseQueryHandler]] = None
    ENV_NAME: ClassVar[str]
    OPERATION_METADATA: ClassVar[OperationMetaData]
    _message_template: ClassVar[GqlClientMessage]

    graphqlChanged = Signal()
    dataChanged = Signal()
    completedChanged = Signal()
    errorChanged = Signal()

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        name = self.__class__.__name__
        self.setObjectName(name)
        self._completed: bool = False
        self._data: Optional[T_QObject] = None
        self.environment = get_gql_env(self.ENV_NAME)
        self.environment.add_query_handler(self)
        self._consumers_count: int = 0
        self._operation_on_the_fly: bool = False

    def loose(self) -> None:
        """Releases retention from all children, real implementation is
        generated."""
        raise NotImplementedError

    def unconsume(self) -> None:
        self._consumers_count -= 1
        if self._consumers_count <= 0:
            self.loose()
            self._data = None

    def consume(self) -> None:
        # if it is the first consumer (or first after all previous consumers disposed) fetch the data here.
        if self._consumers_count <= 0 and not self._operation_on_the_fly:
            if self._completed:
                self.refetch()
            else:
                self.fetch()
        self._consumers_count += 1

    @property
    def message(self) -> GqlClientMessage:
        return self._message_template

    @qproperty(QObject, notify=dataChanged)
    def data(self) -> Optional[QObject]:
        return self._data

    @qproperty(bool, notify=completedChanged)
    def completed(self):
        return self._completed

    def fetch(self) -> None:
        self._operation_on_the_fly = True
        self.environment.client.execute(self)  # type: ignore

    @slot
    def refetch(self) -> None:
        if not self._operation_on_the_fly:
            self._completed = False
            self.fetch()

    def on_data(self, message: dict) -> None:  # pragma: no cover
        # real is on derived class.
        raise NotImplementedError

    def on_completed(self) -> None:
        self._completed = True
        self.completedChanged.emit()

    def on_error(self, message: list[dict[str, Any]]) -> None:  # pragma: no cover
        # This (unlike `on_data` is not implemented for real)
        raise NotImplementedError(message)


class UseQueryABC(QQuickItem):
    """Concrete implementation in the template."""

    ENV_NAME: ClassVar[str]

    # signals
    operationNameChanged = Signal()

    def __init__(self, parent: Optional[QQuickItem] = None):
        super().__init__(parent)
        self.destroyed.connect(self.unconsume)  # type: ignore
        self._operationName: Optional[str] = None
        self.env = get_gql_env(self.ENV_NAME)
        self.handler: Optional[BaseQueryHandler] = None

    @slot
    def set_operationName(self, graphql: str) -> None:
        self._operationName = graphql
        self.handler = self.env.get_handler(graphql)
        self.handler.consume()
        self.operationNameChanged.emit()  # type: ignore

    @qproperty(str, fset=set_operationName, notify=operationNameChanged)
    def operationName(self):
        return self._operationName

    @slot
    def unconsume(self) -> None:
        assert self.handler
        self.handler.unconsume()
