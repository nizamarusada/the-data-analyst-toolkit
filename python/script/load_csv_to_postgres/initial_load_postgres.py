#package
import psycopg2
import csv
import os
import datetime
import sys

#variable
DB_NAME             = 'personal_dump'
DB_USER             = 'root'
DB_HOST             = 'localhost'
DB_PORT             = '5435'
DB_PASS             = 'root'

#command
def path(type):
    if list(type) == list('file_path') :
        SRC_DOC = SRC_ARG
        SRC_LOC = os.path.join('/home/nizam/Downloads/git','the-data-analyst-toolkit', 'data_external', 'data_from_chevy', SRC_DOC )
    if list(type) == list('sql_path') :
        SRC_SQL = SRC_ARG
        SRC_LOC = os.path.join('/home/nizam/Downloads/git','the-data-analyst-toolkit', 'sql','initial_load', 'data_from_chevy', SRC_SQL )
    return SRC_LOC

def db_connection():
    return psycopg2.connect("dbname={} user={} password={} host={} port={}".format(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT))

def db_execution(job_type, file_name, table_name):
    con = db_connection()
    cur = con.cursor()
    if list(job_type) == list('ingestion') and file_name is not None and table_name is not None:
        DB_QUERY_CP = """TRUNCATE TABLE {};""".format(table_name)
        cur.execute(DB_QUERY_CP)
        DB_QUERY_CP  = "COPY {} FROM stdin DELIMITER \',\' CSV;".format(table_name)
        cur.copy_expert(DB_QUERY_CP,open(path(file_name)))
        print('{} [INFO] Data inserted into table {}'.format(time_flag(), table_name))
    if list(job_type) == list('create_table') and file_name is not None and table_name is not None:
        sql_file = open(path(file_name), 'r')
        cur.execute(sql_file.read())
        print('{} [INFO] Table {} created on database {}'.format(time_flag(), table_name, DB_NAME))
    if list(job_type) == list('validation') and file_name is None and table_name is not None:
        DB_QUERY_VAL = 'SELECT COUNT(*) FROM {};'.format(table_name)
        cur.execute(DB_QUERY_VAL)
        check_targets = cur.fetchone()
        return check_targets[0]
    cur.close()
    con.commit()
    con.close()
    return None

def check_source(file_name):
    with open(path(file_name), 'r') as f:
        data = f.readlines()
        lines = len(data)
    return lines

def validation_target(y,z,a):
    if y==z:
        return print('{} [INFO] Data between {} are same'.format(time_flag(), a))
    else:
        return print('{} [WARN] Data between {} are diferent'.format(time_flag(), a))
    return None

def time_flag():
    EX_TIME = datetime.datetime.now().replace(microsecond=0).isoformat(' ')
    return EX_TIME

def initial_ingestion():
    BFR_SRC                 = check_source('file_path')
    db_execution('ingestion', 'file_path', DB_INITIAL_TABLE)
    AFT_TRG                 = db_execution('validation', None, DB_INITIAL_TABLE)
    validation_target(AFT_TRG,BFR_SRC,'source-temporary')
    return None

def create_table():
    db_execution('create_table', 'sql_path', DB_INITIAL_TABLE)
    return None

def main(method):
    print('{} [INFO] Job start!'.format(time_flag()))
    if list(method) == list('initial_ingestion'):
        if check_source('file_path') != 0:
            initial_ingestion()
        else:
            print('{} [ERROR] SOURCE HASN\'T DATA'.format(time_flag()))
    if list(method) == list('create_table'):
        create_table()
    return print('{} [INFO] Job finish!'.format(time_flag()))

if __name__ == '__main__':
    help_me = '''
      How to run:
        run with methods version:
            python initial_load_postgres.py "create_table|initial_ingestion" "TechCrunchcontinentalUSA.csv" "tech_crunch_continental_usa"
            python initial_load_postgres.py "initial_ingestion" "TechCrunchcontinentalUSA.csv" "tech_crunch_continental_usa"
            python initial_load_postgres.py "create_table" "tech_crunch_continental_usa.sql" "tech_crunch_continental_usa"
      '''

    arg     = sys.argv[1:]
    if len(arg) > 0:
        method = arg[0]
        DB_INITIAL_TABLE = arg[2]
        SRC_ARG =arg[1]
    else:
        print (help_me)
    main(method)
