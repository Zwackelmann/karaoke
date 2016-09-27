import sys
import rds_config
import psycopg2
import time
import random


# rds settings
rds_host = rds_config.host
db_username = rds_config.db_username
db_password = rds_config.db_password
db_name = rds_config.db_name
port = 5432

server_address = (rds_host, port)

num_artists_fetch_interval = 60*60  # 1h
last_fetched_num_artists = None
num_artists = None

try:
    print "Connecting to PostgresDB"
    conn = psycopg2.connect(host=rds_host, port=port, user=db_username, password=db_password, database=db_name)
    print "Connected"

    cur = conn.cursor()
    cur.execute("""PREPARE random_artists AS
                   SELECT id, name FROM(
                     (SELECT id, name FROM artist OFFSET $1 LIMIT 1) UNION ALL
                     (SELECT id, name FROM artist OFFSET $2 LIMIT 1) UNION ALL
                     (SELECT id, name FROM artist OFFSET $3 LIMIT 1)
                   ) AS random_artists""")

    print "prepared random_artists stmt"

    cur.execute("""PREPARE count_artists AS SELECT COUNT(*) AS num_artists FROM artist""")
    print "prepared count_artists stmt"
except psycopg2.Error as e:
    print "Connection failed: ", e
    sys.exit()


def handler(event, _):
    global num_artists
    global last_fetched_num_artists

    if last_fetched_num_artists is None or time.time() - last_fetched_num_artists > num_artists_fetch_interval:
        cur.execute("""EXECUTE count_artists""")
        for row in cur.fetchall():
            num_artists = row[0]

        last_fetched_num_artists = time.time()
        print "Updated num_artists to %d" % (num_artists, )

    seed = event.get('seed', int(random.random()*pow(2, 31)))
    offset = event.get('offset', 0)

    random.seed(seed)
    artist_ord_list = list(xrange(num_artists))
    random.shuffle(artist_ord_list)

    offsets = [(offset+i) % num_artists for i in range(3)]
    artist_query_ords = [artist_ord_list[o] for o in offsets]

    cur.execute("""EXECUTE random_artists(%s, %s, %s)""", tuple(artist_query_ords))

    artists = []
    for row in cur.fetchall():
        artist_id = row[0]
        artist_name = row[1]

        artists.append({'artist_id': artist_id, 'artist_name': artist_name})

    return {'artists': artists, 'seed': seed, 'next_offset': offset + 3}
