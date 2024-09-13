"""Dummy class
"""


class UserConsentRevoked(Exception):
    """Exception raised when an user entity consent is updated to false."""

    def __init__(self, message="User consent revoked"):
        self.message = message
        super().__init__(self.message)
