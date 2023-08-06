class CustomError(Exception):
    
    EXCEPTION_MAP = {
        1: "Connection Refused"
        }
    
    WARNING_MAP = {
        "": ""
    }
    
    def __init__(self, arg):
        self.strerror = self.EXCEPTION_MAP[arg]
        self.args = {self.EXCEPTION_MAP[arg]}