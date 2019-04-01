from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

### Declare user table
Base = declarative_base()

_engine = create_engine('postgresql://test:test@localhost:5433/test', echo=True)
metadata = MetaData(_engine)

def _get_session(target_engine):
  return scoped_session(
    sessionmaker(
      autocommit=False,
      autoflush=False,
      bind=target_engine,
      expire_on_commit=False)
  )

session = _get_session(_engine)

def try_create_table(table_name):
  if not _engine.dialect.has_table(_engine, 'users'):
    metadata.create_all()

