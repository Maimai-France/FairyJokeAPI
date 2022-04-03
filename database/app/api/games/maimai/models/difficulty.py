import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db

"""
At most 6 levels of difficulties for any music in maimai, going from easy to Utage.
Usually, a song always has the 5 first ones. Re:Master & Utage are not always present.
EXCLUDING UTAGE FOR NOW, THEY ARE WEIRDLY SHAPED IN THE DB
"""

class maimaiDifficulties(enum.Enum):
    EASY = 'EASY'
    BASIC = 'BASIC'
    ADVANCED = 'ADVANCED'
    EXPERT = 'EXPERT'
    MASTER = 'MASTER'
    REMASTER = 'Re:MASTER'

    def __int__(self):
        return {
            self.EASY: 1,
            self.BASIC: 2,
            self.ADVANCED: 3,
            self.EXPERT: 4,
            self.MASTER: 5,
            self.REMASTER: 6,
        }.get(self, 0)

    def __str__(self):
        return self.name


class maimaiDifficulty(db.IdMixin, db.Base):
    music_id = sa.Column(sa.ForeignKey('maimai_musics.id'))
    # Level in string as there are tracks rated with a + (e.g. 10+, 11+...)
    diff = sa.Column(sa.Enum(maimaiDifficulties))
    level = sa.Column(sa.String)

    music = orm.relationship('maimaiMusic', back_populates='difficulties')

    def __str__(self):
        return f'{self.music} [{self.name}]'

    @property
    def name(self):
        return f'{self.diff} {self.level}'

    @property
    def full(self):
        return f'{self.diff.value} {self.level}'

    @property
    def games(self):
        return {x.batch.version.game for x in self.imports}

    imports = orm.relationship('maimaiDifficultyImport')


class maimaiDifficultyImport(db.ImportMixin, db.Base):
    difficulty_id = sa.Column(sa.ForeignKey('maimai_difficulties.id'))

    difficulty = orm.relationship('maimaiDifficulty', back_populates='imports')
