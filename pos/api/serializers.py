from rest_framework import serializers
from pos_app.models import StatusModel, TableResto, Category, MenuResto
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name', 'last_name')
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required' : True},
            'password' : {'write_only' : True}
        }

    def create(self, validated_data):
        # Both script code belo can running well
        # user = User.objects.create(
        #     username = validated_data['username'],
        #     email = validated_data['email'],
        #     first_name = validated_data['first_name'],
        #     last_name = validated_data['last_name']
        # )
        # user.set_password(validated_data['password'])
        # user.save()

        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user

class StatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusModel
        fields = ('id', 'name')

class TableRestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableResto
        # fields = '__all__'
        fields = ('id', 'code', 'name', 'capacity', 'table_status', 'status')

class CategorySerializer(serializers.ModelSerializer):
    # status = serializers.CharField(source = 'status.name', read_only = True)
    status = StatusModelSerializer()

    class Meta:
        model = Category
        fields = ('id', 'name', 'status')
        # fields = '__all__'
        # depth = 1

class MenuRestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuResto
        fields = ('id', 'code', 'name', 'price', 'description', 'image_menu', 
            'category', 'menu_status', 'status')
        
class MenuRestoFilterSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source = 'category.name', read_only = True)
    status = serializers.CharField(source = 'status.name', read_only = True)

    class Meta:
        model = MenuResto
        fields = ('id', 'code', 'name', 'price', 'description', 'image_menu', 
            'category', 'menu_status', 'status')
