from os import listdir
from os import path
from os import remove

import ast
import sqlite3
from fastapi import FastAPI, Response

from getdata_funcs import getlines_f #gets the line on which function is defined
from getdata_funcs import getlines_c #gets the line on which class is defined
from getdata_funcs import getlines_cf 
from getdata_funcs import onefunc_1

from sqlite_funcs import opendbase #creates empty database 
from sqlite_funcs import insertdata #inserts a row in a table
from sqlite_funcs import putfuncs_inallwk


if path.isfile('filesdata.db'):  #does this in case you run this file again
    remove('filesdata.db')       #just in case you added more files into files folder
    print("previous version removed")
    
opendbase('filesdata.db')




##################### PART A ###############
file_id5000=0
for filename1 in  listdir("ARCHIVE_PYFILES"):
    file_id5000+=1
    if filename1 == "__pycache__" : continue #just in case you ran those py files
    print ("\t\""+filename1+"\"")
    f = open("ARCHIVE_PYFILES\\"+filename1)
    filename = filename1[:-3]
    FILEdata = []
    FILEdata.append(file_id5000)
    FILEdata.append(filename)
    node = ast.parse(f.read())


    functions=[]
    classes=[]
    class_functions=[]

    for n in node.body: #<-- this whole loop gets all functions and classes
        functions.append(onefunc_1(n, ast.FunctionDef, file_id5000))
        classes.append(onefunc_1(n, ast.ClassDef, file_id5000))
        if isinstance(n, ast.ClassDef):
            for new in n.body:
                class_functions.append(onefunc_1(new, ast.FunctionDef, file_id5000))
                if class_functions[-1]!=[]:
                    class_functions[-1][2] =  n.name + "." +class_functions[-1][2]
   
    f.close()
    f = open("ARCHIVE_PYFILES\\"+filename1) #close and open again because already reached EOF
    
    i=0
    fnames=[]
    cnames=[]
    cfnames=[]
    lns = f.readlines()
    amnt = len(lns)
    for line in lns: #<-- in this loop we get lines on which funcs/classes are defined
        i+=1
        getlines_f(functions, line, i, fnames) 
        getlines_c(classes, line, i, cnames)

    i=0
    for line in lns: #we do this loop separately because it needs full data from cnames
        i+=1
        getlines_cf(class_functions, line, i, classes,cfnames, lns)
    f.close()

    while [] in functions: # in these we remove empty entries
        functions.remove([])
    while [] in classes:
        classes.remove([])
    while [] in class_functions:
        class_functions.remove([])
        

    # after this line we put all data of this file into the database
    FILEdata.append(len(functions)+len(class_functions))
    FILEdata.append(len(classes))
    insertdata('filesdata.db', 'py_files', FILEdata)

    
    for fun in functions:
        insertdata('filesdata.db', 'functions', fun)
    for clfunc in class_functions:
        insertdata('filesdata.db', 'functions', clfunc)
    for clss in classes:
        insertdata('filesdata.db', 'classes', clss)
       




##################### PART B ###############




app= FastAPI()




@app.get("/api/files")
def output_py_files():
    files=[]
    connection = sqlite3.connect('filesdata.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM py_files")
    py_files = cursor.fetchall()
    if py_files==[]: return files #if we dont have any files there
    connection.close()
 
    for i in range(len(py_files)):
        files.append({"file": py_files[i][0], "name": py_files[i][1], "functions": py_files[i][2], "classes":py_files[i][3] } )
    return files






@app.get("/api/files/{name}/structure")
def structure(name):
    data_f =[]
    
    connection = sqlite3.connect('filesdata.db')
    cursor = connection.cursor()
    cursor.execute('SELECT file_id FROM py_files WHERE filename = ?', [name])
    c = cursor.fetchall()
    if c == []: return data_f #if we cant find the file we return []
    
    newid = int(str(c[0])[1:-2])
    cursor.execute('SELECT * FROM functions WHERE file_id = ?', [newid])
    funcs = cursor.fetchall()
    cursor.execute('SELECT * FROM classes WHERE file_id = ?', [newid])
    clss=cursor.fetchall()
    connection.close()
    
    for i in range(len(funcs)):
        data_f.append({"type" : "function", "name": funcs[i][2], "defined on line": funcs[i][1], "docstring": funcs[i][3] } )
    for i in range(len(clss)):
        data_f.append({"type" : "class", "name": clss[i][2], "defined on line": clss[i][1], "docstring": clss[i][3] } )
    data_f.sort(key=lambda x: x["defined on line"])
    
    return data_f







@app.get("/api/search")
def find_all_w_keyword(q: str="", type: str=""):
    if ((q=="") and (type=="")): return {"message":"no variables inputted"}

    if q!="":
        allwk, fff, ccc=[], [], [] #allwk is an array of properly formatted data that we return
        connection = sqlite3.connect('filesdata.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM functions')
        fnames=cursor.fetchall()
        cursor.execute('SELECT * FROM classes')
        cnames=cursor.fetchall()
        #fnames and cnames hold arrays functions and classes
        #fff and  only hold functions that have q in their name or desc !!
        
        if cnames==[] and fnames==[]: return allwk #in case we dont have any files
        if not (fnames==[]):
            for i in fnames: #here we check if q is in name or desc
                if i==[]: continue
                if q.lower() in i[2].lower() or q.lower() in i[3].lower():
                    fff.append(i)
        if not (cnames==[]):
            for i in cnames:
                if i==[]: continue
                if q.lower() in i[2].lower() or q.lower() in i[3].lower():
                    ccc.append(i)
        if fff==[] and ccc==[]:return allwk
        
        putfuncs_inallwk(allwk,fnames, fff, 1) # this function finds rows with the names and adds to allwk
        putfuncs_inallwk(allwk, fnames,fff, 1)
        putfuncs_inallwk(allwk,cnames, ccc, 0)

        allwk.sort(key=lambda x: x["defined on line"]) #sorts by order of definition 
        

        #this here checks if we also have a type variable
        if type=="": return allwk
        if (type).lower()=="function":
            allwk = [d for d in allwk if d.get("type")=="function"]
        elif (type).lower()=="class":
            allwk = [d for d in allwk if d.get("type")==(type).lower()]
            return allwk
        else: return {"message":"wrong type"}


    # this route is if we only check by type
    else:
        allwk, fids =[], [] # fids keeps only file ids
        connection = sqlite3.connect('filesdata.db')
        cursor = connection.cursor()
        if type=="function":
            cursor.execute('SELECT * FROM functions')
        elif type=="class":
            cursor.execute('SELECT * FROM classes')
        else: return [] #if type is incorrect we return []
        nnames=cursor.fetchall()  #holds either all classes or all funcs
        if nnames==[]: return {"some sort of weird error":"beh"}

        for fucl in nnames:
            if not (fucl[0] in fids): fids.append(fucl[0])  # here we get ids of all file ids we need
         
        for f_id in fids: #f_id is just ONE id from an array of ids
            cursor.execute('SELECT filename FROM py_files WHERE file_id=?', [f_id])
            filename = cursor.fetchone()[0]
            for fc in nnames:
                if fc[0] == f_id:  #if  the function/class is from this file: add it to allwk
                    allwk.append({"from file:": filename, "type" : type, "name": fc[2], "defined on line": fc[1], "docstring": fc[3] })
        allwk.sort(key=lambda x: x["defined on line"])
    connection.close()        
    return allwk
            

@app.get("api/filescount")
def countfiles():
    connection = sqlite3.connect('filesdata.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM py_files')
    py_files = cursor.fetchall()
    connection.close()
    return {"number of files in ARCHIVE_PYFILES FOLDER": len(py_files)}
    









        
        
    
