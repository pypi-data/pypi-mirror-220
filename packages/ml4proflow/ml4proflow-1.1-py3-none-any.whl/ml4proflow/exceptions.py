class ChannelAlreadyExists(Exception):
    pass


class NoSuchModule(Exception):
    pass


class NoSuchChannel(Exception):
    pass


class UnknownModeError(Exception):
    """Raised when the configured mode is not supported.
    """
    pass


class SettingsError(Exception):
    """Raised when the configuration is invalid.
    """
    pass


class ModuleIsAlreadySink(Exception):
    pass


class InterfaceFunction(Exception):
    pass
