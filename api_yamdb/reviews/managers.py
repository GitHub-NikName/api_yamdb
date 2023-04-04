# from django.contrib.auth.base_user import BaseUserManager
#
#
# class UserManager(BaseUserManager):
#     """
#     Менеджер для модели пользователя.
#     """
#
#     def create_user(self, username, email, **extra_fields):
#         """Создает и возвращает пользователя"""
#
#         if not username:
#             raise TypeError('Users must have a username.')
#         if not email:
#             raise TypeError('Users must have an email address.')
#
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.save()
#         return user
#
#     def create_superuser(self, username, email, password, **extra_fields):
#         """ Создает и возвращает пользователя с привилегиями суперадмина. """
#
#         if password is None:
#             raise TypeError('Superusers must have a password.')
#
#         user = self.create_user(username, email, **extra_fields)
#         user.is_superuser = True
#         user.is_staff = True
#         user.set_password(password)
#         user.role = 'admin'
#         user.save()
#         return user
