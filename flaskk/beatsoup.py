import os
from bs4 import BeautifulSoup
from alchlib import *

def openize(pather):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, pather)
    return open(filename)

def changer(html_file, tablez=None):
    soup = BeautifulSoup(html_file, 'html.parser')
    fil=openize('../apps/overall.css')
    z=fil.read()
    z="<head>\n<style>\n"+z+"\n</style>\n</head>"
    zv="<script>"
    if (tablez!=None):
        zv=zv+f"let docs = {str(tablez)};\n" 
        fil=openize('../apps/cud.js')
        zv=zv+fil.read()
    else:
        fil=openize('../apps/inserto.js')
        zv=zv+fil.read()

    zv=zv+"</script>"
    zk=BeautifulSoup(z, 'html.parser')
    zv=BeautifulSoup(zv, 'html.parser')
    
    soup.head.replace_with(zk)
    soup.body.append(zv)
    d=soup.prettify()
    return d

#Zamienia tablicę o podanym id nową tablicą - wstawianie z bazy
def supchanger(html, idd, new):
    html=BeautifulSoup(html, 'html.parser')
    new=BeautifulSoup(new, 'html.parser')
    html.findAll('table', id=idd)[0].replaceWith(new)
    return html.prettify()

_M_dict={}
def mass(engine, arg='x'):
    if (not arg in _M_dict.keys()):
        sk=engine.execute(f"select max({arg}) from point_on_map;")
        for vx in sk:
            _M_dict[arg]=vx[0]
    return _M_dict[arg]

#Dane inputu: nazwa inputu w formularzu to key, value to kolejno: 
dbparse={
    "player":{
        "player-color":["Player Color", "text", "Color of the player - use alphanumeric characters or space, _, -", "[A-Za-z0-9-_ ]{1,50}"]
    },
    
    "castle_on_map":{
        "castle_on_map-color":["Color", "select", "Color of the player owning this castle"],
        "castle_on_map-castle":["Type", "select", "Type of this castle"],
        "castle_on_map-x":["X", "number", "X coordinate of a castle - not higher than width selected by You - {}", ["1", "{}"]],
        "castle_on_map-y":["Y", "number", "Y coordinate of a castle - not higher than height selected by You - {}", ["1", "{}"]]
    },
    
    "building_in_castle_on_map":{
        "building_in_castle_on_map-build_name-castle":["Building name", "select", "Name of the building You want to create"],
        "building_in_castle_on_map-x-y-castle":["Castle", "select", "Where to insert that building"],
    },
    
    "hero":{
        "hero-name":["Hero name", "text", "Name of the Hero You want to create - use alphanumeric characters or space, _, -", "[A-Za-z0-9-_ ]{1,50}"],
        "hero-color":["Hero color", "select", "Player to whom the hero belongs"],
        "hero-id_army":["Hero army", "select", "Army belonging to this hero"],
        "hero-attack":["Attack", "number", "Coefficients of this hero, between 0 and 50000", ["0", "50000"]],
        "hero-defence":["Defence", "number", "Coefficients of this hero, between 0 and 50000", ["0", "50000"]],
        "hero-might":["Might", "number", "Coefficients of this hero, between 0 and 50000", ["0", "50000"]],
        "hero-wisdom":["Wisdom", "number", "Coefficients of this hero, between 0 and 50000", ["0", "50000"]],
    },
    
    "army":{
        "army-x":["X", "number", "X coordinate of an army - not higher than width selected by You - {}", ["1", "{}"]],
        "army-y":["Y", "number", "Y coordinate of an army - not higher than height selected by You - {}", ["1", "{}"]],
    },
    
    "army_connect":{
        "army_connect-id_army":["Army id", "select", "Army of this unit"],
        "army_connect-position":["Positon", "number", "Position in army - number between 1 and 7", ["1", "7"]],
        "army_connect-unit_name":["Unit", "select", "Name of an unit"],
        "army_connect-number_of_units":["Number", "number", "Number of units on this position, lower than 5*10^7", ["0", "50000000"]],
    } 
}

#Tworzenie selectów, egzekucja polecenia SQL
def dispatcher(engine, name, myval=None):
    dick={
        'castle_on_map-color':'select color from player union select NULL;',
        'castle_on_map-castle':'select castle_name from castles;',
        'building_in_castle_on_map-x-y-castle':'select x,y,castle from castle_on_map;',
        'building_in_castle_on_map-build_name-castle':'select build_name,castle_name from castle_building;',
        'hero-color':'select color from player;',
        'hero-id_army':'select id_army from army where hero_name is null;',
        'army_connect-id_army':'select id_army from army;',
        'army_connect-unit_name':'select unit_name from unit;', 
    }
    
    allezklar=f"<select name={name}>"
    #command to execute
    cte=dick[name]
    if (name=='hero-id_army' and myval!=None):
        cte=f"{cte[:-1]} union select id_army from army where id_army={myval};"


    for s in engine.execute(cte):
        s=[str(x) for x in s]
        if (myval==None or "-".join(list(s))!=myval):
            allezklar=allezklar+f'<option value="{"-".join(list(s))}">{"-".join(list(s))}</option>'
        else:
            allezklar=allezklar+f'<option value="{"-".join(list(s))}" selected=\"selected\">{"-".join(list(s))}</option>'
            
    allezklar=allezklar+"</select>"
    
    return allezklar

#Wypis errora na spodzie strony
def hterro(htcode, communicate):
    soup = BeautifulSoup(htcode, 'html.parser')
    dignity=f'<div id="error">{communicate}</div>'
    dignity=BeautifulSoup(dignity, 'html.parser')
    soup.body.append(dignity)
    return soup.prettify()

#Tworzenie HTML-a od inserta/updata
def htcreat(htcode, name, engine, fas=0, ite=None):
    soup = BeautifulSoup(htcode, 'html.parser')
    
    s=dbparse[name]
    mine=""
    for x in s.keys():
        #jeśli ite istnieje, sprawdzić wartość jego dla argumentu <oberżnięta nazwa z s-a(bez nazwy relacji)
        if (ite!=None):
            vall=ite[x[len(name)+1:]] 
        else:
            vall=0
        
        mine=mine+f"<div class=\"formverse\"> <div class=\"lform\"> <label for=\"{s[x][0]}\">{s[x][0]}</label></div> <div class=\"mform\">"
        if (s[x][1]=="select"):
            if (fas==0):
                mine=mine+dispatcher(engine, x)
            else:
                mine=mine+dispatcher(engine, x, vall)
        elif (s[x][1]=="number"):
            if (s[x][0][0]=="X" or s[x][0][0]=="Y"):
                xfk=mass(engine, arg=s[x][0][0])
                s[x][3][1]=xfk
                s[x][2]=s[x][2].format(xfk)

            if (fas==0):
                mine=mine+f"<input id=\"{s[x][0]}\" type=\"{s[x][1]}\" name=\"{x}\" min=\"{s[x][3][0]}\" max=\"{s[x][3][1]}\">"
            else:
                mine=mine+f"<input id=\"{s[x][0]}\" type=\"{s[x][1]}\" name=\"{x}\" value=\"{vall}\" min=\"{s[x][3][0]}\" max=\"{s[x][3][1]}\">"

        
        else:
            if (fas==0):
                mine=mine+f"<input id=\"{s[x][0]}\" type=\"{s[x][1]}\" name=\"{x}\" pattern=\"{s[x][3]}\" required>"
            else:
                mine=mine+f"<input id=\"{s[x][0]}\" type=\"{s[x][1]}\" name=\"{x}\" value=\"{vall}\" pattern=\"{s[x][3]}\" required>"
        mine=mine+f"</div> <div class=\"rform\"><label for=\"{s[x][0]}\">{s[x][2]}</label> </div></div>"
    mine=BeautifulSoup(mine, 'html.parser')
    soup.select("#changer")[0].append(mine)
    return soup.prettify()
