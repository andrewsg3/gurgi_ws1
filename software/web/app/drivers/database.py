## Connect to psql database
import psycopg2
import configparser
import datetime
config=configparser.ConfigParser()
config.read('config.ini')

dbname = config['DATABASE']['DBNAME'] # The name of an existing database
username = config['DATABASE']['USERNAME']
mypass = config['DATABASE']['PASSWORD']
init_date = datetime.datetime.now().strftime(f"%Y_%m_%d_%Hh%Mm%Ss")
tablename = f"Session_{init_date}"
print("Connecting to SQL database...")
try:
    conn = psycopg2.connect( # Connect to database
        host="localhost",
        database=dbname,
        user=username,
        password=mypass,
    )
    print("Connected!")
except:
    print(f"ERROR! Could not connect to database '{dbname}'. Speak to a system admin. Exiting program...")
    raise SystemExit(0)

cur=conn.cursor() # Create a cursor
user_cur = conn.cursor()
print("Testing an execute statement...")
cur.execute("SELECT version()")
print("Success. Cursor object is working correctly.")
print(f'PostgreSQL database version: {cur.fetchone()} ') 

cols = ["epoch", "date", "time", "pressure", "humidity", "temperature", "wind_speed", "rain", "wind_direction"]
datatype = ["FLOAT", "VARCHAR(30)", "VARCHAR(30)", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT"]

def create_table(tablename,cols, datatype):
    global conn, cur
    statement = f"CREATE TABLE {tablename}("
    i = 0
    while i < len(cols):
        statement += f"{cols[i]} {datatype[i]}"
        if i < len(cols)-1:
            statement +=", "
        i+=1
    statement += ");"
    print(statement)
    cur.execute(statement)
    conn.commit()

create_table(tablename, cols, datatype)
print(f"Table {tablename} created.")

def insert(tablename, cur, conn, res):
    statement = f"INSERT INTO {tablename}(epoch, date, time, pressure, humidity, temperature, wind_speed, rain, wind_direction) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);" # 
    statement = cur.mogrify(statement, res)
    cur.execute(statement)
    conn.commit()

def query(tablename, user_cur, conn, cols, n):
    s1 = f"AVG({cols[0]}), AVG({cols[1]}), AVG({cols[2]}), AVG({cols[3]}), AVG({cols[4]}), AVG({cols[5]})"
    s2 = f"{cols[0]}, {cols[1]}, {cols[2]}, {cols[3]}, {cols[4]}, {cols[5]}"
    statement = f"SELECT {s1} FROM (SELECT {s2} FROM {tablename} ORDER BY epoch DESC LIMIT {n}) AS a"
    user_cur.execute(statement)
    conn.commit()
    res = []
    for i in user_cur.fetchone():
        if i != None:
            res.append(round(i,2))
        else:
            res.append(i)
    return res