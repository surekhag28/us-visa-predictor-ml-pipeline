import sys


class DatabaseConnectionError(Exception):
    def __init__(self, error_message, error_details):
        self.error_message = error_message
        _,_,exc_tb=error_details.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
    
    def __str__(self) -> str:
        return 'Error occurred in python script name [{0}] line number [{1}] error message [{2}]'.format(
            self.file_name, self.lineno, str(self.error_message)
        )
        

class USvisaException(Exception):
    def __init__(self, error_message, error_details):
        self.error_message = error_message
        _,_,exc_tb=error_details.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
    
    def __str__(self) -> str:
        return 'Error occurred in python script name [{0}] line number [{1}] error message [{2}]'.format(
            self.file_name, self.lineno, str(self.error_message)
        )