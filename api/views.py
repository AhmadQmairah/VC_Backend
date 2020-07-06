
from datetime import datetime
import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from .serializers import UserCreateSerializer, UserLoginSerializer, AppSer, DocSer, HisSer
# from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User
from .models import Patient, Appointment, AppointmentBooking
from rest_framework_simplejwt.tokens import RefreshToken
from PIL import Image
import base64
from django.core.files.base import ContentFile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# class UserCreateAPIView(CreateAPIView):
#     serializer_class = UserCreateSerializer
from django.core.mail import send_mail


class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        try:
            user_obj = User.objects.get(username=email)
        except:
            return Response("Account does not exists", status=404)

        if not user_obj.check_password(password):
            return Response("Wrong Password", status=404)

        real_user = Patient.objects.get(user=user_obj)

        if(real_user.is_doctor):
            if real_user.doctor_verified == "Not Checked":
                return Response("You need to be approved before logging in", status=404)
            if real_user.doctor_verified == "Rejected":
                return Response("You Cant Access Because You Are Rejected", status=404)

        payload = RefreshToken.for_user(user_obj)
        print(dir(payload.access_token))
        payload.access_token["he"] = True
        token = str(payload.access_token)

        data = {"access": token, "is_doctor": real_user.is_doctor}

        print(data)
        return Response(data)


class UserCreateAPIView(APIView):
    def post(self, request):
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        civilID = request.data["civilID"]
        age = request.data["age"]
        address = request.data["address"]
        image = request.data.get("image")
        is_doctor = request.data.get("is_doctor")
        speciality = request.data.get("speciality")
        phone_number = request.data.get("phone_number")
        print(speciality)
        new_user = User(username=email)
        new_user.set_password(password)
        new_user.save()

        user = Patient.objects.create(user=new_user, age=age,
                                      civil_id=civilID, name=username, address=address, phone_number=phone_number)

        if(is_doctor):
            user.is_doctor = True
            user.dcctor_speciality = speciality
            if(image):
                image = CreateAndVerifyPicture(image)
                user.doctor_image = image

            user.save()
        return Response()


class getApp(APIView):
    def post(self, request):
        user = Patient.objects.get(user=request.user)
        if(user.is_doctor):
            return Response(AppSer(Appointment.objects.filter(
                doctor=user), many=True).data)

        return Response(AppSer(Appointment.objects.all(), many=True).data)


class get_doctors(APIView):
    def post(self, request):
        return Response(DocSer(Patient.objects.filter(is_doctor=True).exclude(id=31), many=True).data)


class change_doctor_status(APIView):
    def post(self, request):
        print(request.data)
        pat = Patient.objects.get(id=request.data["id"])
        pat.doctor_verified = request.data["radio"]
        pat.save()
        return Response()


class isDoctor(APIView):
    def post(self, request):
        user = Patient.objects.get(user=request.user)
        print(user)
        return Response(user.is_doctor)


class createApp(APIView):
    def post(self, request):

        app = Appointment.objects.create(
            time=request.data["time"], date=request.data["date"], end_time=request.data["end_time"],
            doctor=Patient.objects.get(user=request.user))
        print(request.data)
        return Response(AppSer(app).data)


class updateApp(APIView):
    def post(self, request):
        app = Appointment.objects.get(id=request.data["id"])
        app.time = request.data["time"]
        app.date = request.data["date"]
        app.save()
        print(request.data)
        return Response(AppSer(app).data)


class getHistory(APIView):
    def post(self, request):

        user = Patient.objects.get(user=request.user)
        print(user.history.all())
        # print(request.data)
        return Response(HisSer(user.history.all(), many=True).data)


class createHistory(APIView):
    def post(self, request):

        user = Patient.objects.get(user=request.user)
        user.history.create(description=request.data["description"])

        return Response()


class ChangeBook(APIView):
    def post(self, request):
        print("here")
        radio = request.data["radio"]
        fdr = request.data["fdr"]
        app = Appointment.objects.get(id=request.data["id"])
        print(app, app.booked_by.status)
        if(radio == "Forward"):
            app.doctor = Patient.objects.get(id=fdr)
            print("here xd")
        else:
            app.booked_by.status = radio

        app.booked_by.save()
        app.save()

        return Response()


class deleteApp(APIView):
    def post(self, request):
        print("hi")
        id = request.data["id"]
        app = Appointment.objects.get(id=id)
        app.booked_by = None
        app.save()
        return Response()


class bookApp(APIView):
    def post(self, request):
        id = request.data["id"]
        image = request.data["image"]
        app = Appointment.objects.get(id=id)
        booking = AppointmentBooking.objects.create(
            user=Patient.objects.get(user=request.user), description=request.data["description"])
        if(image):
            image = CreateAndVerifyPicture(image)
            booking.image = image
            booking.save()

        app.booked_by = booking

        # print(dir(booking.time), dir(booking.date))
        test = datetime.combine(app.date,
                                app.time)
        diff = test-datetime.now()

        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print(hours)
        if(hours <= 2):
            print("sending")
            send_mail(
                'You have an appointment',
                'Your Appointment is at '+str(app.time),
                'frm',
                ['to'],
                fail_silently=False,
            )
        app.save()
        return Response()


class delApp(APIView):
    def post(self, request):

        booking = AppointmentBooking.objects.create(
            user=Patient.objects.get(user=request.user), description=request.data["description"])

        app.save()
        return Response()


class get_my_appointments(APIView):
    def post(self, request):
        user = Patient.objects.get(user=request.user)

        # app = Appointment.objects.filter(id=id, booked_by_user_id=user.id)
        app = AppointmentBooking.objects.filter(user=user)
        app = Appointment.objects.filter(booked_by__in=app)

        return Response(AppSer(app, many=True).data)


def CreateAndVerifyPicture(picture):
    try:
        image = picture["imageUrl"]
        image_name = picture["name"].split(".")[0]
        format, imgstr = image.split(';base64,')
        ext = format.split('/')[-1]
        picture = ContentFile(base64.b64decode(
            imgstr), name='{}.'.format(image_name) + ext)  # Converted base64 to image

        trial_image = Image.open(picture)  # Verifying
        trial_image.load()
        if hasattr(picture, 'reset'):
            picture.reset()

        trial_image = Image.open(picture)
        trial_image.verify()

        return picture
    except Exception as e:
        print(e)
        return None


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @ classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
