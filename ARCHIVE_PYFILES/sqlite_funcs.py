import sqlite3


def opendbase(dbname):
    """ creates a database with tables: py_files, functions, classes"""
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS py_files(
    file_id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    funct_count INTEGER,
    class_count INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS functions(
    file_id INTEGER,
    line INTEGER,
    name TEXT PRIMARY KEY,
    desc TEXT,
    FOREIGN KEY (file_id) REFERENCES py_files (file_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes(
    file_id INTEGER,
    line INTEGER,
    name TEXT PRIMARY KEY,
    desc TEXT,
    FOREIGN KEY (file_id) REFERENCES py_files (file_id)
    )
    ''')
    
    cursor.execute('CREATE INDEX idx_file_id ON py_files(file_id)')
    cursor.execute('CREATE INDEX idx_name ON functions(name)')
    connection.commit()
    connection.close()



def insertdata( dbname, tabname, data):
    """inserts data into a line in tabname table"""
    if data==[]: return
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    l = 'INSERT INTO '+tabname+' VALUES(null, '
    for i in range (len(data)):
        l+='?'
        if i<(len(data)-1):
            l+=', '
        else:
            l+=')'
    cursor.execute(l, data)
    connection.commit()
    connection.close()

def updateid(dbname, tabname, filename, name):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute('SELECT file_id FROM py_files WHERE filename = ?', [filename])
    newid = int(str(cursor.fetchall()[0])[1:-2])
    cursor.execute('UPDATE ' +tabname+' SET file_id = ? WHERE name = ?', [newid, name])
    connection.commit()
    connection.close()









    


