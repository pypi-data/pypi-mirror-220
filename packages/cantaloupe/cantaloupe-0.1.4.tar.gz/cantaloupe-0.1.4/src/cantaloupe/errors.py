class CantaloupeError(Exception):
    """Base class for all Cantaloupe errors."""

    pass


class CantaloupeConfigError(CantaloupeError):
    """Raised when there is an error with the configuration."""

    pass


class CantaloupeContextError(CantaloupeError):
    """Raised when there is an error with the context."""

    pass


class InvalidWorkflow(CantaloupeError):
    """Raised when there is an error with the workflow."""

    pass


class ValidationError(CantaloupeError):
    """Raised when there is an error with a variable."""

    pass
