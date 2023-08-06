class BizException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.code = -1