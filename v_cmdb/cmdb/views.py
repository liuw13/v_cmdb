from django.views import View
from .models import *
from django.http import JsonResponse,HttpResponse,QueryDict
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from utils.baseview import *
import json

class APIVmView(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = Vm.objects.get(pk=pk)
            data = obj.to_dict()
        else:
            queryset = Vm.objects.all()[:1000]
            objs = [obj.to_dict() for obj in queryset ]
            data = {'data':objs}
        return JsonResponse(data)

class APIServerView(View):
    model = Server
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = Server.objects.get(pk=pk)
            data = obj.to_dict()
        else:
            queryset = Server.objects.all()[:1000]
            objs = [obj.to_dict() for obj in queryset ]
            data = {'data':objs}
        return JsonResponse(data)

    def post(self,request,*args,**kwargs):
        data = QueryDict(request.body).dict()
        name = data.get('hostname')
        cpu = data.get('server_cpu')
        memory = data.get('server_mem')
        disk = data.get('server_disk')
        uuid = data.get('uuid')
        daq = json.dumps(data)
        server_data = {
            'name':name,
            'cpu':cpu,
            'memory':memory,
            'disk':disk,
            'uuid':uuid,
            'daq':daq
        }
        #如果数据存在就修改，否则 保存
        qs_obj = self.model.objects.filter(uuid=uuid)
        try:
            if qs_obj:
                qs_obj.update(**server_data)
                qs_obj.first().save()
            else:
                self.model.objects.create(**server_data)
        except Exception as e:
            return  JsonResponse(e.args[1])
        return JsonResponse({'status':1})



class APIRackView(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = Rack.objects.get(pk=pk)
            data = obj.to_dict()
        else:
            queryset = Rack.objects.all()[:1000]
            objs = [obj.to_dict() for obj in queryset ]
            data = {'data':objs}
        return JsonResponse(data)

class APIIdcView(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = Idc.objects.get(pk=pk)
            data = obj.to_dict()
        else:
            queryset = Idc.objects.all()[:1000]
            objs = [obj.to_dict() for obj in queryset ]
            data = {'data':objs}
        return JsonResponse(data)

class IdcView(BaseView):
    model = Idc
    detail_page = 'cmdb/idc_details.html'
    list_page = 'cmdb/idcs.html'


class RackView(BaseView):
    model = Rack
    detail_page = 'cmdb/rack_details.html'
    list_page = 'cmdb/racks.html'
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = Rack.objects.filter(Q(name__contains=search))
        return queryset

class ServerView(BaseView):
    model = Server
    detail_page = 'cmdb/server_details.html'
    list_page = 'cmdb/servers.html'
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = Server.objects.filter(Q(name__contains=search) | Q(ip__contains=search) |Q(sn__contains=search) )
        return queryset

class VmView(BaseView):
    model = Server
    detail_page = 'cmdb/vm_details.html'
    list_page = 'cmdb/vms.html'
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = Vm.objects.filter(Q(name__contains=search) | Q(ip__contains=search))
        return queryset

class DashBoardView(TemplateView):
    template_name = 'dashboard.html'

class APIDashBaord(View):
    def get(self,request,*args,**kwargs):
        '''
        data = {
            'count':{
                'idcs': 10,
                'racks':20,
                'servers':30,
                'vms':40
            },
            'site':[
                {'name':'idc1','total_size':200,'size':60},
                {'name':'idc2','total_size':130,'size':80},
            ],
            'idc_servers':[
                ['idc1',200],
                ['idc2',130]
            ]
        }
        '''
        data = {}
        data['count']={
            'idcs':Idc.objects.count(),
            'racks':Rack.objects.count(),
            'servers':Server.objects.count(),
            'vms':Vm.objects.count()
        }

        site =[]
        idc_servers = []
        for idc in Idc.objects.all():
            site_dict = {}
            site_dict['name']= idc.name
            site_dict['total_size']=idc.rack_set.count()* 10
            size =0
            for rack in idc.rack_set.all():
                size += rack.server_set.count()
            site_dict['size'] = size
            site.append(site_dict)
            idc_servers.append([idc.name,size])
        data['site']=site
        data['idc_servers'] = idc_servers
        return JsonResponse(data)