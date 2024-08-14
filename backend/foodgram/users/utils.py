from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator

from foodgram.settings import DEFAULT_EMAIL


def generate_and_send(email, username, user):
    """Генерирует код подтверждения и отправляет на почту"""

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        subject='Код подтверждения',
        message=(f'Зравствуйте {username}, \n'
                 + 'Для подтверждения регистрации введите код.'
                 + f'\n Ваш код {confirmation_code}'),
        from_email=DEFAULT_EMAIL,
        recipient_list=[email],
    )
    return confirmation_code


def generate_confirmation_code(user):
    """Генерирует код подтверждения"""

    confirmation_code = default_token_generator.make_token(user)

    return confirmation_code


def send_confirmation_code(email, username, user):


    return send_mail(
        subject='Код подтверждения',
        message=(f'Зравствуйте {username}, \n'
                 + 'Для подтверждения регистрации введите код.'
                 + f'\n Ваш код {user.confirmation_code}'),
        from_email=DEFAULT_EMAIL,
        recipient_list=[email],
    )
