from django.db import models
from django.db import connection
from phonenumber_field.modelfields import PhoneNumberField



class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    ph_no=PhoneNumberField(blank=True)
    msg=models.TextField(max_length=500)
    def __str__(self):
        return self.name
    class Meta:
        db_table="contact_form"
 

class Myadm(models.Model):
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=200,default='')
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to='images/',default='')
    def __str__(self):
        return self.name
    class Meta:
        db_table="Adm_handle"
       
class Order(models.Model):
     id= models.AutoField(primary_key=True)
     item=models.CharField(max_length=200,default='')
     price=models.IntegerField(default=0)   
     name=models.CharField(max_length=200,default='') 
     email=models.EmailField(max_length=200)
     ph_no=PhoneNumberField(blank=True)
     address=models.CharField(max_length=200,default='')
     city=models.CharField(max_length=200,default='')
     def __str__(self):
        return self.item 
     class Meta:
        db_table="Order_db"
           
