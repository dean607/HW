import json
import sqlite3
x=0

def movies_db():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn
with movies_db() as conn:
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE if not exists "movies" (
	    "id"	INTEGER,
	    "title"	TEXT NOT NULL,
	    "director"	TEXT NOT NULL,
	    "genre"	TEXT NOT NULL,
	    "year"	INTEGER NOT NULL,
	    "rating"	REAL CHECK(rating >= 1.0 and rating <= 10.0),
	    PRIMARY KEY("id" AUTOINCREMENT)
        )'''
    )
    while x!='7' :
        try:
            print("----- 電影管理系統 -----")
            print("1. 匯入電影資料檔")
            print("2. 查詢電影")
            print("3. 新增電影")
            print("4. 修改電影")
            print("5. 刪除電影")
            print("6. 匯出電影")
            print("7. 離開系統")
            print("------------------------")
            x=input("請選擇操作選項 (1-7):")
            if x =='1':
                # 匯入電影資料檔
                with open('movies.json', 'r', encoding='UTF-8') as f:
                    a = json.load(f)
                for i in range(0,len(a)) :
                    cursor.execute("INSERT INTO movies (title, director, genre, year, rating) VALUES ( ?, ?, ?, ?, ?)",
                                   (a[i]['title'], a[i]['director'], a[i]['genre'], a[i]['year'], a[i]['rating']))
                print("電影已匯入")
            elif x =='2':
                # 查詢電影
                c=input("查詢全部電影嗎？(y/n):")
                if c=='y':
                    t='0'
                    cursor.execute('SELECT * FROM movies')
                    result_all = cursor.fetchall()
                    for row in result_all:
                        if t!='1':
                            print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<10}{'評分':{chr(12288)}<10}")
                            print("------------------------------------------------------------------------")
                        t='1'
                        print(f"{row[1]:{chr(12288)}<10}{row[2]:{chr(12288)}<10}{row[3]:{chr(12288)}<10}{row[4]:{chr(12288)}<10}{row[5]:{chr(12288)}<10}")
                    if t =='0':
                        print("查無資料")
                elif c=='n':
                    n=input("請輸入電影名稱:")
                    n='%'+n+'%'
                    t='0'
                    cursor.execute("SELECT * FROM movies WHERE title LIKE ?",(n,))
                    result_all = cursor.fetchall()
                    for row in result_all:
                        if t!='1':
                            print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<10}{'評分':{chr(12288)}<10}")
                            print("------------------------------------------------------------------------")
                        t=1
                        print(f"{row[1]:{chr(12288)}<10}{row[2]:{chr(12288)}<10}{row[3]:{chr(12288)}<10}{row[4]:{chr(12288)}<10}{row[5]:{chr(12288)}<10}")
                    if t =='0':
                        print("查無資料")
                else:
                    print("無效輸入")
            elif x =='3':
                # 新增電影
                n=input("電影名稱:")
                nn=input("導演:")
                nnn=input("類型:")
                nnnn=input("上映年份:")
                nnnnn=input("評分 (1.0 - 10.0):")
                cursor.execute("INSERT INTO movies (title, director, genre, year, rating)VALUES ( ?, ?, ?, ?, ?)",
                               (n ,nn ,nnn ,nnnn ,nnnnn))
                print("電影已新增")
            elif x =='4':
                # 修改電影
                nx=input("請輸入要修改的電影名稱:")
                t='0'
                print()
                cursor.execute("SELECT * FROM movies WHERE title = ?",(nx,))
                result_all = cursor.fetchall()
                for row in result_all:
                    if t!='1':
                        print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<10}{'評分':{chr(12288)}<10}")
                        print("------------------------------------------------------------------------")
                    t=1
                    print(f"{row[1]:{chr(12288)}<10}{row[2]:{chr(12288)}<10}{row[3]:{chr(12288)}<10}{row[4]:{chr(12288)}<10}{row[5]:{chr(12288)}<10}")
                    print()
                if t=='0':
                    print("查無資料")
                else :
                    n=nn=nnn=nnnn=nnnnn=''
                    n=input("請輸入新的電影名稱 (若不修改請直接按 Enter):")
                    nn=input("請輸入新的導演 (若不修改請直接按 Enter):")
                    if nn !='' :
                        cursor.execute('UPDATE movies SET director = ? WHERE title = ?', (nn, nx))
                    nnn=input("請輸入新的類型 (若不修改請直接按 Enter):")
                    if nnn !='' :
                        cursor.execute('UPDATE movies SET genre = ? WHERE title = ?', (nnn, nx))
                    nnnn=input("請輸入新的上映年份 (若不修改請直接按 Enter):")
                    if nnnn !='' :
                        cursor.execute('UPDATE movies SET year = ? WHERE title = ?', (nnnn, nx))
                    nnnnn=input("請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter):")
                    if nnnnn !='' :
                        cursor.execute('UPDATE movies SET rating = ? WHERE title = ?', (nnnnn, nx))
                    if n !='' :
                        cursor.execute('UPDATE movies SET title = ? WHERE title = ?', (n, nx))
                    print("資料已修改")
            elif x =='5':
                # 刪除電影
                c=input("刪除全部電影嗎？(y/n):")
                if c =='y':
                    y=input("是否要刪除(y/n):")
                    if y=='y':
                        cursor.execute('DELETE FROM movies')
                        print("電影已刪除")
                    elif y!='n':
                        print("無效輸入")
                elif c=='n':
                    n=input("請輸入要刪除的電影名稱:")
                    n='%'+n+'%'
                    t='0'
                    cursor.execute("SELECT * FROM movies WHERE title LIKE ?",(n,))
                    result_all = cursor.fetchall()
                    for row in result_all:
                        if t!='1':
                            print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<10}{'評分':{chr(12288)}<10}")
                            print("------------------------------------------------------------------------")
                            n=row[1]
                        t=1
                        print(f"{row[1]:{chr(12288)}<10}{row[2]:{chr(12288)}<10}{row[3]:{chr(12288)}<10}{row[4]:{chr(12288)}<10}{row[5]:{chr(12288)}<10}")
                    if t =='0':
                        print("查無資料")
                    else:
                        y=input("是否要刪除(y/n):")
                        if y=='y':
                            cursor.execute('DELETE FROM movies WHERE title = ?', (n,))
                            print("電影已刪除")
                        elif y!='n':
                            print("無效輸入")
            elif x =='6':
                #  匯出電影
                with open('exported.json', 'w', encoding='UTF-8') as f:
                    c=input("匯出全部電影嗎？(y/n):")
                    if c=='y':
                        cursor.execute("SELECT * FROM movies")
                        result_all = cursor.fetchall()
                        for row in result_all:
                            e={"title": row[1],"director": row[2],"genre": row[3],"year": row[4],"rating": row[5]}
                            json.dump( e, f, ensure_ascii=False, indent=4)
                        print("電影資料已匯出至 exported.json")
                    elif c=='n':
                        n=input("請輸入要匯出的電影名稱:")
                        t='0'
                        cursor.execute("SELECT * FROM movies WHERE title = ?",(n,))
                        result_all = cursor.fetchall()
                        for row in result_all:
                            t='1'
                            e={"title": row[1],"director": row[2],"genre": row[3],"year": row[4],"rating": row[5]}
                            json.dump( e, f, ensure_ascii=False, indent=4)
                        if t=='1':
                            print("電影資料已匯出至 exported.json")
                        else :
                            print("查無資料")
                    else:
                        print("無效輸入")
            elif x!='7':
                # 例外處理
                print("無效輸入")
            print()
        except:
            print('發生錯誤')