from passlib.hash import pbkdf2_sha256


class PasswordHasher:
    @staticmethod
    def hash(password):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify(password, hashdigest):
        return pbkdf2_sha256.verify(password, hashdigest)
