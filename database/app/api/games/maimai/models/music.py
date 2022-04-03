import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from .difficulty import maimaiDifficulties, maimaiDifficulty


class maimaiGenres(enum.Enum):
    Pops_Anime = 1
    Niconico_Vocaloid = 2
    Touhou = 4
    SEGA = 8
    Games_Variety = 16
    Original_Joypolis = 32
    #Utage = 32

    @classmethod
    def from_mask(cls, mask):
        return [
            x
            for x in cls
            if x.value & mask or x.value == mask
        ]

    @classmethod
    def from_name(cls, s: str):
        for x in cls:
            if cls.stringify(x.name) == s:
                return x
        raise KeyError(s)

    @staticmethod
    def stringify(s: str):
        return s.replace('_', ' ')

    def __str__(self):
        return self.stringify(self.name)


class maimaiMusicGenre(db.IdMixin, db.Base):
    music_id = sa.Column(sa.ForeignKey('maimai_musics.id'))
    genre = sa.Column(sa.Enum(maimaiGenres))

    music = orm.relationship('maimaiMusic', back_populates='music_genres')


class maimaiMusic(db.BpmMixin, db.Base):
    id = sa.Column(sa.Integer, primary_key=True)
    label = sa.Column(sa.String, unique=True)
    title = sa.Column(sa.String)
    title_kana = sa.Column(sa.String)
    artist = sa.Column(sa.String)
    #release = sa.Column(sa.Integer)
    image_url = sa.Column(sa.String)

    difficulties = orm.relationship('maimaiDifficulty', order_by=maimaiDifficulty.level, cascade="all, delete-orphan")
    music_genres = orm.relationship('maimaiMusicGenre', order_by=maimaiMusicGenre.genre, cascade="all, delete-orphan")

    def __init__(self, genre_mask=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if genre_mask:
            self.music_genres = [
                maimaiMusicGenre(music=self, genre=genre)
                for genre in maimaiGenres.from_mask(genre_mask)
            ]

    def __str__(self):
        return f'{self.artist} - {self.title}'

    @property
    def folder(self):
        return f'{str(self.id).zfill(4)}_{self.ascii}'

    @property
    def genres(self):
        return [x.genre for x in self.music_genres]
