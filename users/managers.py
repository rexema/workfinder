from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    """
    Пользовательская модель менеджера пользователей.
    В качестве уникального идентификатора вместо имени пользователя используется email
    """

    def create_user(self, email, password, **kwargs):
        """
        Создаем и сохраняем пользователя с введенным email и паролем.
        :param email:
        :param password:
        :param kwargs:
        :return:
        """
        if not email:
            raise ValueError('Не указан email')
        if not password:
            raise ValueError('Не указан пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Создаем и сохраняем суперпользователя.
        :param email:
        :param password:
        :param kwargs:
        :return:
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь статус is_staff=True'
            )
        if kwargs.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь статус is_superuser=True'
            )
        return self.create_user(email, password, **kwargs)
