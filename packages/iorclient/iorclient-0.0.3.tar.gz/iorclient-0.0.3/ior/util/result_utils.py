import enum
import traceback

def error_handler(func):
    def execute(self,*args,**kwargs):
        try:
            res = func(self,*args,**kwargs)
            return 0, res
        except:
            msg = traceback.format_exc()
            return 1, f'error:{msg}'
    return execute
    
def two_ret_error_handler(func):
    def execute(self,*args,**kwargs):
        try:
            res1,res2 = func(self,*args,**kwargs)
            return 0,res1,res2
        except:
            msg = traceback.format_exc()
            return 1,f'error:{msg}',None
    return execute

    
class StatusCode(enum.Enum):
    """
    状态码
    """
    success = 200
    error = 500


def success(message: str = None, data: any = None) -> dict:
    """
    操作成功
    :param message:
    :param data:
    :return:
    """
    message = message if message else '操作成功'
    return {'status': StatusCode.success.value, 'message': message, 'data': data}


def error_500(message: str = None, data: any = None) -> dict:
    """
    系统异常
    :param message:
    :param data:
    :return:
    """
    message = message if message else '系统异常'
    return {'status': StatusCode.error.value, 'message': message, 'data': data}


def error_invalid_parameter(data: any = None) -> dict:
    """
    参数格式不正确
    :param data:
    :return:
    """
    return error_500(message="参数格式不正确", data=data)
