import sqlalchemy as sqla
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, sql
import psycopg2
import re

def schanger(x, s1, s2):
    if (x in s1):
        return s2
    return x

#Parsowanie inserta/update'a/deleta
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

#Zamiana dicta z niepoprawnymi nazwami na sensownego dicta
def dictvisioner(dct):
    dct=dict(dct)
    ancient_dict={}
    dct.pop('which', None)
    for x in dct.keys():
        sv=x[re.search('-', x).span()[1]:]
        for v, y in zip(re.split('-', sv), re.split('-', dct[x])):
            ancient_dict[v]=y
    return ancient_dict

#Wbijacz zapytań
def interactor(engine, query, tp=None, arg=[]):
    _Dict_prime={
            'player_pkey':"Player already inserted!",
            'pk_castle_on_map':"Castle already exists on that point!",
            'pk_build_in_castle_on_map':"This building is already created in that castle!",
            'pk_army_connect':"This army already has some unit on that position!",
            'hero_pkey':"This hero name is already used!",
            'pk_point':"This point already exists!",
    }
    _Dict_foreign={
            'fk_playh':"Player doesn't exist!",
            'fk_armyxy':"You tried to place army on non-existent point of map!",
            'fk_tohero':"This hero doesn't exist!", 
            'fk_toarmy':"This army doesn't exist!",
            'fk_armycon':"This army doesn't exist!",
            'fk_unit_from_army':"This unit doesn't exist",
            'fk_castle_map_point':"You tried to place castle on non-existent point of map!" ,
            'fk_castle_merge':"You tried to create castle of non-existent type!",
            'fk_to_player':"Player does not exist!",
            'fk_castle_build_map':"This type of building doesn't exist for that castle!",
            'fk_xy_place':"You tried to attach building on non-existent point on map!",
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
        
        elif (tp=='procp'):
            pv=str(*arg[1])
            cursor.execute(f"do $$ begin call {arg[0]}('{pv}'); end $$;")


        cursor.close()
        connection.commit()
    except BaseException as ex:
        comm=ex.args[0][:re.search('\n', ex.args[0]).span()[0]]
        print(comm)

        if (re.search('too long for type character', comm)):
            comm="You cannot use names longer than 50 characters!"   
        if (re.search('unique', comm)):
            for x in _Dict_prime.keys():
                if (re.search(x, comm)):
                    comm=_Dict_prime[x]
                    break
        
        elif (re.search("violates foreign key", comm)):
            for x in _Dict_foreign.keys():
                if (re.search(x, comm)):
                    comm=_Dict_foreign[x]
                    break
        
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


#Selekcja danych 
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

#twórca tablicy z zapytania selecta(lst) i nazwy tabeli(table)
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
