class DbGenDataNotValidError(Exception):
    def __init__(self, msg="The data that was sent to the DbGen is not valid"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'
