from django.db import models
from django.contrib.auth.models import User

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
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
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
