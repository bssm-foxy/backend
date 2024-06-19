import uvicorn

from fastapi import FastAPI
from app.endpoints import router

app = FastAPI()

# 엔드포인트 라우터 추가
app.include_router(router)

# FastAPI 서버 실행 (uvicorn을 사용하는 경우)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)