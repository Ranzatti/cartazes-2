import psycopg2

conn = psycopg2.connect(
    # dbname='ranzatti',
    # user='ranzatti',
    # password='a',
    # host='localhost'

    dbname='postgres',
    user='postgres.kngdhvmwmbcnrcutuuqm',
    password='11711FIS237',
    host='aws-0-sa-east-1.pooler.supabase.com'

    #dbname='snrmyrdk',
    #user='snrmyrdk',
    #password='WdWoPvt6qtVm9uq8V93rSYGKkf3WW-nt',
    #host='tuffi.db.elephantsql.com'
)