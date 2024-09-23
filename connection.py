import psycopg2

conn = psycopg2.connect(
    dbname='ranzatti',
    user='ranzatti',
    password='a',
    host='localhost'

    #dbname='snrmyrdk',
    #user='snrmyrdk',
    #password='WdWoPvt6qtVm9uq8V93rSYGKkf3WW-nt',
    #host='tuffi.db.elephantsql.com'
)