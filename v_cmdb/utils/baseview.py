from django.views import View
from django.http import JsonResponse,QueryDict
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseView(LoginRequiredMixin,View):
    model = None
    detail_page = None
    list_page = None

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = self.model.objects.filter(Q(name__contains=search))
        return queryset

    def get(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        if pk:
            obj_data = self.model.objects.get(id=pk).to_dict()
            return render(request,self.detail_page,obj_data)
        queryset = self.get_queryset()
        p = Paginator(queryset, 10)
        page = request.GET.get('page')
        try:
            paginator_data = p.page(page)
        except PageNotAnInteger:
            paginator_data = p.page(1)
        except EmptyPage:
            paginator_data = p.page(p.num_pages)
        return render(request,self.list_page , {'paginator_data': paginator_data})

    #@method_decorator(permission_required('cmdb.mng_idc'))
    def post(self,request,*args,**kwargs):
        data = QueryDict(request.body).dict()
        self.model.objects.create(**data)
        return JsonResponse({})

    def delete(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        #pk=QueryDict(request.body).dict().get('pk')
        self.model.objects.filter(pk=pk).delete()
        return JsonResponse({})

    def put(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        data = QueryDict(request.body).dict()
        self.model.objects.filter(id=pk).update(**data)
        return JsonResponse({})