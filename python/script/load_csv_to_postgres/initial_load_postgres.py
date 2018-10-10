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
DB_INITIAL_TABLE    = 'tech_crunch_continental_usa'
DB_TRANSFORM_TABLE  = 'preprocessed_users'

#command
def src_file(f):
    if list(f) == list('src') :
        SRC_DOC = SRC_DOC
    if list(f) == list('prc') :
        SRC_DOC = 'dataset-medium-preprocess.csv'
    SRC_LOC = os.path.join('~/Downloads/git','the-data-analyst-toolkit', 'data_external', 'data_from_chevy', SRC_DOC )
    return SRC_LOC

def db_connection():
    return psycopg2.connect("dbname={} user={} password={} host={} port={}".format(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT))

def db_execution(a, b, c):
    con = db_connection()
    cur = con.cursor()
    if list(a) == list('ingestion') and b is not None and c is not None:
        DB_QUERY_CP = """TRUNCATE TABLE {};""".format(c)
        cur.execute(DB_QUERY_CP)
        DB_QUERY_CP  = "COPY {} FROM stdin DELIMITER \',\' CSV;".format(c)
        cur.copy_expert(DB_QUERY_CP,open(src_file(b)))
        print('{} [INFO] Data inserted into table {}'.format(time_flag(), c))
    if list(a) == list('processing') and b is None and c is None:
        DB_QUERY_PRE = """TRUNCATE TABLE {};""".format(DB_TRANSFORM_TABLE)
        cur.execute(DB_QUERY_PRE)
        DB_QUERY_PRE = """insert into {}
                        select concat(first_name,' ', last_name) as full_name, email, address, created_at from {};""".format(DB_TRANSFORM_TABLE, DB_INITIAL_TABLE)
        cur.execute(DB_QUERY_PRE)
        print('{} [INFO] Data processed into table {}'.format(time_flag(), DB_TRANSFORM_TABLE))
    if list(a) == list('validation') and b is not None and c is None:
        DB_QUERY_VAL = 'SELECT COUNT(*) FROM {};'.format(b)
        cur.execute(DB_QUERY_VAL)
        check_targets = cur.fetchone()
        return check_targets[0]
    cur.close()
    con.commit()
    con.close()
    return None

def file_preprocess():
    with open(src_file('src'), 'r') as f:
        reader = csv.reader(f)
        with open(src_file('prc'), 'w', newline='') as g:
            writer = csv.writer(g,lineterminator='\r\n',quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                new_row = [' '.join([row[0], row[1]])] + row[2:]
                writer.writerow(new_row)
    return print('{} [INFO] Data have been pre-processed!'.format(time_flag()))

def check_source(a):
    with open(src_file(a), 'r') as f:
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

def method_v1():
    BFR_SRC                 = check_source('src')
    db_execution('ingestion', 'src', DB_INITIAL_TABLE)
    AFT_TRG                 = db_execution('validation', DB_INITIAL_TABLE, None)
    validation_target(AFT_TRG,BFR_SRC,'source-temporary')
    db_execution('processing', None, None)
    AFT_TRG                 = db_execution('validation', DB_TRANSFORM_TABLE, None)
    validation_target(AFT_TRG,BFR_SRC,'temporary-target')
    return None

def method_v2():
    BFR_SRC                 = check_source('src')
    file_preprocess()
    AFT_TRG                 = check_source('prc')
    validation_target(AFT_TRG,BFR_SRC,'source-temporary')
    db_execution('ingestion', 'prc', DB_TRANSFORM_TABLE)
    AFT_TRG                 = db_execution('validation', DB_TRANSFORM_TABLE, None)
    validation_target(AFT_TRG,BFR_SRC,'temporary-target')
    return None

def method_v3():
    BFR_SRC                 = check_source('src')
    db_execution('ingestion', 'src', DB_INITIAL_TABLE)
    AFT_TRG                 = db_execution('validation', DB_INITIAL_TABLE, None)
    validation_target(AFT_TRG,BFR_SRC,'source-temporary')

def main(methods):
    print('{} [INFO] Job start!'.format(time_flag()))
    if check_source('src') != 0:
        if list(methods) == list('v1'):
            method_v1()
        if list(methods) == list('v2'):
            method_v2()
        if list(methods) == list('v3'):
            method_v3()
    else:
        print('{} [ERROR] SOURCE HASN\'T DATA'.format(time_flag()))
    return print('{} [INFO] Job finish!'.format(time_flag()))

if __name__ == '__main__':
    help_me = '''
      How to run:
        run with methods version:
            python initial_load_postgres.py "v1|v2|v3" "TechCrunchcontinentalUSA.csv" "tech_crunch_continental_usa"
            python initial_load_postgres.py "v3" "TechCrunchcontinentalUSA.csv" "tech_crunch_continental_usa"
      '''
    print (help_me)
    arg_1     = sys.argv[1:]
    if len(arg_1) > 0:
        methods = arg_1[0]
    arg_2     = sys.argv[2:]
    if len(arg_2) > 0:
        SRC_DOC = arg_2[1]
    arg_3     = sys.argv[3:]
    if len(arg_3) > 0:
        DB_INITIAL_TABLE = arg_2[2]
    main(methods)
