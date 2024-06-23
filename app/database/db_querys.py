import pymysql
import asyncio
import aiomysql

from database.config.db_config import DB_CONFIG

#  PEP8 문법 적용된 코드
#  수정 전 이름: SetPoint
import pymysql
from database.config.db_config import DB_CONFIG  # DB_CONFIG를 정의한 모듈을 import 해야 합니다.


async def set_load_true():
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Number FROM setPoint WHERE Number = (SELECT MAX(Number) FROM SetPoint);")
            result = cursor.fetchone()
            
            # 새로운 데이터의 Number 값을 설정합니다.
            latest_number = int(result[0]) + 1 if result else 1

            # query = f"INSERT INTO SetLoad (TimeLog, Number, IsLoad) VALUES (CURRENT_TIMESTAMP, {latest_number}, false);"
            # cursor.execute(query)

            query = f"UPDATE SetLoad SET IsLoad = true WHERE Number = {latest_number};"
            cursor.execute(query)
            conn.commit()

    except pymysql.Error as e:
        # 데이터베이스 에러가 발생한 경우 이를 출력합니다.
        print("Database error occurred:", e)
        raise  # 에러를 다시 발생시켜 호출자에게 전달합니다.

    finally:
        # 커넥션을 닫습니다.
        if conn:
            conn.close()
        
async def insert_load():
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Number FROM setPoint WHERE Number = (SELECT MAX(Number) FROM SetPoint);")
            result = cursor.fetchone()
            
            # 새로운 데이터의 Number 값을 설정합니다.
            latest_number = int(result[0]) + 1 if result else 1

            query = f"INSERT INTO SetLoad (TimeLog, Number, IsLoad) VALUES (CURRENT_TIMESTAMP, {latest_number}, false);"
            cursor.execute(query)

            # query = f"UPDATE SetLoad SET IsLoad = true WHERE Number = {latest_number};"
            # cursor.execute(query)
            conn.commit()

    except pymysql.Error as e:
        # 데이터베이스 에러가 발생한 경우 이를 출력합니다.
        print("Database error occurred:", e)
        raise  # 에러를 다시 발생시켜 호출자에게 전달합니다.

    finally:
        # 커넥션을 닫습니다.
        if conn:
            conn.close()


async def init_location_info(start_point: str, finish_point: str):
    # pymysql을 사용하여 데이터베이스에 연결합니다.
    conn = pymysql.connect(**DB_CONFIG)
    
    try:
        with conn.cursor() as cursor:
            # 가장 최근 Number 값을 가져옵니다.
            cursor.execute("SELECT Number FROM setPoint WHERE Number = (SELECT MAX(Number) FROM SetPoint);")
            result = cursor.fetchone()
            
            # 새로운 데이터의 Number 값을 설정합니다.
            latest_number = int(result[0]) + 1 if result else 1
            
            # 새로운 데이터를 SetPoint 테이블에 삽입합니다.
            query1 = (
                f"""
                INSERT INTO SetPoint (TimeLog, Number, StartPoint, FinishPoint) 
                VALUES (CURRENT_TIMESTAMP, {latest_number}, '{start_point}', '{finish_point}');
                """
            )
            # 출발지 도착 정보를 StartPointArrived 테이블에 삽입합니다.
            query2 = (
                f"""
                INSERT INTO StartPointArrived (TimeLog, Number, GoalPoint, IsArrived) 
                VALUES (CURRENT_TIMESTAMP, {latest_number}, '{start_point}', {False});
                """
            )
            # 도착지 도착 정보를 FinishPointArrived 테이블에 삽입합니다.
            query3 = (
                f"""
                INSERT INTO FinishPointArrived (TimeLog, Number, GoalPoint, IsArrived) 
                VALUES (CURRENT_TIMESTAMP, {latest_number}, '{finish_point}', {False});
                """
            )

            # SQL 쿼리를 실행합니다.
            cursor.execute(query1)
            cursor.execute(query2)
            cursor.execute(query3)
            
            # 변경 사항을 커밋하여 데이터베이스에 저장합니다.
            conn.commit()
            print(f"{latest_number}번째 데이터, 출발지: {start_point}, 도착지: {finish_point}가 생성되었습니다.")

    except pymysql.Error as e:
        # 데이터베이스 에러가 발생한 경우 이를 출력합니다.
        print("Database error occurred:", e)
        raise  # 에러를 다시 발생시켜 호출자에게 전달합니다.

    finally:
        # 커넥션을 닫습니다.
        if conn:
            conn.close()


#  PEP8 문법 적용된 코드 ✅
#  출발지 좌표 
#  수정 전 이름: GetStartPoint
#  수정 사항: print("최근 SetPoint 데이터가 없습니다.") 수정 필요함.
def search_location_info(start_or_finish):
    conn = pymysql.connect(**DB_CONFIG)

    try: 
        if conn.open:
            with conn.cursor() as cursor: 
                if start_or_finish == "start":
                    query = "SELECT StartPoint FROM SetPoint Where Number = (SELECT MAX(Number) FROM SetPoint);"
                else:
                    query = "SELECT FinishPoint FROM SetPoint Where Number = (SELECT MAX(Number) FROM SetPoint);"

                cursor.execute(query)
                location_name = cursor.fetchone()[0]
                
                if location_name:
                    #  실제 작동시 수정 필요 (Test_Location -> <실제 맵 데이터 테이블>)
                    query = f"SELECT Position_X, Position_Y FROM Test_Locations WHERE PointName = '{location_name}';"
                    cursor.execute(query)
                    start_locatioin_info = cursor.fetchone()
            
                    if start_locatioin_info:
                        location_x, location_y = start_locatioin_info[0], start_locatioin_info[1]  # x, y 
                        print(f"{location_name} 좌표 ({location_x}, {location_y})")
                        return {
                            "name": location_name,
                            "locations": {
                                "x": location_x,
                                "y": location_y
                            }
                        }
                    else:
                        print(f"{location_name}에 해당하는 좌표가 데이터베이스에 없습니다.")
                else:
                    print("최근 SetPoint 데이터가 없습니다.")

    except pymysql.Error as e:
        #  변경해야할 사항 
        #  - 에러 출력 자세허게  
        #   - 진행 여부: ❌ 
        print(e)

    finally:
        if conn:
            conn.close()

#  변경 전 이름: StartArrived
def location_arrived(start_or_finish):
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            if start_or_finish == "start":  # 출발지 도착 여부 설정 
                start_location_arrived_query = ( 
                    """
                    UPDATE StartPointArrived AS T1
                    JOIN (SELECT MAX(Number) AS MaxNumber FROM StartPointArrived) AS T2
                    ON T1.Number = T2.MaxNumber
                    SET T1.IsArrived = True;
                    """
                )       
                cursor.execute(start_location_arrived_query)
            else:  # 도착지 도착 여부 설정 
                finish_location_arrived_query = (
                    """
                    UPDATE FinishPointArrived AS T1
                    JOIN (SELECT MAX(Number) AS MaxNumber FROM FinishPointArrived) AS T2
                    ON T1.Number = T2.MaxNumber
                    SET T1.IsArrived = True;
                    """
                )
                cursor.execute(finish_location_arrived_query)
            conn.commit()

    except pymysql.Error as e:
        print(f"도착 여부를 수정하는 중 에러가 발생하였습니다.: {e}")

    finally:
        if conn:
            conn.close()

def check_arrived_value(start_or_finish):  # 도착하였는지 확인하는 코드 
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            if start_or_finish == "start":  # 출발지 도착 여부 확인 
                arrived_start_location_query = (
                    """
                    SELECT Number, IsArrived FROM StartPointArrived 
                    WHERE Number = (SELECT MAX(Number) FROM StartPointArrived);
                    """
                )
                cursor.execute(arrived_start_location_query)
            else:  # 도착지 도착 여부 확인 
                arrived_finish_location_query = (
                    """
                    SELECT Number, IsArrived FROM FinishPointArrived 
                    WHERE Number = (SELECT MAX(Number) FROM FinishPointArrived);
                    """
                )
                cursor.execute(arrived_finish_location_query)

            result = cursor.fetchone()

            if result:
                return {
                    "latest_number": result[0],
                    "status": result[1]
                }
            else:
                print("데이터가 없음")

    except pymysql.Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

async def wait_until_arrived(timeout: int, start_or_finish: str) -> bool:  # 도착할 때까지 계속 확인, bool type으로 리턴 
    start_time = asyncio.get_event_loop().time() 

    while True: 
        is_arrived = check_arrived_value(start_or_finish)["status"]
        if is_arrived:
            return True 
        elif asyncio.get_event_loop().time() - start_time >= timeout:
            return False
        else:
            await asyncio.sleep(1)  # 1초 대기 후 다시 체크 

def load_stats():
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            query = "select isLoad from Setload where number = (SELECT MAX(Number) FROM setload);"
            cursor.execute(query)

            result = cursor.fetchone()

            latest_number = int(result[0]) if result else 1

            return {
                "number": latest_number
            }
    
    except pymysql.Error as e:
        print(e)
    
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    pass