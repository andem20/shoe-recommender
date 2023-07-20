class DataStore():
    def __init__(self):
        self.images: list[str] = []
        self.labels: list[int] = []
        self.path = ""
        self.index = 0