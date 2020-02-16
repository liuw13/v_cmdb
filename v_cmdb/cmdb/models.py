from django.db import models
from django.contrib.auth.models import AbstractUser
from account.models import User
# Create your models here.

class BaseModel(models.Model):
    name = models.CharField(max_length=32)
    remark = models.TextField()
    class Meta:
        abstract = True

class Idc(BaseModel):
    user = models.ManyToManyField(User)
    address = models.CharField(max_length=96, blank=False, verbose_name='测试地址')
    contact = models.CharField(max_length=11, blank=False, verbose_name='联系方式')

    def change_name(self):
        return '你查到的机房是: {} '.format(self.name)

    def to_dict(self):
        ret = {}
        for i in self._meta.fields:
            field_name = i.name
            field_value = getattr(self, field_name)
            if field_name == 'contact':
                v = ''
                if len(field_value) != 0:
                    v = field_value[:3] + '****' + field_value[-4:]
                field_value = v
            ret[field_name] = field_value
            racks = [{'id': rack.id, 'name': rack.name} for rack in self.rack_set.all()]
            ret['racks'] = racks
        return ret

    class Meta:
        ordering = ['-id']
        verbose_name = '机房'

class Rack(BaseModel):
    idc = models.ForeignKey(Idc, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='所属机房')
    number = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='编号')
    size = models.CharField(default='', max_length=8, null=True, blank=True, verbose_name='U型')

    def to_dict(self):
        ret = {}
        for i in self._meta.fields:
            field_name = i.name
            print(field_name)
            field_value = getattr(self, field_name)
            if field_name == 'idc':
                if field_value:
                    field_value = field_value.to_dict()
                else:
                    field_value = ''
            ret[field_name] = field_value
            #racks = [{'id': rack.id, 'name': rack.name} for rack in self.rack_set.all()]
            #ret['racks'] = racks
        return ret

    class Meta:
        ordering = ['-id']
        verbose_name = '机柜'

class Server(BaseModel):
    STATUS = (
        (0, u'下线'),
        (1, u'在线'),
    )
    rack = models.ForeignKey(Rack, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='所属机柜')
    sn = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='SN')
    uuid = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='UUID')
    cpu = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='CPU')
    memory = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='内存')
    disk = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='磁盘大小')
    ip = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='ip地址')
    business = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='业务线')
    server_type = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='服务器类型')
    daq = models.TextField(default='', null=True, blank=True, verbose_name='数据采集')
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='运行状态')

    class Meta:
        ordering = ['-id']
        verbose_name = '物理服务器'

    def to_dict(self):
        ret = {}
        for i in self._meta.fields:
            field_name = i.name
            print(field_name)
            field_value = getattr(self, field_name)
            if field_name == 'rack':
                if field_value:
                    field_value = field_value.to_dict()
                else:
                    field_value = ''
            ret[field_name] = field_value
            #racks = [{'id': rack.id, 'name': rack.name} for rack in self.rack_set.all()]
            #ret['racks'] = racks
        return ret

class Vm(BaseModel):
    STATUS = (
        (0, u'下线'),
        (1, u'在线'),
    )
    server = models.ForeignKey(Server, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='所属宿主机')
    cpu = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='CPU')
    memory = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='内存')
    disk = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='磁盘大小')
    ip = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='ip地址')
    business = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='业务线')
    OS_type = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='操作系统')
    daq = models.TextField(default='', null=True, blank=True, verbose_name='数据采集')
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='运行状态')

    class Meta:
        ordering = ['-id']
        verbose_name = '虚拟机'

    def to_dict(self):
        ret = {}
        for i in self._meta.fields:
            field_name = i.name
            print(field_name)
            field_value = getattr(self, field_name)
            if field_name == 'server':
                if field_value:
                    field_value = field_value.to_dict()
                else:
                    field_value = ''
            ret[field_name] = field_value
            #racks = [{'id': rack.id, 'name': rack.name} for rack in self.rack_set.all()]
            #ret['racks'] = racks
        return ret