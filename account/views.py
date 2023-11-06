from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import random
import datetime

from django.core.mail import send_mail
# from .permissions import IsFieldOwnerOrReadOnly
from .models import UserModel
from .serializer import UserRegistrationSerializer, UserSerializer
from account_rest_auth.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from rest_framework.authtoken.models import Token
from django.utils.encoding import smart_str

class UserRegistrationView(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserRegistrationSerializer
   

    @action(detail=False, methods=["POST"])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        # print(serializer)
        # print("email : ", request.data['email'])
        if serializer.is_valid():
            user = serializer.save()
            from_email = settings.EMAIL_HOST_USER
            recipient_email = request.data['email']  
            user = UserModel.objects.get(email=request.data['email'] )
            subject = 'Your OTP for Account Verification'
            email_context = {'otp': user.otp}
            html_content = render_to_string('otp_email.html', email_context)
            # Create the email message
            text_content = strip_tags(html_content)  # Plain text version of the HTML email
            email = EmailMultiAlternatives(subject, text_content, from_email, [recipient_email])
            email.attach_alternative(html_content, "text/html")  # Attach the HTML content

            # Send the email
            email.send()
            # context = {'otp': user.otp}
            # email_body = render_to_string('otp_email.html', context)
            # subject = 'Your OTP for Account Verification'
            # from_email = settings.EMAIL_HOST_USER
            # recipient_email = request.data['email']  
            # send_mail(subject, email_body, from_email, [recipient_email], fail_silently=False)
            return Response({'message': 'OTP sent to your email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #     text_content = strip_tags(html_content)  
        #     email = EmailMultiAlternatives(subject, text_content, from_email, [recipient_email])
        #     email.attach_alternative(html_content, "text/html") 
        #     email.send()
        #     return render(request, 'registration_success.html')
        # return render(request, 'registration_form.html', {'errors': serializer.errors})
        #     return Response({'message': 'OTP sent to your email'}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["PATCH"])
    def verify_otp(self, request):
        instance_data = request.data
        email = instance_data.get('email')
        otp = instance_data.get('otp')

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        if user.otp == str(instance_data['otp']):
            user.otp_verified = True
            user.is_active = True
            user.otp_expiry = None
            user.max_otp_try = settings.MAX_OTP_TRY
            user.otp_max_out = None
            user.save()
            return Response(
                "Successfully verified the user and Active your account.", status=status.HTTP_200_OK
            )

        return Response(
            "Please enter the correct OTP.",
            status=status.HTTP_400_BAD_REQUEST,
        )
        # if user.otp == otp:
        #     user.otp_verified = True
        #     user.is_active = True
        #     user.otp_expiry = None
        #     user.max_otp_try = settings.MAX_OTP_TRY
        #     user.otp_max_out = None
        #     user.save()
        #     return Response("Successfully verified the user.", status=status.HTTP_200_OK)
        # else:
        #     return Response("Invalid OTP .", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["PATCH"])
    def profile_update(self, request):
        instance_data = request.data
        email= instance_data.get('email')
        phone_number = instance_data.get('phone_number')
        username = instance_data.get('username')
        password = instance_data.get('password1')
        first_name = instance_data.get('first_name')
        last_name = instance_data.get('last_name')

        if not email or not password:
            return Response("Email and password are required", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def regenerate_otp(self, request):
        instance_data = request.data
        email = instance_data.get('email')

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        if int(user.max_otp_try) == 0 and timezone.now():
            return Response("Max OTP try reached, try after an hour", status=status.HTTP_400_BAD_REQUEST)

        otp = random.randint(100000, 999999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(user.max_otp_try) - 1

        user.otp = otp
        user.otp_expiry = otp_expiry
        user.max_otp_try = max_otp_try
        if max_otp_try == 0:
            otp_max_out = timezone.now() + datetime.timedelta(minutes=60)
            user.otp_max_out = otp_max_out
        elif max_otp_try == -1:
            user.max_otp_try = settings.MAX_OTP_TRY
        else:
            user.otp_max_out = None
        user.save() 

        return Response("Successfully generated a new OTP.", status=status.HTTP_200_OK)






class CustomLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            print(token)
            # token, created = Token.objects.get_or_create(user=user)  # Create or retrieve the token for the user
            return Response({'token': token})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


