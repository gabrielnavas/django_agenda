from typing import Union


class User():
    EMPTY_VALUES = 'Alguns campos obrigatórios estão em branco.'

    def __init__(self, name, last_name, username, email, password, password_confirmation):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.password_confirmation = password_confirmation
        self.username = username
        self.__verify_valid_empty_data()

    def __verify_valid_empty_data(self) -> None:
        errors = []
        inputs_obrigatory = {
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'password_confirmation': self.password_confirmation
        }
        for input_name, value in inputs_obrigatory.items():
            if not value or value == None:
                raise Exception(self.EMPTY_VALUES)


class RegisterUserUsecase:

    EMAIL_WRONG = 'Email já cadastrado de usuário já existe.'
    USERNAME_HAS_EXISTS = 'Nome de usuário já está em uso.'
    EMAIL_HAS_EXISTS = 'Já existe usuário com esse email'

    def __init__(self, validate_email, user_repository):
        self.__validate_email = validate_email
        self.__user_repository = user_repository

    def handle(self, user: User) -> None:
        self.__verify_valid_email(user.email)
        self.__password_verify_correct(
            user.password, user.password_confirmation)
        self.__verify_username_exists(user.username)
        self.__verify_email_exists(user.email)
        self.__user_repository.create(
            first_name=user.name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            password=user.password,
        )

    def __verify_email_exists(self, email):
        if self.__user_repository.filter(email=email).exists():
            raise Exception(self.EMAIL_WRONG)

    def __verify_username_exists(self, username):
        if self.__user_repository.filter(username=username).exists():
            raise Exception(self.USERNAME_HAS_EXISTS)

    def __verify_valid_email(self, email) -> None:
        try:
            self.__validate_email(email)
        except Exception as e:
            raise Exception(self.EMAIL_HAS_EXISTS)

    def __password_verify_correct(self, password: str, password_confirmation: str) -> None:
        if len(password) < 4:
            raise Exception('Senha não pode ser menor que 4.')
        if len(password) > 50:
            raise Exception('Senha muito grande.')
        if len(password_confirmation) < 4:
            raise Exception('Confirmação de senha não pode ser menor que 4.')
        if len(password_confirmation) > 50:
            raise Exception('Confirmação de senha muito grande.')
        if password != password_confirmation:
            raise Exception('Senha está diferente da confirmação de senha.')
