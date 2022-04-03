#!/usr/bin/env python3

from ast import parse
from datetime import date
from pathlib import Path
import sys
import json

sys.path.append(str(Path('.').resolve()))

from app import db
from app.models import Version, ImportBatch, Series, Game
from app.api.games.maimai.models import Difficulty, Music, MusicGenre, Genres, Difficulties, DifficultyImport

target = open(sys.argv[1])

def genre_to_mask(genre):
    if genre == 'POPS&アニメ':
        return 1
    if genre == 'niconico & ボーカロイド':
        return 2
    if genre == '東方Project':
        return 4
    if genre == 'SEGA':
        return 8
    if genre == 'ゲーム & バラエティ':
        return 16
    if genre == 'オリジナル & ジョイポリス':
        return 32
    else:
        return 1

def parse_music_db(database, batch):
    fakeid = 1
    for music in database:
        # DB is not clean, filters needed on parsing
        if 'id' in music:
            # id, title, artist (some seems to be missing !)
            music_id = fakeid
            mdata = db.create(
                Music,
                {'id': music_id},
                {
                    'label': music.get('title')+"-"+str(fakeid),
                    'title': music.get('title'),
                    'title_kana': music.get('title_kana', ''),
                    'artist': music.get('artist', ''),
                    'image_url': music.get('image_url', ''),
                    'genre_mask': genre_to_mask(music.get('category'))
                },
                commit = False,
                update = True,
            )

            # Dirty for the first prototype
            deasy = db.create(
                Difficulty,
                {
                    'music_id': music_id,
                    'diff': Difficulties('EASY'),
                },
                {
                    'level': music.get('lev_eas'),
                },
                commit=False,
                update=True,
            )
            db.add(DifficultyImport, difficulty=deasy, commit=False, batch=batch)

            dbas = db.create(
                Difficulty,
                {
                    'music_id': music_id,
                    'diff': Difficulties('BASIC'),
                },
                {
                    'level': music.get('lev_bas'),
                },
                commit=False,
                update=True,
            )
            db.add(DifficultyImport, difficulty=dbas, commit=False, batch=batch)

            dadv = db.create(
                Difficulty,
                {
                    'music_id': music_id,
                    'diff': Difficulties('ADVANCED'),
                },
                {
                    'level': music.get('lev_adv'),
                },
                commit=False,
                update=True,
            )
            db.add(DifficultyImport, difficulty=dadv, commit=False, batch=batch)

            dexp = db.create(
                Difficulty,
                {
                    'music_id': music_id,
                    'diff': Difficulties('EXPERT'),
                },
                {
                    'level': music.get('lev_exp'),
                },
                commit=False,
                update=True,
            )
            db.add(DifficultyImport, difficulty=dexp, commit=False, batch=batch)

            dmas = db.create(
                Difficulty,
                {
                    'music_id': music_id,
                    'diff': Difficulties('MASTER'),
                },
                {
                    'level': music.get('lev_mas'),
                },
                commit=False,
                update=True,
            )
            db.add(DifficultyImport, difficulty=dmas, commit=False, batch=batch)

            if 'lev_remas' in music:
                # Also include Re:MASTER
                dremas = db.create(
                    Difficulty,
                    {
                        'music_id': music_id,
                        'diff': Difficulties('Re:MASTER'),
                    },
                    {
                        'level': music.get('lev_remas'),
                    },
                    commit=False,
                    update=True,
                )
                db.add(DifficultyImport, difficulty=dremas, commit=False, batch=batch)
        fakeid += 1

if __name__ == '__main__':
    # Load with scriptname.py path_to_finale_json_db finale
    game_name = sys.argv[2]
    mdb = json.load(target)
    series = db.session.query(Series).filter_by(short='maimai').one()
    game = db.session.query(Game).filter_by(short=game_name, series=series).one()
    version = db.create(Version, name='finale', game=game)
    batch = db.add(ImportBatch, version=version, commit=False)
    parse_music_db(mdb, batch)
    db.session.commit()