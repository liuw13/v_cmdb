from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict, JsonResponse
from django.views.generic import View, ListView
from django.shortcuts import render
from utils.wrappers import handle_save_data


class BaseListView(LoginRequiredMixin, ListView):
    """"列表页/详情页, 增删改查, 通用类视图"""
    model = None
    template_detail = None
    paginate_by = 10

    def handle_page(self, page, object_list):
        paginator = Paginator(object_list, self.paginate_by, 1)
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            paginator_data = paginator.page(1)
        except EmptyPage:
            paginator_data = paginator.page(paginator.num_pages)
        return paginator_data

    def data_format(self, data):
        res = {}
        for k in data:
            v = data[k]
            if len(v) == 0 or v.isspace() == True:
                v = None
            res[k] = v
        return res

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                instance = self.model.objects.get(pk=pk)
                return render(request, self.template_detail, instance.to_dict)
            except self.model.DoesNotExist:
                return JsonResponse({'data':'id {} not exits'.format(pk)})
        object_list = self.get_queryset()
        page = request.GET.get('page')
        paginator_data = self.handle_page(page, object_list)
        search = request.GET.get('search', '')
        return render(request, self.template_name, {'paginator_data': paginator_data, 'search': search})

    @handle_save_data
    def post(self,request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        data = self.data_format(data)
        self.model.objects.create(**data)
        return JsonResponse({'status': 1})

    @handle_save_data
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        data = QueryDict(request.body).dict()
        data = self.data_format(data)
        self.model.objects.filter(pk=pk).update(**data)
        return JsonResponse({'status': 1})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.model.objects.get(pk=pk)
        instance.delete()
        return JsonResponse({'status': 1})


class BaseAPIView(View):
    """"查询API, 通用类视图"""
    model = None
    count_limit = 1000

    def get_queryset(self):
        queryset = self.model.objects.all()[:self.count_limit]
        qs = [i.to_dict for i in queryset]
        return qs

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                instance = self.model.objects.get(pk=pk).to_dict
            except Exception as e:
                instance = e.args[0]
            return JsonResponse({'data': instance})
        queryset = self.get_queryset()
        return JsonResponse({'count':len(queryset), 'data': queryset})

