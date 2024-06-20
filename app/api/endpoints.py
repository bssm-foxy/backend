import yaml
import asyncio

from pydantic import BaseModel
from fastapi import APIRouter, status, HTTPException

from api.models import PointName, RobotPosition
from database.db_querys import SetPointQueryAsync, GetStartPoint, Arrived, WaitUntilArrived, \
                                ReturnLatestStartPosition


router = APIRouter()


@router.get("/")
def home():
    return "Hello"


## 로봇 출발 후 대기 시간 페이지 로딩 대기 
async def post_point(point: PointName):
    TIME_OUT = 120 # 대기시간 2분으로 설정

    try:
        await SetPointQueryAsync(point.start_point, point.finish_point)
        positions = GetStartPoint()

        point_name = positions["point_name"]
        point_x = positions["point_x"]
        point_y = positions["point_y"]
        
        await post_move_to_goal(point_name, point_x, point_y)
        
        if await WaitUntilArrived(timeout=TIME_OUT):
            return {
                "Success_or_not": True
                }
        else:
            # 타임아웃 처리
            raise HTTPException(status_code=500, detail="대기시간이 너무 길어 Timeout 처리하였습니다.")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/point", status_code=status.HTTP_201_CREATED)
async def post_point_handler(point: PointName):
    return await post_point(point)


## 로봇 출발 명령
@router.post("/robot/move_to_goal", status_code=status.HTTP_201_CREATED)
async def post_move_to_goal(point_name: str, point_x: float, point_y: float):
    print(f"{point_name} 으로 이동합니다. 해당좌표: ({point_x}, {point_y})")

    return {
        "Success_or_not": True
    }

@router.get("/robot/move_to_goal", status_code=status.HTTP_200_OK)
async def get_move_to_goal():
    # 데이터베이스 조회 코드로 수정 필요 
    start_positions = ReturnLatestStartPosition()
    
    if start_positions:
        return {
            "point_name": start_positions["point_name"],
            "position_x": start_positions["position_x"],
            "position_y": start_positions["position_y"]
        }

## 도착시 데이터베이스 is_arrived 값 True로 변경 
@router.post("/robot/arrived", status_code=status.HTTP_201_CREATED)
async def RobotArrived():
    Arrived() # 도착하면 도착 값을 True로 변경

    return {
        "Success_or_not": True
    }




## 현재 로봇 위치 파악 코드 
TempPosition = {
    "point_x": None, 
    "point_y": None
}

@router.post("/robot/position", status_code=status.HTTP_201_CREATED)
def PostPosition(position: RobotPosition):
    global TempPosition

    res_data = position # 받은 좌푯값 

    TempPosition["point_x"] = res_data.x
    TempPosition["point_y"] = res_data.y
    TempPosition["point_z"] = 0.050000

    return {
        "Success_or_not": True,
        "Position": TempPosition
    }

@router.get("/robot/position", status_code=status.HTTP_200_OK)
def GetPosition():
    return {
        "Success_or_not": True,
        "Position": TempPosition
    }

# 로봇에서 수화물이 적재 되었다고 신호를 보내면 POST 전송 
@router.post("/load", status_code=status.HTTP_201_CREATED)
def Load():
    # 이 사이에 도착했다는 결과가 와야함.

    return {
        "Success_or_not": True
    }

# 로봇에서 수화물이 양하 되었다고 신호를 보내면 POST 전송 
@router.post("/unload", status_code=status.HTTP_201_CREATED)
def Load():
    return {
        "Success_or_not": True
    }