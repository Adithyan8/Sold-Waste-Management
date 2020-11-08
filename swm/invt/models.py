from django.db import models
import uuid
from phone_field import PhoneField
class address(models.Model):
    House_Apt_Number=models.CharField(max_length=150,blank=False)
    Area=models.CharField(max_length=150,blank=False)
    Landmark=models.CharField(max_length=150,blank=True)
    city=models.CharField(max_length=50,blank=False)
    state=models.CharField(max_length=30,blank=False)
    zipcode=models.IntegerField(max_length=10,blank=False)
# Create your models here.
class TUser(address):
    User_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Full_Name=models.CharField(blank=False,max_length=50)
    email=models.EmailField(blank=False)
    contact=PhoneField(max_length=50,blank=False,help_text='Contact phone number')
    choices_gender=(
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
        ('OTHER','OTHER')
    )
    Gender=models.CharField(max_length=20,choices=choices_gender,blank=False)
    def __str__(self): 
         return self.Full_Name
class Waste(models.Model):
    Waste_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Tpuser= models.ForeignKey(TUser,on_delete=models.DO_NOTHING)
    choices_type=(
        ('Recyable','Recyable'),
        ('Non-Recyable','Non-Recyable')
    )
    Type=models.CharField(max_length=20,choices=choices_type,blank=False)
    created_date = models.DateField(default=timezone.now)
    Quantity=models.IntegerField(blank=False,null=False,max_length=100)

class Organisationaddress(models.Model):
    Area=models.CharField(max_length=150,blank=False)
    Landmark=models.CharField(max_length=150,blank=True)
    city=models.CharField(max_length=50,blank=False)
    state=models.CharField(max_length=30,blank=False)
    zipcode=models.IntegerField(max_length=10,blank=False)
class Processsingplant(Organisationaddress):
    pp_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PPName=models.CharField(blank=False,max_length=100)
    total_waste=models.IntegerField(blank=False,null=False,max_length=100)
    waste_recycled=models.IntegerField(blank=False,null=False,max_length=100)
    def get_lw(self):
        return self.total_waste-self.waste_recycled
    landfill_Waste=property(get_lw)
class Tv(models.Model):
    Tv_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date_Of_Collection = models.DateField(default=timezone.now)
    Plate_Number=models.CharField(blank=False,null=False,max_length=20)
    Capacity=models.IntegerField(blank=False,null=False,max_length=100)
    choices_permit=(
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
        ('OTHER','OTHER')
    )
    Permit=models.CharField(max_length=20,choices=choices_permit,blank=False)
    pp=models.ForeignKey(Processsingplant,on_delete=models.CASCADE)

class Landfill(Organisationaddress):
    lf_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    LFName=models.CharField(blank=False,max_length=100)
    maximum_capacity=models.IntegerField(blank=False,null=False,max_length=100)
    capacity_filled=models.IntegerField(blank=False,null=False,max_length=100)
    pp=models.ForeignKey(Processsingplant,on_delete=models.CASCADE)





    









    