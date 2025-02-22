from sqlalchemy import create_engine, MetaData
from decouple import config

engine = create_engine(config("DATABASE_URI"))

metadata = MetaData(schema="elcaffetal")

conn = engine.connect()
