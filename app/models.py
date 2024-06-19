from pydantic import BaseModel


# 출발지와 도착지 이름 
class Point(BaseModel):
    start_point: str 
    finish_point: str 
