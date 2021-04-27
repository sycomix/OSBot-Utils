import logging

# todo refactor into Status class

logger = logging.getLogger()

def status_message(status, message:str=None, data=None, error=None):
    return  {  'data'   : data    ,
               'error'  : error   ,
               'message': message ,
               'status' : status
            }

def status_error  (message:str='', data=None,error=None): logger.error  ('[osbot] [error] '   + message); return status_message('error'  , message=message, data=data, error=error)
def status_debug  (message:str='', data=None,error=None): logger.debug  ('[osbot] [debug] '   + message); return status_message('debug'  , message=message, data=data, error=error)
def status_fatal  (message:str='', data=None,error=None): logger.fatal  ('[osbot] [fatal] '   + message); return status_message('fatal'  , message=message, data=data, error=error)
def status_info   (message:str='', data=None,error=None): logger.info   ('[osbot] [info] '    + message); return status_message('info'   , message=message, data=data, error=error)
def status_ok     (message:str='', data=None,error=None): logger.info   ('[osbot] [ok] '      + message); return status_message('ok'     , message=message, data=data, error=error)
def status_warning(message:str='', data=None,error=None): logger.warning('[osbot] [warning] ' + message); return status_message('warning', message=message, data=data, error=error)

#todo: add logging hook that automatically picks up the caller (class and method) from the stack trace
#todo: add status_exception that automatically picks up the exception from the stack trace
