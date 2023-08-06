import typing as t

_T = t.TypeVar('_T')


# TODO make NoInit with self replace function with check and create__subscribers attribute
# TODO publish loop???
# TODO filter in subscribe
class Publisher:
    def __init__(self, subscribers: t.Union[t.Callable, t.Iterable[t.Callable]] = None):
        self._subscribers = set()
        if subscribers:
            self.subscribe(subscribers)

    def publish(self, *args, loop=None, **kwargs):
        if loop:
            for callback in self._subscribers:
                loop.call_soon(callback, *args, **kwargs)
        else:
            for callback in self._subscribers:
                callback(*args, **kwargs)

    def subscribe(self, callback: t.Union[t.Callable, t.Iterable[t.Callable]]):
        if isinstance(callback, t.Iterable):
            self._subscribers.update(callback)
        else:
            self._subscribers.add(callback)

    def unsubscribe(self, callback: t.Union[t.Callable, t.Iterable[t.Callable]]):
        if isinstance(callback, t.Iterable):
            self._subscribers.difference_update(callback)
        else:
            try:
                self._subscribers.remove(callback)
            except KeyError:
                pass


# TODO make normally type hinted by IDE
def publisher(cls: _T) -> t.Union[t.Type[Publisher], _T]:
    def __init__(self, *args, **kw):
        super_init(self, *args, **kw)
        Publisher.__init__(self)

    super_init = getattr(cls, '__init__')
    setattr(cls, '__init__', __init__)
    setattr(cls, 'publish', Publisher.publish)
    setattr(cls, 'subscribe', Publisher.subscribe)
    setattr(cls, 'unsubscribe', Publisher.unsubscribe)
    return cls
