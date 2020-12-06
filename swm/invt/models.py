from django.db import models
import uuid
from phone_field import PhoneField
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator


class Address(models.Model):
    area=models.CharField(max_length=150,blank=False)
    landmark=models.CharField(max_length=150,blank=True)
    city=models.CharField(max_length=50,blank=False)
    state=models.CharField(max_length=30,blank=False)
    zipcode=models.IntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)],blank=False)

class TUser(Address):
    user_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name=models.CharField(blank=False,max_length=50)
    email=models.EmailField(blank=False)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    choices_gender=(
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
        ('OTHER','OTHER')
    )
    gender=models.CharField(max_length=20,choices=choices_gender,blank=False)
    def __str__(self): 
         return self.full_name

class OrganisationAddress(models.Model):
    area=models.CharField(max_length=150,blank=False)
    landmark=models.CharField(max_length=150,blank=True)
    city=models.CharField(max_length=50,blank=False)
    state=models.CharField(max_length=30,blank=False)
    zipcode=models.IntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)],blank=False)

class ProcesssingPlant(OrganisationAddress):
    pp_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ppname=models.CharField(blank=False,max_length=100)
    total_waste=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    waste_recycled=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    def get_lw(self):
        return self.total_waste-self.waste_recycled
    landfill_Waste=property(get_lw)

    def __str__(self):
        return self.ppname

class TransportVehicle(models.Model):
    tv_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_Of_collection = models.DateField(default=timezone.now)
    plate_number=models.CharField(blank=False,null=False,max_length=20)
    capacity=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    choices_permit=(
        ('ALL INDIA PERMIT','ALL INDIA PERMIT'),
        ('STATE PERMIT','STATE PERMIT'),
        ('CITY','CITY')
    )
    permit=models.CharField(max_length=20,choices=choices_permit,blank=False)
    pp=models.ForeignKey(ProcesssingPlant,on_delete=models.CASCADE)
    pincode = models.IntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)],blank=False)

    def __str__(self):
        return str(self.pincode) +" ( "+ self.plate_number+" ) "

class Landfill(OrganisationAddress):
    lf_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lfname=models.CharField(blank=False,max_length=100)
    maximum_capacity=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    capacity_filled=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    pp=models.ForeignKey(ProcesssingPlant,on_delete=models.CASCADE)

    def __str__(self):
        return self.lfname

class Waste(models.Model):
    waste_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tpuser= models.ForeignKey(TUser,on_delete=models.DO_NOTHING)
    choices_type=(
        ('Recyable','Recyable'),
        ('Non-Recyable','Non-Recyable')
    )
    type_waste=models.CharField(max_length=20,choices=choices_type,blank=False)
    created_date = models.DateField(default=timezone.now)
    quantity=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    tv = models.ForeignKey(TransportVehicle,blank=True,on_delete=models.DO_NOTHING)




    









    