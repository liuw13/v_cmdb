from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User

class LoginView(TemplateView):
    """登录页面, 用户密码鉴权"""
    template_name = 'login.html'

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        #login_type = request.POST.get('login_type', None)
        '''
        if login_type == 'ldap':
            ldap_ops = LdapOps()
            res = ldap_ops.check(username, password)
            status = res.get('status')
            if status == 0:  # LDAP验证通过
                try:  # 用户存在，改密码
                    user = User.objects.get(username=username)
                except User.DoesNotExist:  # 用户不存在，创建用户
                    user = User.objects.create_user(username=username, password=password)
                user.set_password(password)
                user.save()
            else:
                data = res.get('data')
                return JsonResponse({'status': status, 'data': data})
        '''
        user = authenticate(username=username, password=password)  # django鉴权
        if user is not None:  # 用户密码及token正确
            login(request, user)
            status = 0
        else:
            status = 1
        return JsonResponse({'status': status})


class LogoutView(LoginRequiredMixin, View):
    """"退出登录"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login/")


class IndexPage(LoginRequiredMixin, TemplateView):
    """首页"""
    template_name = 'index.html'