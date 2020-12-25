from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,WasteGenerationForm,LfGenerationForm,PpGenerationForm,TvGenerationForm,TvUpdateForm,LfUpdateForm,PpUpdateForm
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
@login_required
def tv_form(request):
    if request.method=='POST':
        tv_form = TvGenerationForm(request.POST)
        if tv_form.is_valid():
            tv_form.save()
            return redirect(r'home')
    else:    
        tv_form = TvGenerationForm()
    return render(request,'utility/tv_form.html',{'form':tv_form})
@login_required
def pp_form(request):
    if request.method=='POST':
        pp_form = PpGenerationForm(request.POST)
        if pp_form.is_valid():
            pp_form.save()
            return redirect(r'home')
    else:    
        pp_form = PpGenerationForm()
    return render(request,'utility/pp_form.html',{'form':pp_form})
@login_required
def lf_form(request):
    if request.method=='POST':
        lf_form = LfGenerationForm(request.POST)
        if lf_form.is_valid():
            lf_form.save()
            return redirect(r'home')
    else:    
        lf_form = LfGenerationForm()
    return render(request,'utility/lf_form.html',{'form':lf_form})
@login_required
def delete_tv(request, pk):

    template = 'users/home.html'
    TransportVehicle.objects.filter(tv_id=pk).delete()
    return redirect(r'home')
@login_required
def delete_pp(request, pk):

    template = 'users/home.html'
    ProcesssingPlant.objects.filter(pp_id=pk).delete()
    return redirect(r'home')
@login_required
def delete_lf(request, pk):

    template = 'users/home.html'
    Landfill.objects.filter(lf_id=pk).delete()
    return redirect(r'home')
def edit_item(request, pk, model, cls):
    item = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        form = cls(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(r'home')
    else:
        form = cls(instance=item)
        return render(request, 'utility/edit_item.html', {'form': form})


def update_tv(request, pk):
    return edit_item(request, pk, TransportVehicle, TvUpdateForm)


def update_pp(request, pk):
    return edit_item(request, pk, ProcesssingPlant, PpUpdateForm)


def update_lf(request, pk):
    return edit_item(request, pk, Landfill, LfUpdateForm)

