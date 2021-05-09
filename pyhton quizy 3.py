import requests
import json
import sqlite3

conn=sqlite3.connect("similar.sqlite")
c=conn.cursor()
c.execute(""" create table if not exists Similar
    (
        id integer primary key autoincrement,
        movies varchar(50),
        musics varchar(50)
    )
""")
KEY="412462-Kacho-I4T05PRU"
query=input("შეიყვანეთ სასურველი ფილმი ან მუსიკოსი : ")
r = requests.get(f'https://tastedive.com/api/similar?q={query}&k={KEY}')
res=r.json()
resp=json.dumps(res,indent=4)
print(r.headers["Date"])
print(r.status_code)
print(res["Similar"]["Results"][0]["Name"])
with open('quizyy.json', 'w') as file:
    json.dump(res, file, indent=3)
allrows=[]
for each in res["Similar"]["Results"]:
    movies=" "
    musics=" "
    if (each["Type"]=="movie"):
        movies=each["Name"]
    elif(each["Type"]=="music"):
        musics=each["Name"]
    rows=(movies,musics)
    allrows.append(rows)
c.execute('delete from similar')
conn.commit()
c.executemany('insert into similar (movies,musics) values (?,?)',allrows)
conn.commit()
c.close()
