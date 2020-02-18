from functools import wraps
from django.http import JsonResponse


def handle_save_data(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            code = e.args[0]
            desc = e.args[1]
            if code == 1062:
                status = 0
                instance = '名称重复({})'.format(desc)
            else:
                status = -1
                instance = desc
            return JsonResponse({'data': instance, 'status':status})
    return wrapper