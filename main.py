# main.py

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    start_point: str
    finish_point: str 
    
@app.get("/")
def home():
    return "Hello"

# 로봇에서 도착되었다고 뜰 때까지 대기한 후 POST 전송 
@app.post("/point/", status_code=status.HTTP_201_CREATED)
def Point():
    import time 
    time.sleep(10) # 테스트를 위해 10초 대기 
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