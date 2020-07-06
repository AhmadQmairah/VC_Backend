from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Patient, Appointment, MedHistory


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(allow_blank=True, read_only=True)

    def validate(self, data):

        my_username = data.get('email')
        my_password = data.get('password')
        user_obj = None
        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError(
                "Incorrect username/password combination")
        payload = RefreshToken.for_user(user_obj)
        token = str(payload.access_token)

        data = {"access": token}

        return data


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        username = validated_data['username']
        password = validated_data['password']
        print(validated_data)
        # new_user = User(username=username)
        # new_user.set_password(password)
        # new_user.save()
        return validated_data


class AppSer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    booked_by = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_status(self, obj):
        try:
            return obj.booked_by.status
        except:
            return ""

    def get_booked_by(self, obj):
        try:
            return obj.booked_by.user.name
        except:
            return None

    def get_history(self, obj):
        try:
            return HisSer(obj.booked_by.user.history.all(), many=True).data
        except:
            return []


class DocSer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class HisSer(serializers.ModelSerializer):
    class Meta:
        model = MedHistory
        fields = "__all__"
