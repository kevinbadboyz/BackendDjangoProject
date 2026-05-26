from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

def convert_to_roman(number):    
    if number == str(1):
        roman = 'I'
    elif number == str(2):
        roman = 'II'
    elif number == str(3):
        roman = 'III'
    elif number == str(4):
        roman = 'IV'
    elif number == str(5):
        roman = 'V'
    elif number == str(6):
        roman = 'VI'
    elif number == str(7):
        roman = 'VII'
    elif number == str(8):
        roman = 'VIII'
    elif number == str(9):
        roman = 'IX'
    elif number == str(10):
        roman = 'X'
    elif number == str(11):
        roman = 'XI'
    elif number == str(12):
        roman = 'XII'
    return roman

def convert_to_number(roman):
    if roman == 'I':
        number = int(1)
    elif roman == 'II':
        number = int(2)
    elif roman == 'III':
        number = int(3)
    elif roman == 'IV':
        number = int(4)
    elif roman == 'V':
        number = int(5)
    elif roman == 'VI':
        number = int(6)
    elif roman == 'VII':
        number = int(7)
    elif roman == 'VIII':
        number = int(8)
    elif roman == 'IX':
        number = int(9)
    elif roman == 'X':
        number = int(10)
    elif roman == 'XI':
        number = int(11)
    elif roman == 'XII':
        number = int(12)
    return number

class StatusModel(models.Model):
    status_choices = (
        ('Aktif','Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
	)            
    name = models.CharField(max_length = 50, unique = True)
    description = models.TextField(blank = True, null = True)
    status = models.CharField(max_length = 15, 
        choices = status_choices, default = 'Aktif')
    user_create = models.ForeignKey(User, 
        related_name = 'user_create_status_model', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, 
        related_name = 'user_update_status_model', 
        blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.name)

class TableResto(models.Model):
    table_status_choices = (
        ('Kosong', 'Kosong'),
        ('Terisi', 'Terisi'),
    )
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Non-Aktif', 'Non-Aktif'),
    )
    code = models.CharField(max_length = 10, unique = True)
    name = models.CharField(max_length = 100)
    capacity = models.IntegerField(default = 0)
    table_status = models.CharField(max_length = 10, 
        choices = table_status_choices, default = 'Kosong')
    status = models.CharField(max_length = 10, 
        choices = status_choices, default = 'Aktif')
    user_create = models.ForeignKey(User, on_delete = models.SET_NULL, 
        null = True, blank = True, 
        related_name = 'user_create_table_resto')
    user_update = models.ForeignKey(User, on_delete = models.SET_NULL, 
        null = True, blank = True,
        related_name = 'user_update_table_resto')
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Category(models.Model):    
    name = models.CharField(max_length = 100)    
    status = models.ForeignKey(StatusModel, related_name = 'status_category', 
        on_delete = models.PROTECT)    
    user_create = models.ForeignKey(User, related_name = 'user_create_category', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_category', 
        blank = True, null = True, on_delete = models.SET_NULL)
    # created_on = models.DateTimeField(blank = True, null = True)
    # last_modified = models.DateTimeField(blank = True, null = True)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class MenuResto(models.Model):    
    status_menu_choices = (
        ('Ada','Ada'),
        ('Habis', 'Habis'),
	)        
    code = models.CharField(max_length = 20, unique = True)
    name = models.CharField(max_length = 100)    
    price = models.FloatField(default = 0)
    description = models.CharField(max_length = 200)    
    image_menu = models.ImageField(default = None, upload_to = 'menu_images/', blank = True, null = True)    
    category = models.ForeignKey(Category, related_name = 'category_menu', blank = True, null = True, on_delete = models.SET_NULL)
    menu_status = models.CharField(max_length = 15, choices = status_menu_choices, default = 'Ada')
    status = models.ForeignKey(StatusModel, related_name = 'status_menu', on_delete = models.PROTECT)    
    user_create = models.ForeignKey(User, related_name = 'user_create_menu', blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_menu', blank = True, null = True, on_delete = models.SET_NULL)
    # created_on = models.DateTimeField(blank = True, null = True)
    # last_modified = models.DateTimeField(blank = True, null = True)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

def increment_order_menu_code():
    last_id = Order.objects.all().last()        
    m = convert_to_roman(str(datetime.today().month))

    if not last_id:
        return '0001' + '-OM-' + m + '-' + str(datetime.today().year)
    else:
        code = last_id.code
        code_first, code_middle_1, code_middle_2, code_last = code.split("-")    
        y = int(code_last[0:4]) 
        M = convert_to_number(code_middle_2)

        if ((M == datetime.today().month) & (y == datetime.today().year)):
            code_int = int(code_first[0:4])
            new_code_int = code_int + 1
            return str(new_code_int).zfill(4)+ '-OM-' + m + '-' + str(datetime.today().year)
        elif ((M != datetime.today().month) | (y != datetime.today().year)):
            return '0001' + '-OM-' + m + '-' + str(datetime.today().year)

class Order(models.Model):
    status_order_status_choices = (
        ('Belum Bayar','Belum Bayar'),
        ('Sudah Bayar', 'Sudah Bayar'),
	) 
    code = models.CharField(max_length = 20, default = increment_order_menu_code, editable = False)
    table_resto = models.ForeignKey(TableResto, related_name = 'table_resto_order', 
        blank = True, null = True, on_delete = models.SET_NULL)    
    user = models.ForeignKey(User, related_name = 'user_order', 
        blank = True, null = True, on_delete = models.SET_NULL)
    order_status = models.CharField(max_length = 20, choices = status_order_status_choices, 
        default = 'Belum Bayar')
    total_order = models.FloatField(default = 0, blank = True, null = True)
    tax_order = models.FloatField(default = 0, blank = True, null = True)
    total_payment = models.FloatField(default = 0, blank = True, null = True)
    user_create = models.ForeignKey(User, related_name = 'user_create_order', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_order', 
        blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.code}'
    
class OrderDetail(models.Model):    
    status_order_detail_choices = (
        ('Sedang disiapkan','Sedang disiapkan'),
        ('Sudah disajikan', 'Sudah disajikan'),
	)
    order = models.ForeignKey(Order, related_name = 'order_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    menu_resto = models.ForeignKey(MenuResto, related_name = 'menu_resto_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    quantity = models.IntegerField(default = 0)
    subtotal = models.IntegerField(default = 0, blank = True, null = True)
    description =  models.CharField(max_length = 200, blank = True, null = True)
    order_detail_status = models.CharField(max_length = 30, 
        choices = status_order_detail_choices, default = 'Sedang disiapkan')
    status = models.ForeignKey(StatusModel, related_name = 'status_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_create = models.ForeignKey(User, related_name = 'user_create_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.order}'

    def get_subtotal(self):                
        return self.quantity * self.menu_resto.price 

    # @staticmethod
    def get_total(self, order_id):
        total = 0
        for item in self.order.object.filter(order__id = order_id):
            total += item.get_subtotal()
        return total
