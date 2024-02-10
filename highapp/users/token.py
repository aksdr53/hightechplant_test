from django.contrib.auth.tokens import PasswordResetTokenGenerator 
import six


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for generating tokens for account activation.

    This class inherits from Django's PasswordResetTokenGenerator and provides
    a custom implementation for generating hash values used in email activation tokens.

    Methods:
    - _make_hash_value(self, user, timestamp): Generates a hash value based on the user's
      primary key, timestamp, and user's activation status.
    """
    def _make_hash_value(self, user, timestamp): 
        """
        Generates a hash value for the given user and timestamp.

        Parameters:
        - user: The user object for whom the token is generated.
        - timestamp: The timestamp when the token is generated.

        Returns:
        - str: The hash value based on user's primary key, timestamp, and activation status.
        """
        return( 
            six.text_type(user.pk) + six.text_type(timestamp) + 
            six.text_type(user.is_active) 
        ) 
account_activation_token = TokenGenerator() 