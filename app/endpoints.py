import yaml

from fastapi import APIRouter, status

from models import Point
from state import PointManager

with open("../data/Classes.yaml", "r") as file:
    yaml_file = yaml.safe_load(file)

def load_file(classname):
    point_x = float(yaml_file[classname]["x"][:-1])
    point_y = float(yaml_file[classname]["y"])

    return point_x, point_y


router = APIRouter()

@router.get("/")
def home():
    return "Hello"

## Point 부분 
@router.post("/point", status_code=status.HTTP_201_CREATED)
async def post_point(point: Point):
    # 웹에서 출발지와 도착지를 받음 
    points = PointManager.set_points(point.start_point, point.finish_point)

    # 출발지에 출발하기 위해 출발지 이름의 좌표를 받음 
    point_name = str(points["start_point"])
    point_x, point_y = load_file(point_name)

    # 로봇에게 출발 명령 보내기 (예시로 print만 사용)
    await move_to_goal(point_name, point_x, point_y)

    # 로봇이 도착했을 때 Success_or_not 반환
    return {
        "Success_or_not": True
    }

## 로봇 출발 명령
@router.post("/robot/move_to_goal", status_code=status.HTTP_201_CREATED)
async def move_to_goal(point_name: str, point_x: float, point_y: float):
    print(f"{point_name} 으로 이동합니다. 해당좌표: ({point_x}, {point_y})")

    return True
