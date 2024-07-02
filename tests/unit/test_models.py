"""
This file (test_models.py) contains the unit tests for the users.py file.
"""
import unittest

from project.models.user import User # pylint: disable=import-error
from project.exceptions.UserConsentRevoked import UserConsentRevoked # pylint: disable=import-error


class TestUserModel(unittest.TestCase):
    """ Unit test suite for User model"""


    def setUp(self):
        "Mandatory method"
        self.new_user = User('test@example.com',  'password123', True)


    def test_new_user_print_conversion(self):
        """GIVEN a User model
        WHEN a new User is created
        THEN check the email, password, authenticated, and active fields
        are defined correctly
        """

        user = self.new_user
        assert str(user) == '<User: test@example.com>'


    def test_new_user_with_fixture(self):
        """GIVEN a User model
        WHEN a new User is created
        THEN check the email and password fields are defined correctly
        """

        assert self.new_user.email == 'test@example.com'
        assert self.new_user.password != 'password123'


    def test_setting_password(self):
        """GIVEN an existing User
        WHEN the password for the user is set
        THEN check the password is stored correctly and not as plaintext
        """

        self.new_user.password = 'MyNewPassword'

        assert self.new_user.password != 'MyNewPassword'
        assert self.new_user.is_password_correct('MyNewPassword')
        assert not self.new_user.is_password_correct('password123')
        assert not self.new_user.is_password_correct('MyNewPassword2')
        assert not self.new_user.is_password_correct('FlaskIsAwesome')


    def test_is_user_id_protected(self):
        """GIVEN an existing User
        WHEN the ID of the user is reassigned
        THEN we expect an error/exception
        """
        # pylint: disable=invalid-name
        with self.assertRaises((AttributeError)) as context:
            user = self.new_user
            user.id = 17
        # pylint: enable=invalid-name

        self.assertEqual(
            str(context.exception),
            "property 'id' of 'User' object has no setter"
        )


    def test_new_user_memo(self):
        """GIVEN a User model
        WHEN a new User is created
        THEN check the memo fields is not defined
        """

        assert self.new_user.memo is None


    def test_user_memo_update(self):
        """GIVEN a User model
        WHEN the memo is updated
        THEN check the user memo returns a new string
        """

        assert self.new_user.memo is None

        self.new_user.memo = "User related note"

        assert self.new_user.memo is not None
        assert self.new_user.memo == "User related note"


    def test_new_user_is_not_verified(self):
        """GIVEN a User model
        WHEN the email_verified_at of the user is nod defined by default
        THEN check the user email_verified_at returns a None
        """

        assert self.new_user.email_verified_at is None


    def test_user_email_verified(self):
        """GIVEN a User model
        WHEN the User verified()
        THEN check the user email_verified_at returns a not None
        """

        assert self.new_user.email_verified_at is None

        self.new_user.set_email_verified()

        assert self.new_user.email_verified_at is not None


    def test_new_user_is_not_updated_at(self):
        """GIVEN a User model
        WHEN freshly created
        THEN check the user updated_at returns a None
        """

        assert self.new_user.updated_at is None


    def test_new_user_is_updated_at(self):
        """GIVEN a new User model
        WHEN memo value is updated
        THEN check the user updated_at returns a not None
        """

        assert self.new_user.updated_at is None

        self.new_user.memo = 'Test Updated_at'

        assert self.new_user.updated_at is not None


    def test_new_user_consent(self):
        """GIVEN a User model
        WHEN freshly created
        THEN check the user consent is true
        """

        assert self.new_user.consent


    def test_user_consent_change(self):
        """GIVEN a User model
        WHEN freshly created
        THEN check the user consent is true
        """

        with self.assertRaises((UserConsentRevoked)) as context:
            self.new_user.consent = False

        self.assertEqual(str(context.exception), "User consent revoked")


    def test_user_id_is_integer(self):
        """GIVEN a User model
        WHEN freshly created
        THEN check the user id type is int
        """

        assert not isinstance(self.new_user.id, int)


    def test_user_name(self):
        """GIVEN a User model
        WHEN freshly created
        THEN name is None
        """

        assert self.new_user.name == ''


    def test_user_name_update(self):
        """GIVEN a User model
        WHEN update name
        THEN name is updated
        """

        assert self.new_user.name == ''
        self.new_user.name = "Test user"
        assert self.new_user.name == "Test user"


    def test_creating_user_without_consent(self):
        """GIVEN a User model
        WHEN user provide no consent
        THEN model throw an exception during creation
        """

        with self.assertRaises(ValueError) as context:
            User('test@example.com',  'password123', False)

        # Check the error message in the raised exception
        self.assertEqual(str(context.exception), "Cannot add user without consent")


    def test_revoke_user_consent(self):
        """GIVEN a User model
        WHEN user provide no consent
        THEN model throw an exception during creation
        """

        user = User('test@example.com',  'password123', True)

        with self.assertRaises(UserConsentRevoked) as context:
            user.consent = False

        # Check the error message in the raised exception
        self.assertEqual(str(context.exception), "User consent revoked")
