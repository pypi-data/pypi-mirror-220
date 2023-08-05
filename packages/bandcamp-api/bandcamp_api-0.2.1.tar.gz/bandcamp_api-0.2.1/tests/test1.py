from bandcamp_api import Bandcamp

bc = Bandcamp()

artist = bc.get_artist(artist_url="https://lesfriction.bandcamp.com/album/les-friction")
print("Artist Name:", artist.artist_title, "(", artist.artist_id, ")")


print("Album IDs:", artist.album_ids)

for albumid in artist.album_ids:
    album = bc.get_album(album_id=albumid, artist_id=artist.artist_id)
    print(albumid, "-", album.album_url)
    print('\tAlbum Price:', album.price)

    if "2277197926" in str(albumid):
        print(album.tracks[0].price)