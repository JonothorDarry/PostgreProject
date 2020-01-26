import sqlalchemy as sqla
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, sql
import psycopg2
import re

def changer(x, s1, s2):
    if (x in s1):
        return s2
    return x

def parser(table, opera, ins=None, wher=None):
    
    exc=""
    if (opera=='insert'):
        ins1str=str([x for x in ins.keys()])[1:-1]
        ins2str=str([x for x in ins.values()])[1:-1]
        ins1str="".join([changer(x, "'\"", "") for x in ins1str])
        ins2str="".join([changer(x, '"', "'") for x in ins2str]) 
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


def interactor(engine, query):
    e=1
    comm=""
    try:
        engine.execute(query)
    except BaseException as ex:
        comm=ex.args[0][re.search(' ', ex.args[0]).span()[1]:re.search('\n', ex.args[0]).span()[0]]
        if (re.match('value too long', comm)):
            comm="You cannot use names longer than 50 characters!"        
        if (re.match('duplicate', comm)):
            if (re.search('player_pkey', comm)):
                comm="Player already inserted!"
            if (re.search('pk_castle_on_map', comm)):
                comm="Castle already exists on that point!"
            if (re.search('pk_build_in_castle_on_map', comm)):
                comm="This building is already created in that castle!"
            if (re.search('pk_army_connect', comm)):
                comm="This army already has some unit on that position!"
            if (re.search('hero_pkey', comm)):
                comm="This hero name is already used!"
        
        if (re.search("violates foreign key", comm)):
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
        
        if (re.search("violates not-null constraint", comm)):
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
    return(e, comm)


#hardcoded:postgres passwd host dbname
engine = create_engine('postgresql+psycopg2://postgres:dayne@localhost:54320/postgres', echo = True)

#x=parser("player", "insert", {"color":"purpleindicularpenissusmaximusvulpusssiusBanusIncultosMallusMallocusClangosCythonus"}, {})
x=parser("hero", "insert", {"name":"Jonasz", "id_army":25})
s=interactor(engine, x)

print(s)
x=parser("hero", "insert", {"color":"red", "name":"Goldenberginho", "id_army":2})
s=interactor(engine, x)

print(s)
x=parser("army", "insert", {"x":127, "y":141, "hero_name":"Goldenberginho"})
s=interactor(engine, x)

print(s)























#x=parser("army", "insert", {"x":12, "y":13}, {})
#s=interactor(engine, x)

#print(parser("castle", "insert", {"dead":12, "alive":"perhaps"}, {}))
#print(parser("castle", "update", {"dead":12, "alive":"perhaps"}, {"slain":20, "Pure":"Streetcleaner"}))
#print(parser("castle", "delete", {}, {"slain":20, "Pure":"Streetcleaner"}))

"""
meta = MetaData()
students = Table(
   'students', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('lastname', String),
)

meta.create_all(engine)
"""
"""
#engine.execute(students.insert(), name='Ozjasz', lastname='Goldberg')
#engine.execute("insert into students(name, lastname) values({}, {})".format("'Jonasz'", "'Prorok'"))
#engine.execute("delete from students where name={}".format("'Ozjasz'"))
try:
    engine.execute("insert into army(x, y) values (11, 12)")
    engine.execute("insert into army(x, y) values (11, 12)")
except sqla.exc.StatementError as e:
    print(e.args[0])

try:
    engine.execute("insert into army(x, y) values (100012, 12)")
    engine.execute("insert into army(x, y) values (11, 12)")
except sqla.exc.StatementError as e:
    print(e.args[0])
"""


