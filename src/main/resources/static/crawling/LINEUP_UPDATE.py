import pandas as pd
import numpy as np

#pip install mysql-connector-python
import mysql.connector

### 데이터테이블 전부 str로 변경

connection = mysql.connector.connect(
    host="13.124.23.77",
    user="root",
    passwd="!Q2w3e4r",
    database="KBO"
)

cursor = connection.cursor()

# 데이터베이스 내 모든 테이블 조회
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# 각 테이블의 열 타입 변경
for table in tables:
    table_name = table[0]
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()

    try:
        cursor.execute(f"ALTER TABLE {table_name} DROP PRIMARY KEY")
    except:
        pass
    
    for column in columns:
        column_name = column[0]
        cursor.execute(f"ALTER TABLE {table_name} MODIFY {column_name} VARCHAR(255)")

    
    cursor.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY (idx)")
        #print(f"Changed column type of {table_name}.{column_name} to VARCHAR(255)")
            
# 변경 사항 저장
connection.commit()

# 연결 종료
cursor.close()
connection.close()

connection = mysql.connector.connect(
    host="13.124.23.77",
    user="root",
    passwd="!Q2w3e4r",
    database="KBO"
)

cursor = connection.cursor()

df_next_lineup = pd.read_csv('tomorrow_lineup.csv')
df_next_lineup['idx'] = df_next_lineup['idx'].apply(lambda x: str(x).zfill(6))

table_exists_query = "SHOW TABLES LIKE 'tomorrow_lineup'"
cursor = connection.cursor()
cursor.execute(table_exists_query)
result = cursor.fetchone()

if result:
    delete_query = "DELETE FROM tomorrow_lineup"
    cursor.execute(delete_query)

    # 새로운 데이터 추가 (모든 데이터를 문자열로 변환)
    columns = ', '.join(df_next_lineup.columns)  # 열 이름들을 쉼표로 구분하여 문자열로 만듦
    values = ', '.join(['%s'] * len(df_next_lineup.columns))  # 삽입할 값들에 대한 placeholder를 생성
    insert_query = f"INSERT INTO tomorrow_lineup ({columns}) VALUES ({values})"
    data = [tuple(str(value) for value in row) for row in df_next_lineup.values]  # 모든 데이터를 문자열로 변환하여 튜플 형태로 변환
    cursor.executemany(insert_query, data)

    # 변경 사항을 커밋하여 DB에 적용
    print("라인업 DB 추가 완료")
    connection.commit()
else:
    print("tomorrow_lineup 테이블이 존재하지 않습니다.")

# 연결 종료
cursor.close()
connection.close()


for CSV in ['hit_recent.csv','pit_recent.csv']:
    connection = mysql.connector.connect(
        host="13.124.23.77",
        user="root",
        passwd="!Q2w3e4r",
        database="KBO"
    )
    
    cursor = connection.cursor()
    
    df_next_lineup = pd.read_csv(CSV)
    df_next_lineup['idx'] = df_next_lineup['idx'].apply(lambda x: str(x).zfill(6))
    table_exists_query = f"SHOW TABLES LIKE '{CSV[:-4]}'"
    cursor = connection.cursor()
    cursor.execute(table_exists_query)
    result = cursor.fetchone()
    
    if result:
        delete_query = f"DELETE FROM {CSV[:-4]}"
        cursor.execute(delete_query)
    
        # 새로운 데이터 추가 (모든 데이터를 문자열로 변환)
        columns = ', '.join(df_next_lineup.columns)  # 열 이름들을 쉼표로 구분하여 문자열로 만듦
        values = ', '.join(['%s'] * len(df_next_lineup.columns))  # 삽입할 값들에 대한 placeholder를 생성
        insert_query = f"INSERT INTO {CSV[:-4]} ({columns}) VALUES ({values})"
        data = [tuple(str(value) for value in row) for row in df_next_lineup.values]  # 모든 데이터를 문자열로 변환하여 튜플 형태로 변환
        cursor.executemany(insert_query, data)
    
        # 변경 사항을 커밋하여 DB에 적용
        print(f"{CSV[:-4]} DB 추가 완료")
        connection.commit()
    else:
        print(f"{CSV[:-4]} 테이블이 존재하지 않습니다.")
    
    # 연결 종료
    cursor.close()
    connection.close()


connection = mysql.connector.connect(
    host="13.124.23.77",
    user="root",
    passwd="!Q2w3e4r",
    database="KBO"
)

cursor = connection.cursor()

# 데이터베이스 내 모든 테이블 조회
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# 각 테이블의 열 타입 변경
for table in tables:
    table_name = table[0]
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()

    try:
        cursor.execute(f"ALTER TABLE {table_name} DROP PRIMARY KEY")
    except:
        pass
    
    for column in columns:
        column_name = column[0]
        cursor.execute(f"ALTER TABLE {table_name} MODIFY {column_name} VARCHAR(255)")

    
    cursor.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY (idx)")
        #print(f"Changed column type of {table_name}.{column_name} to VARCHAR(255)")
            
# 변경 사항 저장
connection.commit()

# 연결 종료
cursor.close()
connection.close()
    

print("MySQL 연결 종료")
