"""Compile-time error types."""


class CompileError(Exception):
    """Base class for errors reported to the user that stop compilation."""

    def __init__(self, message, file=None, line=None):
        super().__init__(message)
        self.message = message
        self.file = file
        self.line = line


class MlvcSyntaxError(CompileError):
    pass


class MlvcMemoryError(CompileError):
    pass
