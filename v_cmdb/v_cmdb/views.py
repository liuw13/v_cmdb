from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView

def index_page(request):
    return render(request, 'index.html')

class LoginView(TemplateView):

    template_name = 'login.html'

    def post(self,request, *args, **kwargs):
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            status = 1
        else:
            status = 0
        return JsonResponse({'data': status})

class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect('/login/')
