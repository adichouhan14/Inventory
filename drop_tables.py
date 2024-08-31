from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Define your database URI
DATABASE_URI = 'postgresql://postgres:Admin@localhost:5432/saheb_stone' # Replace with your actual database URI

# Create an engine
engine = create_engine(DATABASE_URI)

# Create a metadata instance
metadata = MetaData()

# Reflect the current database
metadata.reflect(bind=engine)

# Drop all tables
metadata.drop_all(bind=engine)

# Optionally, you can delete sequences if your database supports them.
# For PostgreSQL, you might use:
# for sequence in engine.dialect.get_sequences(engine):
#     engine.execute(f'DROP SEQUENCE IF EXISTS {sequence["name"]} CASCADE;')

print("All tables and sequences have been deleted.")
