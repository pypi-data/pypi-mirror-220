import sqlite3
import pandas as pd
from datetime import datetime


def CheckDB(dbname):

    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        print(f'connection {dbname} successfully')
    except:
        print(f'Not Found {dbname}')
        with open(dbname, 'w'):
            conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            print(f'connection {dbname} successfully')

    # DB 初始化
    try:
        cur.execute("SELECT * FROM main;")
    except:
        # columns = ['id', 'date', 'user', 'ip'] # 自主新增欄位
        # columns += ['class', 'time', 'action', 'coordinates', 'duration', 'applicationName', 'href', 'name'] # 原本欄位
            # "id" INT PRIMARY KEY,
        query = """
        CREATE TABLE main(
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "date_time" DATETIME NOT NULL,
            "user" TEXT NOT NULL,
            "computer" TEXT NOT NULL,
            "class" TEXT,
            "action" TEXT,
            "coordinates" TEXT,
            "duration" INTEGER,
            "applicationName" TEXT,
            "href" TEXT,
            "name" TEXT,
            "importdatetime" DATETIME
        )
        """
        cur.execute(query)

    conn.commit()

    return conn


# 列出差異df
def compareDf(df1, df2, which=None):

    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    df1['date_time'] = df1['date_time'].astype(str)
    df2['date_time'] = df2['date_time'].astype(str)

    comparedf = df1.merge(
        df2,
        indicator=True,
        how='outer'
    )
    if which is None:
        diff_df = comparedf[comparedf['_merge'] != 'both']
    else:
        diff_df = comparedf[comparedf['_merge'] != which]

    diff_df = diff_df[diff_df['_merge'] == 'right_only']
    diff_df = diff_df.drop(columns=['_merge'])

    return diff_df

# 匯入資料
def ImportToDB(df:object, conn:object, user:str, computer:str, date:str) -> bool: # 匯入成功返回True, 失敗返回False
    """
    若資料庫該user沒有該日期的資料, 則直接推入
    若資料庫該user存在該日期的資料:
        1. 比較dbdf及df差異的comparedf
        2. 將comparedf資料匯入
    """

    # 查詢資料庫
    selectQuery = f"SELECT * FROM main WHERE user = '{user}' AND date_time BETWEEN '{date} 00:00:00' AND '{date} 23:59:59' AND computer = '{computer}'"
    dbdf = pd.read_sql(selectQuery, con = conn)
    # print(selectQuery)

    # print(f"df len: {len(df)}")

    # 若資料庫該user沒有該日期的資料, 則直接推入
    if len(dbdf) == 0:
        # df['importdatetime'] = datetime.now()
        df['importdatetime'] = datetime.now()
        df = df[['date_time', 'user', 'computer', 'class', 'action', 'coordinates', 'duration', 'applicationName', 'href', 'name', 'importdatetime']]
        # print(df)
        df.to_sql('main', con=conn, if_exists = 'append', index = False)
        return df
    # 若資料庫該user存在該日期的資料:
    else:
        # 1. 比較dbdf及df差異的comparedf
        dbdf = dbdf.drop(columns=['id', 'importdatetime']) # 去除id欄位才能比較
        comparedf = compareDf(dbdf, df)

        if '' in comparedf['date_time'].values:
            comparedf = comparedf.drop(comparedf[comparedf.date_time == ''].index)

        # 若有差異則推入
        if len(comparedf) > 0:
            print(comparedf)
            # 2. 將comparedf資料匯入
            comparedf['importdatetime'] = datetime.now()
            comparedf.to_sql('main', con=conn, if_exists = 'append', index = False)
            print(f'add new {len(comparedf)} data to db')
            return comparedf
        else:
            return pd.DataFrame()