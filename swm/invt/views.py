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
from .models import TUser,Waste

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
    #tuser = TUser.objects.get(username=username)
    return render(request,'users/home.html',{}) 

""" class Home(ListView):
    model = TUser
    template_name='users/home.html'
    context_object_name='tuser'     #variable to be used in templates(variable that has all posts)
    #ordering = ['-date_posted']     #orders according to date_posted. date_posted - oldest to newest
    #paginate_by=4  """

@login_required
def waste_form(request):
    if request.method=='POST':
        form = WasteGenerationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your new entry has been added.')
            return redirect(r'home')
    else:    
        form = WasteGenerationForm()
    return render(request,'utility/waste_form.html',{'form':form})

    def save(self):
        form.instance.tpuser = self.request.tuser
        return super().save()