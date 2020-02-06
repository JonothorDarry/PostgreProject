from bs4 import BeautifulSoup
from alchlib import *

def changer(html_file):
    soup = BeautifulSoup(html_file, 'html.parser')
    fil=open('../apps/overall.css')
    z=fil.read()
    z="<head>\n<style>\n"+z+"\n</style>\n</head>"

    zk=BeautifulSoup(z, 'html.parser')
    soup.head.replace_with(zk)
    d=soup.prettify()
    return d

def supchanger(html, idd, new):
    html=BeautifulSoup(html, 'html.parser')
    new=BeautifulSoup(new, 'html.parser')
    html.findAll('table', id=idd)[0].replaceWith(new)
    return html.prettify()

#Elfstone
dbparse={
    "player":{
        "player-color":["Player Color", "text", "Color of the player"]
    },
    
    "castle_on_map":{
        "castle_on_map-color":["Color", "select", "Color of the player owning this castle"],
        "castle_on_map-castle":["Type", "select", "Type of this castle"],
        "castle_on_map-x":["X", "text", "X coordinate of a castle"],
        "castle_on_map-y":["Y", "text", "Y coordinate of a castle"]
    },
    
    "building_in_castle_on_map":{
        "building_in_castle_on_map-build_name-castle":["Building name", "select", "Name of the building You want to create"],
        "building_in_castle_on_map-x-y-castle":["Castle", "select", "Where to insert that building"],
    },
    
    "hero":{
        "hero-name":["Hero name", "text", "Name of the Hero You want to create"],
        "hero-color":["Hero color", "select", "Player to whom the hero belongs"],
        "hero-id_army":["Hero army", "select", "Army belonging to this hero"],
        "hero-attack":["Attack", "text", "Coefficients of this hero"],
        "hero-defence":["Defence", "text", "Coefficients of this hero"],
        "hero-might":["Might", "text", "Coefficients of this hero"],
        "hero-wisdom":["Wisdom", "text", "Coefficients of this hero"],
    },
    
    "army":{
        "army-x":["X", "text", "X coordinate of an army"],
        "army-y":["Y", "text", "Y coordinate of an army"],
    },
    
    "army_connect":{
        "army_connect-id_army":["Army id", "select", "Army of this unit"],
        "army_connect-position":["Positon", "text", "Position in army - number between 0 and 7"],
        "army_connect-unit_name":["Unit", "select", "Name of an unit"],
        "army_connect-number_of_units":["Number", "text", "Number of units on this position"],
    }
    
}


def dispatcher(engine, name):
    dick={
        'castle_on_map-color':'select color from player;',
        'castle_on_map-castle':'select castle_name from castles;',
        'building_in_castle_on_map-x-y-castle':'select x,y,castle from castle_on_map;',
        'building_in_castle_on_map-build_name-castle':'select build_name,castle_name from castle_building;',
        'hero-color':'select color from player;',
        'hero-id_army':'select id_army from army where hero_name is null;',
        'army_connect-id_army':'select id_army from army;',
        'army_connect-unit_name':'select unit_name from unit;',    
    }


    allezklar=f"<select name={name}>"
    for s in engine.execute(dick[name]):
        s=[str(x) for x in s]
        print("-".join(list(s)))

        allezklar=allezklar+f'<option value="{"-".join(list(s))}">{"-".join(list(s))}</option>'
    allezklar=allezklar+"</select>"

    return allezklar

def htcreat(htcode, name, engine):
    soup = BeautifulSoup(htcode, 'html.parser')
    
    s=dbparse[name]
    mine=""
    for x in s.keys():
        mine=mine+f"<label>{s[x][0]}"
        if (s[x][1]=="select"):
            mine=mine+dispatcher(engine, x)
        else:
            mine=mine+f"<input type=\"{s[x][1]}\" name=\"{x}\">"
        mine=mine+f"{s[x][2]}</label><br>"
    mine=BeautifulSoup(mine, 'html.parser')
    soup.select("#changer")[0].append(mine)
    return soup.prettify()
