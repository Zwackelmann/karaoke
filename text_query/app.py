import sys
import rds_config
import psycopg2
import json

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

    cur = conn.cursor()
    cur.execute("""
        PREPARE text_query AS
        SELECT * FROM ((
            SELECT
                artist.id AS artist_id,
                artist.name AS artist_name,
                song.id AS song_id,
                song.title AS song_title,
                'song' AS item_type,
                GREATEST(similarity($1, song.title),
                         similarity($1, song.artist_title)) AS similarity
            FROM song JOIN artist ON song.artist=artist.id
            WHERE song.title % $1 OR song.artist_title % $1
        ) UNION ALL (
            SELECT
                id AS artist_id,
                name AS artist_name,
                NULL AS song_id,
                NULL AS song_title,
                'artist' AS item_type,
                similarity($1, name) AS similarity
            FROM artist
            WHERE name % $1
        )) AS query_result
        ORDER BY similarity DESC
        LIMIT 10""")

    print "prepared text query stmt"
except psycopg2.Error as e:
    print "Connection failed"
    sys.exit()


def handler(context, event):
    cur.execute("""EXECUTE text_query(%s)""", (context['q'],))

    artists = []
    songs = []
    for row in cur.fetchall():
        result_item = dict()
        item_type = row[4]

        if item_type == 'artist':
            artist = dict()
            artist['artist_id'] = row[0]
            artist['artist_name'] = row[1]
            artist['similarity_score'] = row[5]
            artists.append(artist)
        elif item_type == 'song':
            song = dict()
            song['artist_id'] = row[0]
            song['artist_name'] = row[1]
            song['song_id'] = row[2]
            song['song_title'] = row[3]
            song['similarity_score'] = row[5]
            songs.append(song)
        else:
            # ignore
            pass

    results = {'artists': sorted(artists, key=lambda x: x['similarity_score'], reverse=True),
               'songs': sorted(songs, key=lambda x: x['similarity_score'], reverse=True)}

    return results
