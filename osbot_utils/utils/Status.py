def status_message(status, message:str=None, data=None, error=None):
    return  {  'data'   : data    ,
               'error'  : error   ,
               'message': message ,
               'status' : status
            }

def status_error  (message:str=None, data=None,error=None): return status_message('error'  , message=message, data=data, error=error)
def status_fatal  (message:str=None, data=None,error=None): return status_message('fatal'  , message=message, data=data, error=error)
def status_info   (message:str=None, data=None,error=None): return status_message('info'   , message=message, data=data, error=error)
def status_ok     (message:str=None, data=None,error=None): return status_message('ok'     , message=message, data=data, error=error)
def status_warning(message:str=None, data=None,error=None): return status_message('warning', message=message, data=data, error=error)


#todo: add status_exception that automatically picks up the exception from the stack trace
