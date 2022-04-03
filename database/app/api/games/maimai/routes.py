from typing import Any, Optional, List
from fastapi import HTTPException
from fastapi.responses import FileResponse, RedirectResponse

from app import db, Schema
from .. import GameSchema
from . import DATA_JACKETS, router
from .models import Music, Difficulty


class MusicSchema(Schema):
    id: int
    label: str
    title: str
    title_kana: Optional[str]
    artist: str
    image_url: str


class DifficultySchema(Schema):
    id: int
    level: str
    name: str


class GetMusicSchema(MusicSchema):
    difficulties: List[DifficultySchema]


class GetDifficultySchema(DifficultySchema):
    music: MusicSchema


@router.get('/musics/{music_id}.png')
async def maimai_get_jacket(music_id: int):
    music = await maimai_get_music(music_id)
    path = DATA_JACKETS+music.image_url
    return RedirectResponse(path)


@router.get('/musics/{music_id}', response_model=GetMusicSchema)
async def maimai_get_music(music_id: int):
    music = db.session.get(Music, music_id)
    return music


@router.get('/diff/{diff_id}', response_model=GetDifficultySchema)
async def get_maimai_diff(diff_id: int):
    diff = db.session.get(Difficulty, diff_id)
    return diff


@router.get('/musics/', response_model=List[GetMusicSchema])
async def get_maimai_musics(title: str, limit=1):
    query = db.session.query(Music).filter_by(title=title)
    query = query.limit(limit)
    return query.all()
