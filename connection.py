import psycopg2

conn = psycopg2.connect(
    dbname='socorrpm',
    user='socorrpm',
    password='SICSADM',
    host='localhost'

    #dbname='snrmyrdk',
    #user='snrmyrdk',
    #password='WdWoPvt6qtVm9uq8V93rSYGKkf3WW-nt',
    #host='tuffi.db.elephantsql.com'
)