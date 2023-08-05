import dataclasses
from znflow import utils
from znflow.base import NodeBaseMixin
import typing



@dataclasses.dataclass(frozen=True)
class Connection:
    """A Connector for Nodes.
    
    instance: either a Node or FunctionFuture
    attribute:
        Node.attribute
        or FunctionFuture.result
        or None if the class is passed and not an attribute
    """

    instance: any
    attribute: any
    item: any = None

    def __getitem__(self, item):
        return dataclasses.replace(self, instance=self, attribute="result", item=item)

    def __post_init__(self):
        if self.attribute is not None and self.attribute.startswith("_"):
            raise ValueError("Private attributes are not allowed.")

    @property
    def uuid(self):
        return self.instance.uuid

    @property
    def result(self):
        result = (
            getattr(self.instance, self.attribute) if self.attribute else self.instance
        )

        return result[self.item] if self.item else result
    
class UpdateConnectors(utils.IterableHandler):
    def default(self, value, **kwargs):
        return value.result if isinstance(value, Connection) else value
    
@dataclasses.dataclass
class FunctionFuture(NodeBaseMixin):
    function: typing.Callable
    args: typing.Tuple
    kwargs: typing.Dict
    item: any = None

    _result: any = dataclasses.field(default=None, init=False, repr=True)

    _protected_ = NodeBaseMixin._protected_ + ["function", "args", "kwargs"]

    def run(self):
        self._result = self.function(*self.args, **self.kwargs)

    def __getitem__(self, item):
        return Connection(instance=self, attribute="result", item=item)

    @property
    def result(self):
        if self._result is None:
            self.run()
        return self._result


