import sqlalchemy as sqla
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, sql
import psycopg2
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from matplotlib.patches import Patch
import matplotlib.lines as mlines
import numpy as np
import math

def schanger(x, s1, s2):
    if (x in s1):
        return s2
    return x

#Parsowanie inserta/update'a/deleta
def parser(table, opera, ins=None, wher=None):  
    exc=""
    to_kill=[]
    if (ins!=None):
        for x, y in ins.items():
            if (len(str(y))==0):
                to_kill.append(x)
        for x in to_kill:
            ins.pop(x, None)
    
    if (wher!=None):
        to_kill=[]
        for x, y in wher.items():
            if (str(x)=="hero_name" or (table=="castle_on_map" and str(x)=='color')):
                to_kill.append(x)
        for x in to_kill:
            wher.pop(x, None)
    
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
def dictvisioner(dct, alter=1):
    dct=dict(dct)
    ancient_dict={}
    dct.pop('which', None)
    if (alter==1):
        for x in dct.keys():
            sv=x[re.search('-', x).span()[1]:]
            for v, y in zip(re.split('-', sv), re.split('-', dct[x])):
                ancient_dict[v]=y
    else:
        return dct
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
            if (len(arg[1])>0):
                pv=str(*arg[1])
                cursor.execute(f"do $$ begin call {arg[0]}('{pv}'); end $$;")
            else:
                cursor.execute(f"do $$ begin call {arg[0]}(); end $$;")


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
    #Dodanie generowanej funkcji
    if (table=='player'):
        cols.append("estimated_power")
        lst=[]
        
        for x in res:
            wn=engine.execute(f"select firepower('{x[0]}')")
            for y in wn:
                y=y[0]
                if (len(y)>10):
                    y=[int(z) for z in y[1:-1].split(',')]
                    wnn=math.log((y[0]+y[1])/2*math.sqrt(y[4])+y[5]/100+(y[2]+y[3])/2)
                else:
                    wnn=0
            #print(x[0], wn)
            lst.append([*x, wnn])

        return (lst, cols)
    return(res, cols)

#twórca tablicy z zapytania selecta(lst) i nazwy tabeli(table)
def selhtmler(table, lst):
    sv=[]
    #Button do th
    bth="""
    <div class="buth">
        <button class="sbtnd">
            v
        </button>
        <button class="sbtnu">
            v
        </button>
    </div>"""

    sv.append("<div class=\"wrapped\"><table id="+table+"><thead><tr>")
    for x in lst[1]:
        sv.append("<th>"+x+bth+"</th>")
    sv.append("</tr></thead>")

    sv.append("<tbody>")
    for x in lst[0]:
        sv.append("<tr>")
        for y in x:
            sv.append(f"<td>{y}</td>")
        sv.append("</tr>")
    sv.append("</tbody>")
    sv.append("</table>")
    sv.append("</div>")

    return ''.join(sv)

#Wyrysowanie 2 grup dla 1 koloru - armii i zamków
def doubleprinter(ax, l1, l2, coll):
    if (len(l1)>0):
        ax.scatter(l1[0], l1[1], color=coll, s=100, marker='P')
    if (len(l2)>0):
        ax.scatter(l2[0], l2[1], color=coll, s=100)


#Colorland to zbiór kolorów dla konkretnych graczy
colorland={}
#Twórca mapy dla jakiejś osi
def map_maker(engine, ax):
    #Poszukiwanie rzeczy w DB
    csel=engine.execute('select x, y, color from castle_on_map')
    csel2=engine.execute('select a.x, a.y, h.color from army a left join hero h on a.hero_name=h.name')
    xm=engine.execute('select max(x), max(y) from point_on_map')
    conn=1
    
    #Ustalanie wymiaru mapy
    for k in xm:
        xmax, ymax=k[0], k[1]
    ax.set_xlim(0, conn*xmax)
    ax.set_ylim(0, ymax)
    
    #Zamek, armie - dicty z 2 listami i nazwami graczy jako klucze, wypełnianie punktami
    hlegs=[]
    castel={}
    here={}

    for w in csel:
        try:
            castel[w[2]].append((w[0], w[1]))
        except:
            castel[w[2]]=[(w[0], w[1])]

    for w in csel2:
        try:
            here[w[2]].append((w[0], w[1]))
        except:
            here[w[2]]=[(w[0], w[1])]
        if (not w[2] in castel):
            castel[w[2]]=[]

    for x, y in castel.items():
        #Poszukiwanie x-koloru, y-zamka, z-armia
        if (not x in here.keys()):
            here[x]=[]
        z=here[x]

        lst=list(zip(*y))
        lst2=list(zip(*z))
        

        try:
            doubleprinter(ax, lst, lst2, colorland[x])
            
        except:
            if (x==None):
                clr='Grey'
            else:
                clr=str(x).lower()
            try:
                doubleprinter(ax, lst, lst2, clr)
                vs=clr
            except:
                vs=np.random.uniform(0, 1, 3)
                doubleprinter(ax, lst, lst2, vs)
            #Definiowanie nowego koloru dla usera w przypadku jego nieistnienia
            colorland[x]=vs
        finally:
            hlegs.append(Patch(facecolor=colorland[x], alpha=1.0, label=f"Player: {x}"))
    hlegs.append(mlines.Line2D([], [], color='#FFFFFF', marker='P', markerfacecolor='#000000', markersize=15, label='Castle'))
    hlegs.append(mlines.Line2D([], [], color='#FFFFFF', marker='o', markerfacecolor='#000000', markersize=15, label='Hero'))
    ax.legend(handles=hlegs, loc=1, facecolor='#FFFFFF', shadow=1.0, prop={'size': 12})
    ax.fill_between([xmax, conn*xmax], [0, 0], [ymax, ymax], color='#000000')
    
    
    ax.set_xticks(ax.get_xticks()[ax.get_xticks()<=xmax])


#Funkcja tworząca/updatująca mapę
def inserto_creato_mapo(engine, arg='n'):
    fig, ax=plt.subplots(1, 1, figsize=(24, 18))
    if (arg=='n'):
        map_maker(engine, ax)
        plt.savefig('arda.png', bbox_inches='tight')
        
    plt.close()

