from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get("/")
def home():
    return "Hello"






class ResPoint(BaseModel):
    start_point: str 
    finish_point: str 

START_POINT = None 
FINISH_POINT = None

# 출발지와 도착지 설정 
@app.post("/point", status_code=status.HTTP_201_CREATED)
async def PostPoint(points: ResPoint):
    global START_POINT, FINISH_POINT
    
    START_POINT = points.start_point  
    FINISH_POINT = points.finish_point

    # 도착했을 때 받는 값 추가 
    return {
            "Success_or_not": True
    }



# 로봇한테 출발지를 설정하여 출발지로 출발 
@app.get("/point", status_code=status.HTTP_200_OK)
def GetPoint():
    global START_POINT, FINISH_POINT
    
    if START_POINT is None and FINISH_POINT is None:
        return {
            "Success_or_not": False,
            "Message": "No created points"
        }
    return {
        "Success_or_not": True,
        "start_point": START_POINT,
        "finish_point": FINISH_POINT
    }













class Position(BaseModel):
    x: float 
    y: float 

POSITION = {
    "x": None, 
    "y": None
}

@app.post("/robot/position", status_code=status.HTTP_201_CREATED)
def PostPosition(position: Position):
    global POSITION

    res_data = position # 받은 좌푯값 

    POSITION["x"] = res_data.x
    POSITION["y"] = res_data.y
    POSITION["z"] = 0.050000

    return {
        "Success_or_not": True,
        "Position": POSITION
    }

@app.get("/robot/position", status_code=status.HTTP_200_OK)
def GetPosition():
    return {
        "Success_or_not": True,
        "Position": POSITION
    }


class Type(BaseModel):
    is_arrived: bool

ISARRIVED = None 

@app.post("/robot/isarrived", status_code=status.HTTP_201_CREATED)
def IsArrived(type: Type):
    type = type 

    ISARRIVED = type.is_arrived

    return {
        "Success_or_not": True,
        "IsArrived": ISARRIVED
    }

@app.get("/robot/isarrived", status_code=status.HTTP_200_OK)
def IsArrived():
    return {
        "Success_or_not": True,
        "IsArrived": ISARRIVED
    }
    


# 로봇에서 수화물이 적재 되었다고 신호를 보내면 POST 전송 
@app.post("/load", status_code=status.HTTP_201_CREATED)
def Load():
    # 이 사이에 도착했다는 결과가 와야함.

    return {
        "Success_or_not": True
    }

# 로봇에서 수화물이 양하 되었다고 신호를 보내면 POST 전송 
@app.post("/unload", status_code=status.HTTP_201_CREATED)
def Load():
    return {
        "Success_or_not": True
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)