from typing import List, Optional
from fastapi import Request, Query
from fastapi.responses import RedirectResponse

from app import Router, Schema, db
from app.api.games.maimai.models import Difficulty, Music, MusicGenre, Genres
from .. import templates


router = Router(__name__)


class SearchSchema(Schema):
    #level: Optional[List[str]]
    genre: Optional[List[int]]
    text: Optional[str]


@router.get('/')
async def maimai_index():
    return RedirectResponse(router.url_path_for('maimai_musics'))


@router.get('/musics')
async def maimai_musics(
    req: Request, page: int = 1,  *,
    #level: List[int] = Query([]),
    genre: List[str] = Query([]),
    text: str = Query(''),
    artist: str = Query(''),
):
    query = db.session.query(Music).join(Difficulty)
    #if level:
    #    query = query.filter(Difficulty.level.in_(map(int, level)))
    if genre:
        genres = [Genres[x] for x in genre]
        query = query.filter(Music.music_genres.any(MusicGenre.genre.in_(genres)))
    if text:
        text = text.strip()
        query = query.filter(
            Music.title.ilike(f'%{text}%')
            | Music.title_kana.ilike(f'%{text}%')
            | Music.artist.ilike(f'%{text}%')
        )
    if artist:
        query = query.filter(Music.artist == artist)
    # query = db.session.query(Music).filter(Music.id.in_(x.music_id for x in query))
    query = query.order_by(Music.id.desc())
    query = query.distinct()
    pager = db.paginate(query, page)
    return templates.render(
        'maimai_musics.html', req,
        pager=pager, genres=Genres,
        search=dict(genre=genre, text=text, artist=artist),
    )


@router.get('/musics/{music_id}')
async def maimai_music(music_id: int, req: Request,):
    music = db.session.get(Music, music_id)
    return templates.render('maimai_music.html', req, music=music)