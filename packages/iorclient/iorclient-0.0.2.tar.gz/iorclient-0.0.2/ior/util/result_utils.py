import enum
import traceback

def error_handler(func):
    def execute(self,*args,**kwargs):
        try:
            return func(self,*args,**kwargs), 0
        except:
            msg = traceback.format_exc()
            if self.config.is_print:
                print(msg)
            return f'error:{msg}', 1
    return execute
    
def receipt_error_handler(func):
    def execute(self,*args,**kwargs):
        try:
            receipt,res = func(self,*args,**kwargs)
            return receipt,res,0
        except:
            msg = traceback.format_exc()
            if self.config.is_print:
                print(msg)
            return None,f'error:{msg}',1
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
