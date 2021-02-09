from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerifyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


__all__ = ['EmailVerifyTokenGenerator', 'PasswordResetTokenGenerator']
