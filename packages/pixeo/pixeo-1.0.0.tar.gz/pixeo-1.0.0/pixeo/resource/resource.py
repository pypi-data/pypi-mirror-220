from abc import ABC


class Resource(ABC):
    """Base class for all resource types."""

    def __init__(self, path):
        self.path = path
