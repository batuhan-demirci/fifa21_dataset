from utils.db_connection_manager import connect, close

conn, cur = connect()

cur.execute("SELECT str_url FROM tbl_player_urls")

for str_url in cur.fetchall():
    print(str_url)

close(conn, cur)
