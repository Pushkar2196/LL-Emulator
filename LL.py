import re
def table(G,ter,non_ter,start=0):  # for creating parse table.
    PPT=[] # ppt is values inside parsing table.
    First=first(G,ter,non_ter)
    Follow=follow(G,ter,non_ter,start)
    inpt=ter[:]
    inpt.append('$')
    def closure(l,r):
        if r=="^":
            return Follow[l]
        elif r[0] in non_ter:
            c=First[r[0]]
            if "^" in c:
                c.remove("^")
                c.extend(Follow[l])
                c=list(set(c))
            return c
        else:
            return r[0]
    for i in range(len(non_ter)):
        PPT.append(["error"]*len(inpt))
    con=False
    for i in non_ter:
        m=non_ter.index(i)
        for j in G[i]:
            clos=closure(i,j)
            for k in clos:
                    n=inpt.index(k)
                    if PPT[m][n]=="error":
                        PPT[m][n]=list((i,j))
                    else:
                        PPT[m][n].extend(list((i,j)))
                        con=True
    return PPT,con,inpt


def first(g,term,nterm):
    Firstset={} # hashmap of all first
    def First(x):
        p=g[x] # p is value of g[] hashmap
        fi=[] # fi is list
        for q in p:
            if q[0] in term or q[0]=="^": # as whenever we're finding a terminal or ^(epsilon), add it in first (fi list)
                fi.extend(q[0])
            else:
                for i in q:
                    if i in term:
                        break
                    else:
                        m=Firstset.get(i,"not found")
                        if m!="not found":
                            fi.extend(m)
                            if "^" not in m:
                                break
                        else:
                            u=First(i)
                            fi.extend(u)
                            if "^" not in u:
                                break
        t1=set(fi)
        Firstset[x]=list(t1)
        return fi
    for nt in nterm:  # intially First(x) is not executed as not called
        if nt not in Firstset: # firstset is hashmap
            First(nt)
    return Firstset


def follow(g,term,nterm,strt=0):
    Followset={}
    Firstset=first(g,term,nterm)
    if strt==0:
        strt=nterm[0]
    def Follow(x):
        fo=[]
        if x==strt:
            fo.extend("$")
        for p in g:
            q=g[p]
            for n in q:
                for m in n:
                    if x==m:
                        k1=n.index(x)
                        k=k1+1
                        if k<len(n):
                            s=n[k]
                            if s in term:
                                fo.extend(s)
                            else:
                                temp=Firstset[s]
                                if "^" not in temp:
                                    fo.extend(temp)
                                else:
                                    temp.remove("^")
                                    fo.extend(temp)
                                    v=Followset.get(p,"not found")
                                    if v!="not found":
                                        fo.extend(v)
                        else:
                            v=Followset.get(p,"not found")
                            if v!="not found":
                                fo.extend(v)
        t1=set(fo)
        Followset[x]=list(t1)
        return fo
    for nt in nterm:
            Follow(nt)
    return Followset
