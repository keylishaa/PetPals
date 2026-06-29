class User:
    def __init__(self, id_user, username, email, password, role):
        self._id_user = id_user
        self._username = username
        self._email = email
        self.__password = password  # Private Attribute - Data Hiding
        self._role = role

    @property
    def id_user(self): return self._id_user

    @property
    def username(self): return self._username

    @property
    def email(self): return self._email

    @property
    def role(self): return self._role

    def check_password(self, password_input):
        return self.__password == password_input

    def to_dict(self):
        return {
            'id_user': self._id_user,
            'username': self._username,
            'email': self._email,
            'password': self.__password,
            'role': self._role
        }


# Inheritance: Admin & Customer mewarisi struktur dari User
class Admin(User):
    def __init__(self, id_user, username, email, password):
        super().__init__(id_user, username, email, password, role='Admin')


class Customer(User):
    def __init__(self, id_user, username, email, password):
        super().__init__(id_user, username, email, password, role='Customer')