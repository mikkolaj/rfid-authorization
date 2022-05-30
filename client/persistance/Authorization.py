from enum import Enum


class Authorization(Enum):
    UNAUTHORIZED = 0
    AUTHORIZED = 1
    ADMIN = 2

    def __str__(self):
        return str(self.value)

    def from_int(number):
        for key in Authorization:
            if key.value == number:
                return key

    def toggle_authorization(authorization):
        return Authorization.AUTHORIZED if authorization == Authorization.UNAUTHORIZED else Authorization.UNAUTHORIZED

