import pymysql

from pymysql import MySQLError

from database.config.db_config import DB_CONFIG


def create_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['db'],
            port=DB_CONFIG['port'],
            cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리 형태로 반환
        )
        print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
    except MySQLError as e:
        print(f"Error: '{e}' 발생")
    return connection

def close_connection(connection):
    """ 데이터베이스 연결을 닫습니다. """
    if connection:
        connection.close()
        print("MySQL 데이터베이스 연결이 종료되었습니다.")


if __name__ == "__main__":
    connection = create_connection() 
    close_connection(connection)
