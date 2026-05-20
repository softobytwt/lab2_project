import ast
# some of these functions are explained in the main file

def onefunc_1(n, astfunc, file_id5000):
    """adds one entry to the functions/classes array as
    [foreign key, line=0, self name, self docstring]"""
    curfunc = []
    if isinstance(n, astfunc):
        
        curfunc.append(file_id5000)
        curfunc.append(0)
        curfunc.append((n.name))#.lower())
        newnode = n.body
        for new in newnode:
            if isinstance(new, ast.Expr):
                if isinstance(new.value, ast.Call): continue
                curfunc.append((new.value.value))
        if len(curfunc)==3: curfunc.append('')
    return curfunc


def getlines_f(ForC, line, i, fnames):
    """finds the line number on which the function/class is defined"""
    for temp in ForC:
        if temp==[]: continue
        name = temp[2]
        if name in fnames: continue
        if "def "+name in line:
            temp[1] = i
            fnames.append(name)

            
def getlines_c(ForC, line, i, cnames):
    for temp in ForC:
        if temp==[]: continue
        name = temp[2]
        if name in cnames: continue
        if "class "+name in line:
            temp[1] = i
            cnames.append(name)
           
def getlines_cf(ForC, line, i, classes,cfnames, lns):
    for temp in ForC:
        if temp==[]: continue
        if temp[2] in cfnames: continue
        name = temp[2][temp[2].find(".")+1:]
        cname = temp[2][:temp[2].find(".")]
        cline = 0
        for cl in classes:
            if cl==[]: continue
            if cname==cl[2]:
                cline= cl[1]
                break
        if "def " + name in line:
            if i > cline:
                temp[1] = i
                cfnames.append(temp[2])

                
                






















   

