from typing import Optional
from fastapi import APIRouter, status, HTTPException, Body

from api.models import PointName, RobotPosition
from database.db_querys import SetPoint, GetStartPoint, GetFinishPoint, StartArrived, FinishArrived, \
                                WaitUntilArrived, WaitUntilArrived_1

TIME_OUT = 120 # 대기시간 2분으로 설정

router = APIRouter()


@router.get("/")
def home():
    return "Hello"


# 로봇 출발 후 대기 시간 페이지 로딩 대기 
# 목적지를 출발지로 설정 
async def move_to_start_point(point: PointName):
    try:
        await SetPoint(point.start_point, point.finish_point)  # 데이터베이스에 출발지와 도착지 설정 

        positions = GetStartPoint()  # 출발지 좌표를 가져옴 

        point_name = positions["point_name"]  # 출발지 이름 
        point_x = positions["point_x"]  # 출발지 X 좌표 
        point_y = positions["point_y"]  # 출발지 Y 좌표
        
        await MoveToGoal(point_name, point_x, point_y)  # 출발지로 출발 
        
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
    
async def move_to_finish_point():
    try:
        positions = GetFinishPoint()  # 출발지 좌표를 가져옴 

        point_name = positions["point_name"]  # 출발지 이름 
        point_x = positions["point_x"]  # 출발지 X 좌표 
        point_y = positions["point_y"]  # 출발지 Y 좌표
        
        await MoveToGoal(point_name, point_x, point_y)  # 출발지로 출발 
        
        if await WaitUntilArrived_1(timeout=TIME_OUT):
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
async def point(point: PointName):
    return await move_to_start_point(point)  # start_or_finish 값에 따라 목적지 변경 

# 로봇에서 수화물이 적재 되었다고 신호를 보내면 POST 전송 
@router.post("/load", status_code=status.HTTP_201_CREATED)
async def load():
    return await move_to_finish_point()


# 로봇에서 수화물이 양하 되었다고 신호를 보내면 POST 전송 
@router.post("/unload", status_code=status.HTTP_201_CREATED)
def unoad():
    return {
        "Success_or_not": True
    }







@router.post("/robot/move_to_goal", status_code=status.HTTP_201_CREATED)
async def MoveToGoal(point_name: str, point_x: float, point_y: float):
    print(f"{point_name} 으로 이동합니다. 해당좌표: ({point_x}, {point_y})")

    return {
        "Success_or_not": True
    }

@router.get("/robot/get_start_point",status_code=status.HTTP_200_OK) 
async def GetStartPosition():
    positions = GetStartPoint()

    if positions:
        return {
            "point_name": positions["point_name"],
            "position_x": positions["point_x"],
            "position_y": positions["point_y"]
        }

@router.get("/robot/get_finish_point",status_code=status.HTTP_200_OK) 
async def GetFinishPosition():
    positions = GetFinishPoint()

    if positions:
        return {
            "point_name": positions["point_name"],
            "position_x": positions["point_x"],
            "position_y": positions["point_y"]
        }


## 도착시 데이터베이스 is_arrived 값 True로 변경 
@router.post("/robot/start_point_arrived", status_code=status.HTTP_201_CREATED)
async def StartPointArrived():
    StartArrived() # 도착하면 도착 값을 True로 변경

    return {
        "Success_or_not": True
    }

@router.post("/robot/finish_point_arrived", status_code=status.HTTP_201_CREATED)
async def FinishPointArrived():
    FinishArrived() # 도착하면 도착 값을 True로 변경

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


## 
