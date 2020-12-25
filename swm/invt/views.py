from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,WasteGenerationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import TUser,Waste,ProcesssingPlant,TransportVehicle,Landfill

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your account has been created! You can now login. ')
            return redirect(r'login')
    else:    
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def home(request):
    wuser = request.user
    waste_list = Waste.objects.filter(tpuser=wuser)
    waste_list_admin = Waste.objects.all()
    tv_list = TransportVehicle.objects.all()
    pp_list = ProcesssingPlant.objects.all()
    lf_list = Landfill.objects.all()
    return render(request,'users/home.html',{'waste_list':waste_list,
    'waste_list_admin':waste_list_admin,'tv_list':tv_list,'pp_list':pp_list,'lf_list':lf_list,}) 

@login_required
def waste_form(request):
    if request.method=='POST':
        waste_form = WasteGenerationForm(request.POST)
        if waste_form.is_valid():
            formm = waste_form.save(commit=False)
            my_p =request.user
            formm.tpuser = my_p
            formm.save()

            #saving data to processing plant
            transvehicle = formm.tv
            tv_pp = transvehicle.pp
            pp_temp = ProcesssingPlant.objects.get(pp_id=tv_pp.pp_id)
            pp_temp.total_waste+=formm.quantity
            if(formm.type_waste == 'Non-Recyable'):
                pp_temp.landfill_waste+=formm.quantity
            pp_temp.save()

            #saving data to Landfill
            ll_temp = Landfill.objects.filter(pp=pp_temp)
            if(formm.type_waste == 'Non-Recyable'):
                for ll in ll_temp:
                    if formm.quantity+ll.capacity_filled <= ll.maximum_capacity :
                        ll.capacity_filled+=formm.quantity
                        ll.save()
                        break
            messages.success(request,f'Your new entry has been added.')
            return redirect(r'home')
    else:    
        waste_form = WasteGenerationForm()
    return render(request,'utility/waste_form.html',{'form':waste_form})
""" class UserWasteList(ListView):
    model = Waste
    template_name='users/user_waste.html'
    context_object_name='waste_list'
    
    
    def get_queryset(self,*args,**kwargs):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        #wasteuser = Waste.objects.filter(tpuser=user).first()
        return Waste.objects.filter(tpuser=user).order_by('-created_date')
         """
