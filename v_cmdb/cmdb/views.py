import json
from django.db.models import Q
from django.http import QueryDict,JsonResponse
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from utils.baseviews import BaseAPIView, BaseListView
from .models import Idc, Rack, Server,Vm

# Create your views here.
class IdcView(BaseListView):
    """机房的列表页/详情页, 增删改查"""
    model = Idc
    template_name = 'cmdb/idcs.html'
    template_detail = 'cmdb/idc_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__contains=search) | Q(address__contains=search))
        qs = [i.to_dict for i in queryset]
        return qs
class APIIdcView(BaseAPIView):
    """"机房的API: 查询"""
    model = Idc
class RackView(BaseListView):
    """机柜的列表页/详情页, 增删改查"""
    model = Rack
    template_name = 'cmdb/racks.html'
    template_detail = 'cmdb/rack_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        idc_id = self.request.GET.get('idc_id')
        if idc_id:
            queryset = queryset.filter(idc_id=idc_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__contains=search) | Q(number__contains=search) | Q(size__contains=search))
        qs = [i.to_dict for i in queryset]
        return qs
class APIRackView(BaseAPIView):
    """"机柜的API: 查询"""
    model = Rack
class ServerView(BaseListView):
    """服务器的列表页/详情页, 增删改查"""
    model = Server
    template_name = 'cmdb/servers.html'
    template_detail = 'cmdb/server_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        rack_id = self.request.GET.get('rack_id')
        if rack_id:
            queryset = queryset.filter(rack_id=rack_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__contains=search) | Q(ip__contains=search))
        qs = [i.to_dict for i in queryset]
        return qs
class APIServerView(BaseAPIView):
    """"机柜的API: 查询, 自动采集的信息录入"""
    model = Server

    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        name = data.get('hostname')
        uuid = data.get('uuid')
        server_type = data.get('server_type')
        cpu = data.get('server_cpu')
        memory = data.get('server_mem')
        disk = data.get('server_disk')
        daq = json.dumps(data)
        server_data = {
            'name': name,
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'uuid': uuid,
            'server_type': server_type,
            'daq': daq
        }
        qs_instance = self.model.objects.filter(uuid=uuid, server_type=server_type)
        if qs_instance:
            qs_instance.update(**server_data)
            qs_instance.first().save()
        else:
            self.model.objects.create(**server_data)
        return JsonResponse({})

class VmView(BaseListView):
    """服务器的列表页/详情页, 增删改查"""
    model = Vm
    template_name = 'cmdb/vms.html'
    template_detail = 'cmdb/vm_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        server_id = self.request.GET.get('server_id')
        if server_id:
            queryset = queryset.filter(server_id=server_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__contains=search) | Q(ip__contains=search))
        qs = [i.to_dict for i in queryset]
        return qs
class APIVmView(BaseAPIView):
    """"机柜的API: 查询, 自动采集的信息录入"""
    model = Vm

    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        name = data.get('hostname')
        uuid = data.get('uuid')
        server_type = data.get('server_type')
        cpu = data.get('server_cpu')
        memory = data.get('server_mem')
        disk = data.get('server_disk')
        daq = json.dumps(data)
        vm_data = {
            'name': name,
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'uuid': uuid,
            'server_type': server_type,
            'daq': daq
        }
        qs_instance = self.model.objects.filter(uuid=uuid, server_type=server_type)
        if qs_instance:
            qs_instance.update(**vm_data)
            qs_instance.first().save()
        else:
            self.model.objects.create(**vm_data)
        return JsonResponse({})

class DashBoardView(TemplateView):
    """"DashBoard页面"""
    template_name = 'dashboard.html'
class APIDashBoardView(View):
    """DashBoard页面需要的数据"""
    def get(self, request, *args, **kwargs):
        data = {}
        data_idc_servers = []
        data_site = []
        idc_list = Idc.objects.all()
        for idc in idc_list:
            servers = 0
            site_idc = {}
            racks = idc.rack_set.all()
            total_site = racks.count()*10
            for rack in racks:
                servers += rack.to_dict.get('servers').get('count')
            data_idc_servers.append(
                [idc.name, servers]
            )
            if total_site > 0:
                site_idc['name'] = idc.name
                site_idc['total_site'] = total_site
                site_idc['site'] = servers
                data_site.append(site_idc)
        data['data_idc_servers'] = data_idc_servers
        data['data_site'] = data_site
        data['count'] = {
            'idcs': idc_list.count(),
            'racks': Rack.objects.count(),
            'servers': Server.objects.count(),
            'vms': Vm.objects.count(),
        }
        return JsonResponse({'data': data})
