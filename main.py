# main.py

from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(openapi_prefix="/")

origins = [
    "http://localhost:3000",  # 허용할 Origin을 여기에 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    start_point: str
    finish_point: str 
    

# 로봇에서 도착되었다고 뜰 때까지 대기한 후 POST 전송 
@app.post("/point/", status_code=status.HTTP_201_CREATED)
def Point():
    return {
        "Success_or_not": True
    }

# 로봇에서 수화물이 적재 되었다고 신호를 보내면 POST 전송 
@app.post("/load", status_code=status.HTTP_201_CREATED)
def Load():
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