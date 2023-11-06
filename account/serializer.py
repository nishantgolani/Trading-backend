from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.conf import settings
import random
from datetime import datetime, timedelta
import string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

# Import the User model
UserModel = get_user_model()

# def generate_unique_username(email, phone_number):
#     base_username = phone_number.lower() + email.split('@')[0].lower()

#     if not UserModel.objects.filter(username=base_username).exists():
#         return base_username

#     random_string = ''.join(random.choices(
#         string.ascii_lowercase + string.digits, k=5))
#     unique_username = base_username + random_string

#     while UserModel.objects.filter(username=unique_username).exists():
#         random_string = ''.join(random.choices(
#             string.ascii_lowercase + string.digits, k=5))
#         unique_username = base_username + random_string

class UserRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        email = validated_data['email']
        username = validated_data['username']
        if UserModel.objects.filter(phone_number=phone_number).exists():
            raise ValueError("Phone number already exists.")
        elif UserModel.objects.filter(email=email).exists():
            raise ValueError("Email already exists.")
        elif UserModel.objects.filter(username=username).exists():
            raise ValueError("Username already exists.")
        else:
            print(UserModel.objects.filter(username=username).exists(),"True")
            otp = random.randint(100000, 999999)
            otp_expiry = datetime.now() + timedelta(minutes=10)
            # username = generate_unique_username(email, phone_number)
            user = UserModel(
                phone_number=phone_number,
                email=email,
                username=username,
                otp=otp,
                otp_expiry=otp_expiry,
                max_otp_try=settings.MAX_OTP_TRY
            )
            user.save()
            
            # Sending OTP email
            # destination = email
            # subject = 'MU OTP Verification'
            # context = {
            #     'otp': otp,
            # }
            # html_content = render_to_string('otp.html', context)
            # text_content = strip_tags(html_content)

            # email = EmailMultiAlternatives(
            #     subject=subject,
            #     body=text_content,
            #     from_email=settings.EMAIL_HOST_USER,
            #     to=[destination],
            # )
            # email.attach_alternative(html_content, "text/html")
            # email.send()
            return user

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "Password must be longer than {} characters".format(
                settings.MIN_PASSWORD_LENGTH
            )
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "Password must be longer than {} characters".format(
                settings.MIN_PASSWORD_LENGTH
            )
        },
    )

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2"
        )
        read_only_fields = ("id",)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        phone_number = validated_data["phone_number"]
        email = validated_data["email"]
        username = validated_data["username"]
        otp = random.randint(1000, 9999)
        otp_expiry = datetime.now() + timedelta(minutes=10)
        # username = generate_unique_username(email, phone_number)
        user = UserModel(
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            username=validated_data["username"],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY
        )
        user.set_password(validated_data["password1"])
        user.save()
        
        # Sending OTP email
        # subject = "OTP Verification"
        # message = f"Your OTP is: {otp}"
        # from_email = settings.EMAIL_HOST_USER
        # recipient_list = [validated_data["email"]]
        # send_mail(subject, message, from_email, recipient_list)
        return user


