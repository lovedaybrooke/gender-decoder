from sqlalchemy import *
from migrate import *
import datetime


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
job_ad = Table('job_ad', pre_meta,
    Column('hash', VARCHAR, primary_key=True, nullable=False),
    Column('date', TIMESTAMP),
    Column('jobAdText', TEXT),
    Column('masculine_word_count', INTEGER),
    Column('feminine_word_count', INTEGER),
    Column('coding', VARCHAR),
    Column('masculine_coded_words', TEXT),
    Column('feminine_coded_words', TEXT),
)

job_ad = Table('job_ad', post_meta,
    Column('hash', String, primary_key=True, nullable=False),
    Column('date', DateTime, default=ColumnDefault(datetime.datetime.utcnow)),
    Column('ad_text', Text),
    Column('masculine_word_count', Integer, default=ColumnDefault(0)),
    Column('feminine_word_count', Integer, default=ColumnDefault(0)),
    Column('masculine_coded_words', Text),
    Column('feminine_coded_words', Text),
    Column('coding', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['job_ad'].columns['jobAdText'].drop()
    post_meta.tables['job_ad'].columns['ad_text'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['job_ad'].columns['jobAdText'].create()
    post_meta.tables['job_ad'].columns['ad_text'].drop()
