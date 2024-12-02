import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

# Set up the logger
logger = logging.getLogger('jsonLogger')

# Set up the log rotation with a max size of 5MB per file and 5 backups
logHandler = RotatingFileHandler('logs/decorator_logs.json', maxBytes=5*1024*1024, backupCount=5)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(lineno)d %(funcName)s %(args)s %(result)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Decorator to log function calls and results
def log_function_call(func):
    def wrapper(*args, **kwargs):
        # Log the function call
        logger.info(f'Calling {func.__name__}', extra={'log_args': args, 'log_kwargs': kwargs})
        
        try:
            # Call the original function
            result = func(*args, **kwargs)
            
            # Log the result
            logger.info(f'Function {func.__name__} executed successfully', extra={'log_args': args, 'result': result})
            
            return result
        except Exception as e:
            # Log any exceptions raised
            logger.error(f'Function {func.__name__} raised an exception', extra={'log_args': args, 'error': str(e)})
            raise
    return wrapper
