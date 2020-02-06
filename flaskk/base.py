from flask import Flask, redirect, url_for, request
from beatsoup import *
from alchlib import *

app = Flask(__name__)

#Dokąd prowadzi ten podróżnik? Buttony do mety, armii i innych
def wanderer(pname):
    if (pname=='cast'):
        return 'castles'
    elif (pname=='met'):
        return ('metas')
    elif (pname=='play'):
        return 'players'
    return 'armys'

#Zmiana HTML-a wyświetlanego: arr-tablice do zamiany, cf-kod htmla, engine - silnik bazy
#selector: wybór danych dla tabeli, selhtmler zamienia x-a i tabelę w html-a, supchanger zamienia 1 kod na 2.
def select_preparer(engine, arr, cf):
    for x in arr:
        y=selector(engine, x)
        z=selhtmler(x, y)
        cf=supchanger(cf, x, z)
    return cf

#Zapis do tabeli: data to dane, opera - operacja, table - tablica do zmiany, data - dane do parsowania
#dictvisioner - dict na oucie posta do normalnego dicta do inserta, parser: dane na zapytkę, interactor: wykonanie polecenia
def insert_preparer(engine, data, table, opera):
    vd=dictvisioner(data)
    ls=parser(table, opera, ins=vd)
    interactor(engine, ls) 


#CSS
@app.route('/overall.css')
def css_route():
    fil=open('../apps/overall.css')
    return fil.read() 



#Metawiedza
@app.route('/metasel', methods = ['POST', 'GET'])
def metas():
    if (request.method=='GET'):
        fil=open('../apps/4meta.html')  #Otwarcie html-a
        cf=fil.read()
        cf=select_preparer(engine, ["unit", "resources", "castles", "castle_building"], cf) #SQL->HTML
        return changer(cf) #Zwracanie HTML-a
    #Zmiana lokacji
    if (request.method=='POST'):
        z=request.form['which']
        return redirect(url_for(wanderer(z)))







@app.route('/castleins', methods = ['POST', 'GET'])
def castlei():
    if (request.method=='GET'):
        fil=open('../apps/8formcastle.html')
        cf=fil.read()
        cf=htcreat(cf, "castle_on_map", engine)
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            insert_preparer(engine, request.form, 'castle_on_map', 'insert')
        return redirect(url_for('castles'))
        
@app.route('/buildins', methods = ['POST', 'GET'])
def buildi():
    if (request.method=='GET'):
        fil=open('../apps/9formbuild.html')
        cf=fil.read()
        cf=htcreat(cf, "building_in_castle_on_map", engine)
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            insert_preparer(engine, request.form, 'building_in_castle_on_map', 'insert')
        return redirect(url_for('castles'))



@app.route('/castlesel', methods = ['POST', 'GET'])
def castles():
    if (request.method=='GET'):
        fil=open('../apps/3castle.html')
        cf=fil.read()
        cf=select_preparer(engine, ["castle_on_map", "building_in_castle_on_map"], cf)
        return changer(cf)

    if (request.method=='POST'):
        z=request.form['which']
        if (z=='insc' or z=='updc'):
            return redirect(url_for('castlei'))
            
        elif (z=='insb' or z=='updb'):
            return redirect(url_for('buildi'))
            
        elif(z=='delc'):
            return redirect(url_for('castles'))
        elif(z=='delb'):
            return redirect(url_for('castles'))

        return redirect(url_for(wanderer(z)))










@app.route('/armyins', methods = ['POST', 'GET'])
def armyi():
    if (request.method=='GET'):
        fil=open('../apps/7formarmy.html')
        cf=fil.read()
        cf=htcreat(cf, "army", engine)
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            insert_preparer(engine, request.form, 'army', 'insert')
        return redirect(url_for('armys'))
        
@app.route('/heroins', methods = ['POST', 'GET'])
def heroi():
    if (request.method=='GET'):
        fil=open('../apps/6formhero.html')
        cf=fil.read()
        cf=htcreat(cf, "hero", engine)
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            insert_preparer(engine, request.form, 'hero', 'insert')
        return redirect(url_for('armys'))

@app.route('/aconins', methods = ['POST', 'GET'])
def aconi():
    if (request.method=='GET'):
        fil=open('../apps/11formarmycon.html')
        cf=fil.read()
        cf=htcreat(cf, "army_connect", engine)
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            insert_preparer(engine, request.form, 'army_connect', 'insert')
        return redirect(url_for('armys'))




@app.route('/armysel', methods = ['POST', 'GET'])
def armys():
    if (request.method=='GET'):
        fil=open('../apps/5army.html')
        cf=fil.read()
        #Zmiana HTML-a wyświetlanego: 3 tablice do zamiany; selector: wybór danych dla tabeli, selhtmler zamienia x-a i tabelę w html-a, supchanger zamienia 1 kod na 2.
        cf=select_preparer(engine, ["army", "hero", "army_connect"], cf)
        return changer(cf)
    
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='insa' or z=='upda'):
            return redirect(url_for('armyi')) 
        elif (z=='insh' or z=='updh'):
            return redirect(url_for('heroi'))
        elif (z=='insc' or z=='updc'):
            return redirect(url_for('aconi'))
            
        elif(z=='dela'):
            return redirect(url_for('armys'))
        elif(z=='delh'):
            return redirect(url_for('armys'))
        elif(z=='delc'):
            return redirect(url_for('armys'))

        return redirect(url_for(wanderer(z)))










@app.route('/playerins', methods = ['POST', 'GET'])
def playeri():
    if (request.method=='GET'):
        fil=open('../apps/10formplayer.html')
        cf=fil.read()
        cf=htcreat(cf, "player", engine)
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='pure'):
            insert_preparer(engine, request.form, 'player', 'insert')

        return redirect(url_for('players'))

@app.route('/playersel', methods = ['POST', 'GET'])
def players():
    if (request.method=='GET'):
        fil=open('../apps/2player.html')
        cf=fil.read()
        #Zmiana HTML-a wyświetlanego: 3 tablice do zamiany; selector: wybór danych dla tabeli, selhtmler zamienia x-a i tabelę w html-a, supchanger zamienia 1 kod na 2.
        cf=select_preparer(engine, ["player"], cf)

        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='ins' or z=='upd'):
            return redirect(url_for('playeri'))
        elif(z=='del'):
            return redirect(url_for('players'))
        return redirect(url_for(wanderer(z)))
        





@app.route('/', methods = ['POST', 'GET'])
def hello_world():
    if (request.method=='GET'):
        fil=open('../apps/1start.html')
        cf=fil.read()
        return changer(cf)

    if (request.method=='POST'): 
        z=request.form['which']
        if (z=='creator'):
            c=request.form
            interactor(engine, "", tp='proc', arg=['map_creator', [c['wid'], c['hei']]])
        return redirect(url_for('players'))

if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://postgres:dayne@localhost:54320/postgres', echo = False)
    app.run()
