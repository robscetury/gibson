import math

class threedee_math():
    
    def __init__(self):
        pass
    
    def distance_between(self, point1, point2):
        c = math.sqrt(math.pow((point1[0]-point2[0]),2) + math.pow((point1[1]-point2[1]),2) + math.pow((point1[2]-point2[2]),2))
        return c




