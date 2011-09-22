

class SluggerBase():
    def __init__(self, panda, data):
        self.starting_position = (0, 0, 0)
        self.data = data
        self.panda = panda


    def createTunnel(self):
        raise "Not Implemented"

    def createSlug(self):
        raise "Not Implemented"