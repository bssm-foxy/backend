from fastapi import APIRouter, status, HTTPException

from api.models import PointName, RobotLocationInfo
from database.db_querys import init_location_info, location_arrived, wait_until_arrived
from database.db_querys import search_location_info, check_arrived_value, set_load_true, load_stats, insert_load

TIME_OUT = 120 # 대기시간 2분으로 설정

router = APIRouter()

@router.get("/")
def home():
    return "Hello"

# 로봇 출발 후 대기 시간 페이지 로딩 대기 
async def move_to_start_point(point: PointName):
    try:
        await init_location_info(point.start_point, point.finish_point)  # 데이터베이스에 출발지와 도착지 설정 

        location_info = search_location_info("start")  # start로 설정하여 출발지 정보를 가져옴  

        location_name = location_info["name"]  # 출발지 이름 
        location_x = location_info["locations"]["x"]  # 출발지 X 좌표 
        location_y = location_info["locations"]["y"]  # 출발지 Y 좌표
        
        await MoveToGoal(location_name, location_x, location_y)  # 출발지로 출발 
        await insert_load()

        if await wait_until_arrived(timeout=TIME_OUT, start_or_finish="start"):
            # 여기에 적재 데이터베이스 = True로 설종 들어가야 함 
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
        location_info = search_location_info("finish")  # finish로 설정하여 도착지 정보를 가져옴 

        location_name = location_info["name"]  # 출발지 이름 
        location_x = location_info["locations"]["x"]  # 출발지 X 좌표 
        location_y = location_info["locations"]["y"]  # 출발지 Y 좌표
        
        await MoveToGoal(location_name, location_x, location_y)  # 출발지로 출발 
        
        if await wait_until_arrived(timeout=TIME_OUT, start_or_finish="finish"):
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
    return await move_to_start_point(point)




@router.post("/load", status_code=status.HTTP_201_CREATED)
async def load():
    await set_load_true()
    return await move_to_finish_point()


@router.get("/isload", status_code=status.HTTP_200_OK)
async def isload():
    return load_stats()


@router.post("/unload", status_code=status.HTTP_201_CREATED)
def unoad():
    return {
        "Success_or_not": True
    }


@router.post("/robot/move_to_goal", status_code=status.HTTP_201_CREATED)
async def MoveToGoal(point_name: str, point_x: float, point_y: float):
    # 해당 좌표로 로봇을 이동 
    print(f"{point_name} 으로 이동합니다. 해당좌표: ({point_x}, {point_y})")  # 로그 

    return {
        "Success_or_not": True
    }

@router.get("/robot/set_start_location_arrived", status_code=status.HTTP_200_OK)
async def start_location_arrived():
    location_arrived("start")  # 출발지 도착 여부를 True로 설정 
    return {
        "Success_or_not": True
    }

@router.get("/robot/set_finish_location_arrived", status_code=status.HTTP_200_OK)
async def finish_location_arrived():
    location_arrived("finish")  # 도착지 도착 여부를 True로 설정 
    return {
        "Success_or_not": True
    }

@router.get("/robot/get_start_location_info",status_code=status.HTTP_200_OK) 
async def get_start_location_info():
    location_info = search_location_info("start")  # 출발지 좌표 받음 

    if location_info:
        return {
            "location_name": location_info["name"],
            "location_x": location_info["locations"]["x"],
            "location_y": location_info["locations"]["y"],
        }
    
@router.get("/robot/get_finish_location_info",status_code=status.HTTP_200_OK) 
async def get_finish_location_info():
    location_info = search_location_info("finish")  # 도착지 좌표 받음 

    if location_info:
        return {
            "location_name": location_info["name"],
            "location_x": location_info["locations"]["x"],
            "location_y": location_info["locations"]["y"],
        }
    
@router.post("/robot/check_arrived_status", status_code=status.HTTP_201_CREATED)
async def check_arrived_status(start_or_finish: str):  # 출발지와 도착지 도착 여부 확인
    check_value = check_arrived_value(start_or_finish)
    return {
        "value": check_value,
        "Success_or_not": True
    }

#  데이터베이스에 담기는 귀찮아서 전역변수로 설정 
#  혹시나 문제가 된다면 데이터베이스로 전환 필요 
g_location_data = {
    "x": None, 
    "y": None
}

@router.post("/robot/realtime_location", status_code=status.HTTP_201_CREATED)
def post_realtime_location(locations: RobotLocationInfo):
    global g_location_data
    
    g_location_data["x"] = locations.x
    g_location_data["y"] = locations.y
    g_location_data["z"] = locations.z

    return {  # fastapi api docs에서 확인하기 위한 용도 
        "locations": {
            "x": g_location_data["x"],
            "y": g_location_data["y"],
            "z": g_location_data["z"]
        }
    }

@router.get("/robot/realtime_location", status_code=status.HTTP_200_OK)
def get_realtime_location():
    return {
        "location_info": g_location_data
    }