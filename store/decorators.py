from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_function):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_function(request,*args,**kwargs)

    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            print(group)
        if group == 'admin':
            return view_func(request,*args,**kwargs)
        elif group == 'customer':
            return redirect('store')
    return wrapper_func