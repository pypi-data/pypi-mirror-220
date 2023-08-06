class ZeroAddressError(Exception):
    """Exception raised for errors in the input address.

    Attributes:
        address -- input address which caused the error
        message -- explanation of the error
    """

    def __init__(self, address, message="Address is a zero address"):
        self.address = address
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.address} -> {self.message}'

class TooManyResultsError(Exception):
    """Raised when a query returns more results than expected."""
    pass
