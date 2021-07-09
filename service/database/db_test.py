#%%
# username: postgres
# password: init1234
# host: db-test-wind.ccopuoz0ccji.ap-northeast-2.rds.amazonaws.com
# port: 5432
#%%
def connect(user, password, db, host='여기에 입력', port='여기에 입력'):
    import sqlalchemy
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    #meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con
#%%
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
#%%
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:init1234@db-test-wind.ccopuoz0ccji.ap-northeast-2.rds.amazonaws.com:5432/postgres')
# engine.execute("DROP TABLE IF EXISTS public.score;")
meta = MetaData(bind=engine)
# Session = sessionmaker()
# Session.configure(bind=engine)
meta.tables.keys()
