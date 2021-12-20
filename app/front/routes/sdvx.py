from typing import List, Optional
from fastapi import Request, Query
from fastapi.responses import RedirectResponse

from app import Router, Schema, db
from app.api.games.sdvx.models import Apeca, Difficulty, Music, MusicGenre, Genres
from .. import templates


router = Router(__name__)


class SearchSchema(Schema):
    level: Optional[List[int]]
    genre: Optional[List[int]]
    text: Optional[str]


@router.get('/')
async def sdvx_index():
    return RedirectResponse(router.url_path_for('sdvx_musics'))


@router.get('/musics')
async def sdvx_musics(
    req: Request, page: int = 1,  *,
    level: List[int] = Query([]),
    genre: List[str] = Query([]),
    text: str = Query(''),
):
    query = db.session.query(Difficulty).join(Music)
    if level:
        query = query.filter(Difficulty.level.in_(map(int, level)))
    if genre:
        genres = [Genres[x] for x in genre]
        query = query.filter(Music.music_genres.any(MusicGenre.genre.in_(genres)))
    if text:
        query = query.filter(
            Music.title.ilike(f'%{text}%')
            | Music.artist.ilike(f'%{text}%')
            | Music.ascii.ilike(f'%{text}%')
            | Difficulty.illustrator.ilike(f'%{text}%')
            | Difficulty.effector.ilike(f'%{text}%')
        )
    query = db.session.query(Music).filter(Music.id.in_(x.music_id for x in query))
    pager = db.paginate(query, page)
    return templates.render(
        'sdvx_musics.html', req,
        pager=pager, genres=Genres,
        search=dict(level=level, genre=genre, text=text),
    )


@router.get('/musics/{music_id}')
async def sdvx_music(music_id: int, req: Request,):
    music = db.session.get(Music, music_id)
    return templates.render('sdvx_music.html', req, music=music)


@router.get('/apecas')
async def sdvx_apecas(req: Request, page: int = 1):
    query = db.session.query(Apeca)
    pager = db.paginate(query, page, 60)
    return templates.render('sdvx_apecas.html', req, pager=pager)


@router.get('/apeca/{apeca_id}')
async def sdvx_apeca(apeca_id: int, req: Request):
    apeca = db.session.get(Apeca, apeca_id)
    return templates.render('sdvx_apeca.html', req, apeca=apeca)
