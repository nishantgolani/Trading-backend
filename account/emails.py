from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User


def send_otp_via_email(email):
    subject='your account verification email'
    otp = random.randint(000000, 999999)
    message = f'your otp is {otp}'
    email_from =settings.EMAIL_HOST
    send_mail(subject, message, email_from, ['nngolani2002@gmail.com'])
    print(send_mail(subject, message, email_from, ['nngolani2002@gmail.com']))
    user_obj =User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
    print(user_obj.save())