from models.singer import SingerOrm


def convert_orm_to_dict(singer: SingerOrm) -> dict:
    singer = {
        "id": singer.id,
        "name": singer.name,
        "genre": singer.genre,
        "albums_count": singer.albums_count,
    }
    return singer
