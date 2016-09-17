import spotipy
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
    cur.execute("""PREPARE artist_title_query AS
                   SELECT artist_title FROM song WHERE id = $1""")

    print "prepared artist_title query stmt"
except psycopg2.Error as e:
    print "Connection failed: ", e
    sys.exit()


def fetch_item_info(item, extractor_list):
    return dict(((key, extractor(item)) for key, extractor in extractor_list.items()))


def name(item):
    return item.get('name', None)


def spotify_link(item):
    if 'external_urls' in item:
        external_urls = item['external_urls']
        if 'spotify' in external_urls:
            return external_urls['spotify']

    return None


def uri(item):
    return item.get('uri', None)


def preview_url(item):
    return item.get('preview_url', None)


def artists(item):
    if 'artists' in item:
        artist_list = item['artists']
        return [artist.get('name', None) for artist in artist_list]

    return None


def duration(item):
    return item.get('duration_ms', None)


extractors = {
    'song_name': name,
    'spotify_link': spotify_link,
    'uri': uri,
    'preview_url': preview_url,
    'artists': artists,
    'duration': duration
}

sp = spotipy.Spotify()


def handler(event, context):
    limit = event.get('limit', 5)
    song_id = event.get('song_id', None)

    item_info = []
    if song_id is not None:
        cur.execute("""EXECUTE artist_title_query(%s)""", (song_id,))

        artist_title = None
        for row in cur.fetchall():
            artist_title = row[0]

        if artist_title is not None:
            try:
                results = sp.search(q=artist_title, limit=limit)

                items = results['tracks']['items']
                item_info = [fetch_item_info(item, extractors) for item in items]
            except spotipy.client.SpotifyException:
                pass

    return item_info
