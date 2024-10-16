from django.shortcuts import render,redirect
from django.views.generic import View
from todo.forms import TodoForm,RegistrationForm,LoginForm
from todo.models import Todo
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todo.decorators import signin_required
from django.utils.decorators import method_decorator



# Create your views here.

@method_decorator(signin_required,name="dispatch")
class TodoCreateView(View):
    def get(self,request,*args,**kwargs):

        form_instance=TodoForm

        qs=Todo.objects.filter(user_object=request.user)
        return render(request,"todo_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=TodoForm(request.POST)
        if form_instance.is_valid():
            
            form_instance.instance.user_object=request.user

            form_instance.save()

            messages.success(request,"task added successfully!!!!!!!!")

            print("task has been created")

            return redirect('todo-add')
        
        else:
            messages.error(request,"creation failed")
            return render(request,"todo_add.html",{"form":form_instance})
        

@method_decorator(signin_required,name="dispatch")
class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        todo_obj=Todo.objects.get(id=id)

        form_instance=TodoForm(instance=todo_obj)

        return render(request,"todo_edit.html",{"form":form_instance})
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        todo_obj=Todo.objects.get(id=id)

        form_instance=TodoForm(instance=todo_obj,data=request.POST)

        if form_instance.is_valid():
            form_instance.save()
            messages.success(request,"todo has been updated")
                
            return redirect("todo-add")
            
        else:
            messages.error(request,"updating failed")
            return render(request,"todo_edit.html",{"form":form_instance})

    
@method_decorator(signin_required,name="dispatch")
class TodoDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Todo.objects.get(id=id)

        return render(request,"todo_detail.html",{"data":qs})
    

@method_decorator(signin_required,name="dispatch")
class TodoDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Todo.objects.get(id=id).delete()

        messages.success(request,"todo has been deleted")

        return redirect("todo-add")
    


class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm
        
        return render(request,"register.html",{"form":form_instance})
    
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            # form_instance.save()

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            print("user object created")

            return redirect("signin")
        
        else:

            print("user creation failed")

            return render(request,"register.html",{"form":form_instance})
        

class SignInView(View):

    def get(self,request,*args,**kwargs):
        form_instance=LoginForm()
        return render(request,"sign_in.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)
        
        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            print(uname,pwd)

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:
                login(request,user_object)
                return redirect("todo-add")
        messages.error(request,"authentication failed inavlid credential")
        return render(request,"sign_in.html",{"form":form_instance})    

            
@method_decorator(signin_required,name="dispatch")          
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    




