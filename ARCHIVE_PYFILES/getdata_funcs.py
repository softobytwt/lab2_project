import ast

def onefunc(n, astfunc):
    """adds one entry to the functions/classes array as
    [foreign key, line=0, self name, self docstring]"""
    curfunc = []
    if isinstance(n, astfunc):
        #curfunc.append(name_id)
        curfunc.append(0)
        curfunc.append((n.name))#.lower())
        newnode = n.body
        for new in newnode:
            if isinstance(new, ast.Expr):
                if isinstance(new.value, ast.Call): continue
                curfunc.append((new.value.value))#.lower())
        if len(curfunc)==2: curfunc.append('')
    return curfunc






def getlines_f(ForC, line, i, fnames):
    """finds the line number on which the function/class is defined"""
    for temp in ForC:
        if temp==[]: continue
        name = temp[1]
        if name in fnames: continue
      
        if "def "+name in line:
            temp[0] = i
            fnames.append(name)
            
def getlines_c(ForC, line, i, cnames):
    for temp in ForC:
        if temp==[]: continue
        name = temp[1]
        if name in cnames: continue
      
        if "class "+name in line:
            temp[0] = i
            cnames.append(name)
           


