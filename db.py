from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'test',
}

# Create an SQLAlchemy engine
engine = create_engine("mysql+pymysql://{user}:{password}@{host}/{db}".format(**db_config))
meta = MetaData()

# Continue with the definition of the 'users' table using Base
users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('password', String(255))
)

# Uncomment this if you need to create the table
# meta.create_all(engine)

# Create a connection to the database
conn = engine.connect()
