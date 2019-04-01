"""Show different query styles and how to batch fetch from database
"""
from sqlalchemy import Column, Integer, String

import db_core


class User(db_core.Base):
  __tablename__ = 'users'
  metadata = db_core.metadata
  id = Column(Integer, primary_key=True)
  name = Column(String)


def populate_users():
  # Populate user table
  num_rows = 10
  print('***')
  print('***')
  print(f'== adding {num_rows} rows ==')
  print('***')
  print('***')
  for i in range(0, num_rows):
    name = f'john_{i}'
    u = User(name=name)
    print(u)
    db_core.session.add(u) 
  
  db_core.session.commit()


def query_users():
  print('***')
  print('***')
  print('== normal query ==')
  print('***')
  print('***')
  q = db_core.session.query(User)
  names = {}
  for user_row in q:
    names[user_row.name] = 1
  print(f'names counted: {len(names.keys())}')


def query_users_yield_per():
  print('***')
  print('***')
  print('== yield_per query ==')
  print('***')
  print('***')
  q = db_core.session.query(User).yield_per(2).enable_eagerloads(False)
  names = {}
  for user_row in q:
    names[user_row.name] = 1
  print(f'names counted: {len(names.keys())}')


def query_users_batch():
  print('***')
  print('***')
  print('== batch query ==')
  print('***')
  print('***')
  names = {}
  batch_size = 2
  min_id_row = _batch_query(0, batch_size).first()
  min_id = min_id_row.id

  rows = _batch_query(min_id, batch_size).all()

  while len(rows) > 0:
    print(f'got rows: {len(rows)}')
    for user_row in rows:
      names[user_row.name] = 1
    min_id += len(rows)

    rows = _batch_query(min_id, batch_size).all()
  print(f'names counted: {len(names.keys())}')


def _batch_query(min_id, b_size):
  q = db_core.session.query(User)
  q = q.filter(User.id >= min_id)
  q = q.order_by(User.id.asc())
  q = q.limit(b_size)
  return q


if __name__ == '__main__':
  db_core.try_create_table('users')
  db_core.session.execute('''TRUNCATE TABLE users''')

  populate_users()
  query_users()
  query_users_yield_per()
  query_users_batch()

  db_core.session.execute('''TRUNCATE TABLE users''')
