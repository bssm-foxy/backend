import pymysql
import asyncio
import aiomysql

from database.config.db_config import DB_CONFIG

        
async def SetPointQueryAsync(start_point, finish_point):
    conn = await aiomysql.connect(**DB_CONFIG)

    try:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT Number FROM SetPoint WHERE TimeLog = (SELECT MAX(TimeLog) FROM SetPoint)")
            result = await cursor.fetchone()

            if result:
                latest_number = result[0]
            else:
                latest_number = 0 
            
            query = f"""INSERT INTO SetPoint (TimeLog, Number, StartPoint, FinishPoint) \
                            VALUES (CURRENT_TIMESTAMP, {latest_number + 1}, '{start_point}', '{finish_point}');
                            
                        INSERT INTO StartPointArrived (TimeLog, Number, GoalPoint, IsArrived) \
                            VALUES (CURRENT_TIMESTAMP, {latest_number + 1}, '{start_point}', {False})
                    """
                        # 도착지 데이터베이스 insert도 추가해야함
                        
            await cursor.execute(query)
            await conn.commit()
            print("데이터가 생성되었습니다.")

    except aiomysql.Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def GetStartPoint():
    conn = pymysql.connect(**DB_CONFIG)

    try: 
        if conn.open:
            with conn.cursor() as cursor: 
                query = "SELECT StartPoint FROM SetPoint Where Number = (SELECT MAX(Number) FROM SetPoint);"
                cursor.execute(query)
                point_name = cursor.fetchone()[0]
                print(point_name) # 출발지 이름 출력 
                
                if point_name:
                    # 수정 필요 (Test_Location)
                    query = f"SELECT Position_X, Position_Y FROM Test_Locations WHERE PointName = '{point_name}';"
                    cursor.execute(query)
                    start_point = cursor.fetchone()
            
                    if start_point:
                        point_x, point_y = start_point[0], start_point[1]
                        print(f"{point_name} 좌표 ({point_x}, {point_y})가 리턴되었습니다.")
                        return {
                            "point_name": point_name,
                            "point_x": point_x,
                            "point_y": point_y
                        }
                    else:
                        print(f"{point_name}에 해당하는 좌표가 데이터베이스에 없습니다.")
                else:
                    print("최근 SetPoint 데이터가 없습니다.")
    
    except pymysql.Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def ReturnLatestStartPosition():
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            query = f"""
                    SELECT PointName, TL.Position_X, TL.Position_Y 
                    FROM SetPoint SP
                    JOIN Test_Locations TL ON SP.StartPoint = TL.PointName
                    WHERE SP.Number = (SELECT MAX(Number) FROM SetPoint);
                    """
            cursor.execute(query)
            positions = cursor.fetchone()
            
            if positions:
                point_name, position_x, position_y = positions 

                return {
                    "point_name": point_name,
                    "position_x": position_x, 
                    "position_y": position_y
                }

    except pymysql.Error as e: 
        print("ReturnLatestStartPosition Error")
        print(e)
    
    finally:
        if conn:
            conn.close()


## 목적지로 도착시 Ture 반환 코드 --- 
def Arrived():
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            # 도착시 is_arrived 값을 True로 변경 
            query = """
                    UPDATE StartPointArrived AS T1
                    JOIN (SELECT MAX(Number) AS MaxNumber FROM StartPointArrived) AS T2
                    ON T1.Number = T2.MaxNumber
                    SET T1.IsArrived = True;
                    """
            cursor.execute(query)
            conn.commit()

    except pymysql.Error as e:
        print(f"데이터를 수정하는 과정에서 에러가 발생하였습니다: {e}")

    finally:
        if conn:
            conn.close()

def CheckArrivedValue():  # 도착하였는지 확인하는 코드 
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            query = """
                    SELECT IsArrived FROM StartPointArrived \
                        WHERE Number = (SELECT MAX(Number) FROM StartPointArrived);
                    """
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                print("데이터가 없음")

    except pymysql.Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

async def WaitUntilArrived(timeout: int) -> bool:  # 도착할 때까지 계속 확인 
    start_time = asyncio.get_event_loop().time()

    while True:
        is_arrived = CheckArrivedValue()
        if is_arrived:
            return True
        elif asyncio.get_event_loop().time() - start_time >= timeout:
            return False
        else:
            await asyncio.sleep(1)  # 1초 대기 후 다시 체크


if __name__ == "__main__":
    ReturnLatestStartPosition()