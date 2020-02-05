import sqlalchemy as sqla
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, sql
import psycopg2
import re

def schanger(x, s1, s2):
    if (x in s1):
        return s2
    return x

def parser(table, opera, ins=None, wher=None): 
    exc=""
    if (opera=='insert'):
        ins1str=str([x for x in ins.keys()])[1:-1]
        ins2str=str([x for x in ins.values()])[1:-1]
        ins1str="".join([schanger(x, "'\"", "") for x in ins1str])
        ins2str="".join([schanger(x, '"', "'") for x in ins2str]) 
        exc=opera+" into "+table+" ("+ins1str+")"+" values ("+ins2str+")"
    
    elif (opera=='update'):
        exc=opera+" "+table+" set " 
        c=len(ins.items())
        for i, a in enumerate(ins.items()):
            x, y=a

            if (str(y)==y):
                exc=exc+x+"='"+y+"'"
            else:
                exc=exc+x+"="+str(y)
            if (c-1!=i):
                exc=exc+","
            exc=exc+" "
        
    elif (opera=='delete'):
        exc=opera+" from "+table+" "

    if (opera=="update" or opera=="delete"):
        c=len(wher.items())
        if (wher!=None and len(wher)>0):
            exc=exc+"where "
        for i, a in enumerate(wher.items()):
            x, y=a

            if (str(y)==y):
                exc=exc+x+"='"+y+"'"
            else:
                exc=exc+x+"="+str(y)
            if (c-1!=i):
                exc=exc+" and "

    return exc+";"




def interactor(engine, query, tp=None, arg=[]):
    _Dict_prime={
            'player_pkey':"Player already inserted!",
            'pk_castle_on_map':"Castle already exists on that point!",
            'pk_build_in_castle_on_map':"This building is already created in that castle!",
            'pk_army_connect':"This army already has some unit on that position!",
            'hero_pkey':"This hero name is already used!",
            'pk_point':"This point already exists!",
    }


    e=1
    comm=""
    connection = engine.raw_connection()
    cursor = connection.cursor()
    try:
        if (tp==None):
            cursor.execute(query)

        elif (tp=='proc'):
            cursor.callproc(*arg)

        cursor.close()
        connection.commit()
    except BaseException as ex:
        comm=ex.args[0][re.search(' ', ex.args[0]).span()[1]:re.search('\n', ex.args[0]).span()[0]]

        if (re.match('too long for type', comm)):
            comm="You cannot use names longer than 50 characters!"   
        if (re.search('unique', comm)):
            for x in _Dict_prime.keys():
                if (re.search(x, comm)):
                    comm=_Dict_prime[x]
                    break
        
        elif (re.search("violates foreign key", comm)):
            if (re.search('fk_playh', comm)):
                comm="Player doesn't exist!"
            
            if (re.search('fk_armyxy', comm)):
                comm="You tried to place army on non-existent point of map!"
            if (re.search('fk_tohero', comm)):
                comm="This hero doesn't exist!" 
            if (re.search('fk_toarmy', comm)):
                comm="This army doesn't exist!"

            if (re.search('fk_armycon', comm)):
                comm="This army doesn't exist!"
            if (re.search('fk_unit_from_army', comm)):
                comm="This unit doesn't exist"

            if (re.search('fk_castle_map_point', comm)):
                comm="You tried to place castle on non-existent point of map!" 
            if (re.search('fk_castle_merge', comm)):
                comm="You tried to create castle of non-existent type!"
            if (re.search('fk_to_player', comm)):
                comm="Player does not exist!"

            if (re.search('fk_castle_build_map', comm)):
                comm="This type of building doesn't exist for that castle!"
            if (re.search('fk_xy_place', comm)):
                comm="You tried to attach building on non-existent point on map!"
        
        elif (re.search("violates not-null constraint", comm)):
            if (re.search("id_army", comm)):
                comm="You must fill army id field!!"
            if (re.search("color", comm)):
                comm="You cannot create a hero without player!"
            if (re.search('"x"', comm) or re.search('"y"', comm)):
                comm="You cannot leave empty map coordinates!"
            if (re.search("castle", comm)):
                comm="You need to provide a castle type!"
            if (re.search("unit_name", comm)):
                comm="You need to provide unit name!"


    else:
        e=0
    
    finally:
        connection.close()
    return(e, comm)



def selector(engine, table, order=None, col=None):
    g=engine.execute("SELECT * FROM information_schema.columns WHERE table_name   = '"+table+"'")
    cols=[]
    for x in g:
        cols.append(x[3])
    cols=cols[::-1]
        
    if (order==None and col==None):
        f=engine.execute(f'select {", ".join(cols)} from '+table)
    elif (order!=None):
        f=engine.execute(f'select {", ".join(cols)} from '+table+' order by '+col+' '+order)
        
    res=[]
    for x in f:
        res.append(x)
    return (res, cols)


def selhtmler(table, lst):
    sv=[]
    sv.append("<div class=\"wrapped\"><table id="+table+"><thead>")
    for x in lst[1]:
        sv.append("<th>"+x+"</th>")
    sv.append("</thead>")

    sv.append("<tbody>")
    for x in lst[0]:
        sv.append("<tr>")
        for y in x:
            sv.append("<td>"+str(y)+"</td>")
        sv.append("</tr>")
    sv.append("</tbody>")
    sv.append("</table>")
    sv.append("</div>")

    return ''.join(sv)
