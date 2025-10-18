import abc

class MediaLoader(abc.ABC):
    @abc.abstractmethod
    def play(self) -> None:
        ...

    @property
    @abc.abstractmethd
    def ext(self) -> str:
        ...

class Wav(MediaLoader):
    pass

x = Wav()

class Ogg(MediaLoader):
    ext = '.ogg'
    def play(self) -> None:
        pass

o = Ogg()

