"""
    User DB entity
"""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import class_mapper
from werkzeug.security import check_password_hash, generate_password_hash
from project import db

from project.exceptions.UserConsentRevoked import UserConsentRevoked

# pylint: disable=too-many-instance-attributes
class User(db.Model):
    """
    A User of the application

    The following attributes of a user are stored in this table:
        * email - user email
        * email_verified_at - when email was verified
        * password - Hashed user password
        * remember_token - "Remember Me" cookie hijacking preventing token
        * created_at - when user record was created
        * updated_at - when user record was updated
        * memo - user related note
    """

    __tablename__ = 'users'

    _id                 = db.Column('id', Integer(), primary_key=True, autoincrement=True)
    _email              = db.Column('email', String(), unique=True, nullable=False)
    _name               = db.Column('name', db.String(100), nullable=False)
    _email_verified_at  = db.Column('email_verified_at', DateTime(), nullable=True)
    _password           = db.Column('password', String(128), nullable=True)
    _remember_token     = db.Column('remember_token', String(), nullable=True)
    _created_at         = db.Column('created_at', DateTime(), nullable=False)
    _updated_at         = db.Column('updated_at', DateTime(), nullable=True)
    _memo               = db.Column('memo', String(), nullable=True)
    _consent            = db.Column('consent', Boolean(), nullable=False)

    _hidden_columns = ['password']

    def __init__(self, email: str, password: str, consent: bool, name: str = ''):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """

        if not consent:
            raise ValueError("Cannot add user without consent")

        self._email = email
        self._password = self._generate_password_hash(password) if not password is None else None
        self._created_at = datetime.now()
        self._consent = consent
        self._name = name

    @property
    # pylint: disable=invalid-name
    def id(self):
        """return user ID
            :rtype: int
        """
        return self._id

    @property
    def name(self):
        """return user name
            :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """ Update user name
            :param value: new user name
            :type value: str
        """
        self._name = value
        self._after_setter_called()

    @property
    def updated_at(self):
        """
            :return: The updated_at value as a DateTime object.
            :rtype: datetime.datetime
        """
        return self._updated_at

    @property
    def email_verified_at(self):
        """
            :return: when user email was verified
            :rtype: datetime.datetime
        """
        return self._email_verified_at

    def set_email_verified(self):
        """
            Handle, user email confirmation
        """
        self._email_verified_at = datetime.now()
        self._after_setter_called()

    @property
    def email(self):
        """
            :return: user email
            :rtype: str
        """
        return self._email

    @email.setter
    def email(self, value):
        """
            Update user e-mail

            :param value: new user e-mail
            :type value: str
        """
        self._email = value
        self._after_setter_called()

    @property
    def memo(self):
        """
            :return: user related memo note
            :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, value):
        """
            Update user related memo note

            :param value: new user memo
            :type value: str
        """
        self._memo = value
        self._after_setter_called()

    @property
    def password(self):
        """
            :return: user password hash
            :rtype: str
        """
        return self._password

    @password.setter
    def password(self, value):
        """
            Update user password

            :param value: new user password
            :type value: str
        """
        self._password = self._generate_password_hash(value) if not value is None else None
        self._after_setter_called()

    @property
    def consent(self):
        """
            :return: user consent
            :rtype: bool
        """
        return self._consent

    @consent.setter
    def consent(self, value : bool):
        """
            Update user consent, when false should be deleted

            Raises: UserConsentRevoked

            :param value: new user consent
            :type value: bool
        """

        if value is False:
            raise UserConsentRevoked()

        self._consent = value
        self._after_setter_called()

    @property
    def remember_token(self):
        """
            :return: user remember token
            :rtype: str
        """
        return self._remember_token

    @remember_token.setter
    def remember_token(self, value : str):
        """
            Update user remember token

            :param value: new user remember token
            :type value: str
        """
        self._remember_token = value
        self._after_setter_called()

    @property
    def created_at(self):
        """
            :return: when user record been created
            :rtype: datetime.datetime
        """
        return self._created_at

    def is_password_correct(self, password_plaintext: str):
        """
            :param password_plaintext: Password to check
            :type password_plaintext: str

            :return: is password match
            :rtype: bool
        """
        return check_password_hash(self._password, password_plaintext)

    def _after_setter_called(self):
        """
            :return: when user record been updated
            :rtype: datetime.datetime
        """
        self._updated_at = datetime.now()

    @staticmethod
    def _generate_password_hash(password_plaintext):
        """
            :param password_plaintext: Password to hash
            :type password_plaintext: str

            :return: hash string for password
            :rtype: str
        """
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self._email}>'

    def to_dict(self):
        """
            Create a dictionary representation of the model instance, excluding
            all columns defined in _hidden_columns property

            :return: user entity related columns in a dictionary
            :rtype: dict
        """
        columns = [c.key for c in class_mapper(self.__class__).columns]

        return {col: getattr(self, col) for col in columns if col not in self._hidden_columns}
