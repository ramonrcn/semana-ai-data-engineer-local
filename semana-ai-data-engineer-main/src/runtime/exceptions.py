class CapabilityError(Exception):
    pass


class InvalidCapabilityError(
    CapabilityError
):
    pass


class CapabilityNotFoundError(
    CapabilityError
):
    pass

class DuplicateCapabilityError(
    CapabilityError
):
    pass