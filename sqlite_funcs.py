import sqlite3
# some of these functions are explained in the main file

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
    name TEXT,
    desc TEXT,
    FOREIGN KEY (file_id) REFERENCES py_files (file_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes(
    file_id INTEGER,
    line INTEGER,
    name TEXT,
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
    l = 'INSERT INTO '+tabname+' VALUES('
    for i in range (len(data)):
        l+='?'
        if i<(len(data)-1):
            l+=', '
        else:
            l+=')'
    cursor.execute(l, data)
    connection.commit()
    connection.close()



def putfuncs_inallwk(allwk, fnames, fff, flag):
    connection = sqlite3.connect('filesdata.db')
    cursor = connection.cursor()
    if not (fff==[]):
        for func in fff:
            cursor.execute('SELECT filename FROM py_files WHERE file_id=?', [func[0]])
            fi = cursor.fetchone()
            t = "function"
            if flag==0: t = "class"
            s = {"from file:": fi[0], "type" : t, "name": func[2], "defined on line": func[1], "docstring": func[3] }
            if not (s in allwk): allwk.append(s)
    connection.close()
    







    


