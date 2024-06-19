# 출발지와 도착지 point 반환 
class PointManager:
    def __init__(self):
        self.start_point = None 
        self.finish_point = None 

    @classmethod
    def set_points(self, start_point: str, finish_point: str):
        self.start_point = start_point
        self.finish_point = finish_point 

        return {
            "start_point": self.start_point,
            "finish_point": self.finish_point
        }
