from abc import ABC, abstractmethod


class AbstractToeter(ABC):
    @abstractmethod
    def toeter(self, message, media_files=None, in_reply_to=None):
        pass


class MultiToeter(AbstractToeter):
    def __init__(self, toeters: dict):
        if not isinstance(toeters, dict):
            raise ValueError('Expected dict: {id: toet_adapter, id: toet_adapter, ...}')

        self._toeters = toeters

    def toeter(self, message, in_reply_to=None, *args, **kwargs):
        retvals = {}
        for toeterid, toeter in self._toeters.items():
            irp = None
            if in_reply_to is not None:
                irp = in_reply_to.get(toeterid, None)
            retval = toeter.toeter(message, in_reply_to=irp, *args, **kwargs)
            retvals[toeterid] = retval

        return retvals
