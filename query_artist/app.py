import sys
import rds_config
import psycopg2

# rds settings
rds_host = rds_config.host
db_username = rds_config.db_username
db_password = rds_config.db_password
db_name = rds_config.db_name
port = 5432

server_address = (rds_host, port)

try:
    print "Connecting to PostgresDB"
    conn = psycopg2.connect(host=rds_host, port=port, user=db_username, password=db_password, database=db_name)
    print "Connected"

    cur = conn.cursor()
    cur.execute("""PREPARE artist_query AS
                   SELECT id, title FROM song WHERE artist = $1""")

    print "prepared artist_query stmt"
except psycopg2.Error as e:
    print "Connection failed: ", e
    sys.exit()


def handler(event, context):
    artist_id = event.get('artist_id', None)

    songs = []
    if artist_id is not None:
        cur.execute("""EXECUTE artist_query(%s)""", (artist_id,))

        for row in cur.fetchall():
            song_id = row[0]
            song_title = row[1]
            songs.append({'song_id': song_id, 'song_title': song_title})

    return songs
