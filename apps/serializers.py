from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
# from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings
from apps.models import (
    User,
    Post,
    Category
)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'created_at', 'updated_at']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['name', 'email', 'token', 'created_at', 'updated_at']

    def get_token(self, obj):

        # 여기쯤에서 REDIS 연동을 하면 될것 같음

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(_('VALIDATE_ERROR'))

        if password is None:
            raise serializers.ValidationError(_('VALIDATE_ERROR'))

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(_('AUTHENTICATE_ERROR'))

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        user.last_login = timezone.now()
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    name = serializers.CharField(max_length=255)
    is_superuser = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        ignore_private = kwargs.pop('ignore_private', True)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if ignore_private:
            for field_name in ['is_superuser', 'is_active', 'deleted_at', 'groups', 'user_permissions']:
                self.fields.pop(field_name)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance

class PasswordChange(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, required=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'is_superuser', 'last_login', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        user = self.context.get('user', None)
        post = Post.objects.create(user=user, **validated_data)
        return post


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    depth = serializers.IntegerField(default=1)
    order = serializers.IntegerField(default=0, required=False)
    is_active = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = Category
        fields = ('id', 'parent', 'depth', 'name', 'is_active', 'order', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        user = self.context.get('user', None)
        category = Category.objects.create(user=user, **validated_data)
        return category
