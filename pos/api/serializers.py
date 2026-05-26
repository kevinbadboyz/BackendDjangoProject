from rest_framework import serializers
from pos_app.models import StatusModel, TableResto, Category, MenuResto, Order, OrderDetail
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
    status = serializers.CharField(source = 'status.name', read_only = True)
    # status = StatusModelSerializer()

    class Meta:
        model = Category
        fields = ('id', 'name', 'status')
        # fields = '__all__'
        # depth = 1

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'status', 'user_create')

class MenuRestoSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source = 'category.name', read_only = True)
    status = serializers.CharField(source = 'status.name', read_only = True)
    
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

class OrderDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('id', 'order', 'menu_resto', 'quantity', 'subtotal')

class OrderCreateSerializer(serializers.ModelSerializer):
    order_order_detail = OrderDetailCreateSerializer(many = True)

    class Meta:
        model = Order
        fields = ('id', 'code', 'table_resto', 'user', 'order_order_detail', 'order_status', 'total_order', 
            'tax_order', 'total_payment', 'user_create')
    
    def create(self, validated_data):
        order_items = validated_data.pop('order_order_detail')
        order = Order.objects.create(**validated_data)

        # Save OrderItem multi times
        total_order = 0
        for order_item in order_items:
            oi = OrderDetail.objects.create(order = order, **order_item)
            oi.subtotal = oi.menu_resto.price * oi.quantity
            oi.status = StatusModel.objects.first()
            total_order += oi.subtotal
            oi.user_create = order.user_create
            oi.save()
        
        # Update the TableResto into Occupied
        TableResto.objects.filter(id = order.table_resto.id).update(table_status = 'Terisi')

        # Save Order
        order.total_order = total_order
        order.tax_order = 0.12 * float(total_order)
        order.total_payment = order.total_order + order.tax_order
        order.user = order.user_create
        order.save()
        return order
    
class OrderSerializer(serializers.ModelSerializer):
    table_resto = serializers.CharField(source = 'table_resto.name', read_only = True)

    class Meta:
        model = Order
        fields = ('id', 'code', 'table_resto', 'user', 'order_status', 'total_order', 
            'tax_order', 'total_payment', 'user_create')
        
class OrderInfoSerializer(serializers.ModelSerializer):
    table_resto = serializers.CharField(source = 'table_resto.name', read_only = True)
    order_order_detail = OrderDetailCreateSerializer(many = True)

    class Meta:
        model = Order
        fields = ('id', 'code', 'table_resto', 'user', 'order_status', 'order_order_detail', 'total_order', 
            'tax_order', 'total_payment', 'user_create')
