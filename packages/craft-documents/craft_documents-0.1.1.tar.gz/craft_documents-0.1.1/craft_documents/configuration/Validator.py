from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from craft_documents.configuration.Semantic import Semantic

# Untyped reference to Configuration.. never could resolve the circular import


@dataclass
class Validator(ABC):
    """
    Absstract base class describing a validator for the configuration.
    An implementation of a validator should handle exactly one key
    that can be set in the configuration.

    Subclasses need to implement `validate()` and `resolve()`.
    If `validate()` returns `False`, `resolve()` will be run.
    """

    _semantic: Semantic
    _key: str

    @property
    def semantic(self) -> Semantic:
        return self._semantic

    @property
    def key(self) -> str:
        return self._key

    @property
    def configuration(self):
        return self._configuration

    def __init__(self):
        """
        Set values for `_key` and `_semantic`.
        """
        pass

    @abstractmethod
    def validate(self, value) -> bool:
        """
        Implement logic in order to validate the value of a specific key.
        If key does not exist, this method will be skipped and
        `resolve` is directly run.
        """
        pass

    def default(self):
        """
        Implement logic to resolve an invalid value for the key.
        For example by providing a default value or doing nothing.

        The resolved value should be returned.
        """
        pass

    def lint(self, value):
        """
        Provide a consistent type for the value in the key.
        This is only run if the key exists.

        Return the formatted value or the input if it was already correct.
        """
        return value

    def run(self, configuration):
        self._configuration = configuration

        if self.key in configuration:
            configuration[self.key] = self.lint(configuration[self.key])

        match self.semantic:
            case Semantic.OPTIONAL:
                if self.key in configuration:
                    self.validate(configuration[self.key])
            case Semantic.REQUIRED:
                if self.key in configuration:
                    if not self.validate(configuration[self.key]):
                        configuration[self.key] = self.default()
                else:
                    configuration[self.key] = self.default()
