"""I/O operation from/to database
"""

from sqlalchemy import create_engine

from jitenshop import config


def psql_args():
    """Return the arguments for the command psql with some db parameters

    Return a list of str
    """
    psql = [
        '-h', config['database']['host'],
        '-d', config['database']['dbname'],
        '-U', config['database']['user'],
        '-p', config['database']['port']
    ]
    if (
            'password' in config['database']
            and config['database']['password'] is not None
    ):
        psql.insert(
            0, 'PGPASSWORD={pwd}'.format(pwd=config['database']['password'])
        )
    return psql


def shp2pgsql_args(projection, filename, tablename, encoding=None):
    """Return the arguments for the command shp2pgsql

    projection: str
       Projection SRID no.
    filename: str
       Shapefile
    tablename: str
       Name of the SQL table
    encoding: str (default None)

    Return a list of str
    """
    shp2pgsql = ['-cID']
    if encoding:
        shp2pgsql.extend(['-W', encoding])
    if projection:
        shp2pgsql.extend(['-s', projection])
    shp2pgsql.extend([filename, tablename])
    return shp2pgsql


def engine():
    """Return a SQLAlchemy engine with Postgres connection parameters
    """
    database = config['database']
    if database.get('password') is not None:
        url = 'postgresql://{user}:{password}@{host}/{dbname}'.format(
            user=database['user'],
            password=database['password'],
            host=database['host'],
            dbname=database['dbname']
        )
    else:
        url = 'postgresql://{user}@{host}/{dbname}'.format(
            user=database['user'],
            host=database['host'],
            dbname=database['dbname']
        )
    return create_engine(url)
