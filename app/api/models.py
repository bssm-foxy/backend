from pydantic import BaseModel


# 출발지와 도착지 이름 
class PointName(BaseModel):
    start_point: str 
    finish_point: str 

# 로봇 현재 위치 
class RobotLocationInfo(BaseModel):
    x: float 
    y: float 
    z: float
