import sys
import logging
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
    print "connected"
except psycopg2.Error as e:
    print "Connection failed"
    sys.exit()


def insert_artists(filepath):
    with open(filepath) as f:
        artists = set()

        for line in f:
            parts = line.strip().split(";")
            if len(parts) != 2:
                continue

            artist = parts[0]

            artists.add(artist)

    cur = conn.cursor()
        
    cur.execute("""PREPARE insert_artist AS 
                   INSERT INTO artist(name) 
                   VALUES ($1)""")

    for name in artists:
        cur.execute("""EXECUTE insert_artist (%s)""", (name,))

    conn.commit()


def insert_songs(filepath):
    cur = conn.cursor()
        
    cur.execute("""PREPARE insert_song AS
                   INSERT INTO song (artist, title, artist_title)
                   VALUES ((SELECT id FROM artist WHERE name=$1), $2, $1 || ' ' || $2)""")

    with open(filepath) as f:
        for line in f:
            parts = line.strip().split(";")
            if len(parts) != 2:
                continue

            artist = parts[0]
            title = parts[1]

            print artist, title
            cur.execute("""EXECUTE insert_song(%s, %s)""", (artist, title))

    conn.commit()
