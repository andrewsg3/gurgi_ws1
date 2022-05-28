import psycopg2
conn = psycopg2.connect(host="localhost", user="gurgi", database="gurgibase", password="rocket")
cur = conn.cursor()

tablename="session_2022_05_28_12h45m00s"

def query(conn, cur, cols, n, tablename):
	res = []
	statement = f"SELECT pressure, humidity, temperature FROM {tablename} ORDER BY epoch LIMIT {n}"
	statement = f"SELECT AVG(pressure), AVG(humidity), AVG(temperature) FROM ({statement}) as a"
	cur.execute(statement)
	print(statement)
	res.append(cur.fetchone())
	conn.commit()
	return res

cols = "AVG(pressure), AVG(humidity), AVG(temperature)"

res = query(conn, cur, cols, 100, tablename)
print(len(res))
print(len(res[0]))
print(res)
