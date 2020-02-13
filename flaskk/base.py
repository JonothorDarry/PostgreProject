from flask import Flask, redirect, url_for, request, send_from_directory
import flask
from beatsoup import *
from alchlib import *
import codecs
import subprocess
app = Flask(__name__)

#fas: 1 - update, wtedy w ite jest dict ze zmianami
fas=0
ite=0
#Black flag - tu są składowane błędy
black_flag=[0, '']

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/arda.png')
def static_file():
    return flask.send_file('arda.png', mimetype='kappa')


#Dokąd prowadzi ten podróżnik? Buttony do mety, armii i innych
def wanderer(pname):
    if (pname=='cast'):
        return 'castles'
    elif (pname=='met'):
        return ('metas')
    elif (pname=='play'):
        return 'players'
    elif (pname=='help'):
        return 'helper'
    return 'armys'



#Zajmuje się insert/updatem
def iu_handler(request, htm, name, engine, ret, erro):
    global fas
    global ite
    global black_flag
    #Pokazanie interfejsu, uzależnienie od tego, czy insert, czy update(fas), czarna flaga - zaszedł błąd
    if (request.method=='GET'):
        fil=open(htm)
        cf=fil.read()
        if (fas!=0):
            cf=htcreat(cf, name, engine, fas, ite)
        else:
            cf=htcreat(cf, name, engine)
        
        if (black_flag[0]==1):
            cf=hterro(cf, black_flag[1])

        black_flag=[0, '']
        return changer(cf)
    #Jeśli było postowanie - albo back, zwykły powrót, albo zmiana bazy
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='pure'):
            #vynn - wynik egzekucji, ewentualnie komunikat błędu
            if (fas==0):
                vynn=insert_preparer(engine, request.form, name, 'insert')
            else:
                vynn=update_preparer(engine, ite, request.form, name, 'update')
            #Jeśli błąd, zostaje na stronie z komunikatem o błędzie 
            black_flag=vynn
            if (vynn[0]==1):
                return redirect(url_for(erro))
        inserto_creato_mapo(engine)
        return redirect(url_for(ret))


def savedb(engine, name="mydba", dire="~/Downloads"):
    cmd1=f"docker exec posts pg_dump -U postgres postgres > somalia/{name}"
    cmd2=f"cp somalia/{name} {dire}"
    
    subprocess.call(cmd1, shell=True)
    subprocess.call(cmd2, shell=True)


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
    return interactor(engine, ls) 


#Update tabeli: data to dane, old - stare dane, opera - operacja, table - tablica do zmiany, data - dane do parsowania
#dictvisioner - dict na oucie posta do normalnego dicta do inserta, parser: dane na zapytkę, interactor: wykonanie polecenia
def update_preparer(engine, old, data, table, opera):
    vd=dictvisioner(data)
    ls=parser(table, opera, ins=vd, wher=old)
    return interactor(engine, ls)


#Małe sprawdzenie, czy update, czy insert, stosowne zmiany makrokodu - globalsy
def microchecker(z, formz):
    global fas
    global ite
    
    fas=0
    if ('upd' in z):
        if (len(formz)>1):
            qry=dictvisioner(formz, alter=0)
            fas=1
            ite=qry
            return 1
        return -1
    return 1



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
        return changer(cf, ['castles', 'castle_building', 'resources', 'unit']) #Zwracanie HTML-a
    #Zmiana lokacji
    if (request.method=='POST'):
        z=request.form['which']
        return redirect(url_for(wanderer(z)))


#Helper
@app.route('/helper', methods = ['POST', 'GET'])
def helper():
    if (request.method=='GET'):
        fil=open('../apps/12helper.html')  #Otwarcie html-a
        cf=fil.read()
        return changer(cf, []) #Zwracanie HTML-a
    #Zmiana lokacji
    if (request.method=='POST'):
        z=request.form['which']
        return redirect(url_for(wanderer(z)))





@app.route('/castleins', methods = ['POST', 'GET'])
def castlei():
    return iu_handler(request, '../apps/8formcastle.html', "castle_on_map", engine, 'castles', 'castlei')

@app.route('/buildins', methods = ['POST', 'GET'])
def buildi():
    return iu_handler(request, '../apps/9formbuild.html', "building_in_castle_on_map", engine, 'castles', 'buildi')

@app.route('/castlesel', methods = ['POST', 'GET'])
def castles():
    if (request.method=='GET'):
        fil=open('../apps/3castle.html')
        cf=fil.read()
        cf=select_preparer(engine, ["castle_on_map", "building_in_castle_on_map"], cf)
        return changer(cf, ["castle_on_map", "building_in_castle_on_map"])

    if (request.method=='POST'):
        z=request.form['which']
        if (z=='insc' or z=='updc'):
            rs=microchecker(z, request.form)
            if (rs==-1):
                return redirect(url_for('castles'))
            return redirect(url_for('castlei'))
            
        elif (z=='insb' or z=='updb'):
            rs=microchecker(z, request.form)
            if (rs==-1):
                return redirect(url_for('castles'))
            return redirect(url_for('buildi'))
            
        elif(z=='delc'):
            qry=dictvisioner(request.form, alter=0)
            qry=parser('castle_on_map', opera='delete', wher=qry)
            mwynn=interactor(engine, qry)
            inserto_creato_mapo(engine)
            return redirect(url_for('castles'))
        elif(z=='delb'):
            qry=dictvisioner(request.form, alter=0)
            qry=parser('building_in_castle_on_map', opera='delete', wher=qry)
            mwynn=interactor(engine, qry)
            inserto_creato_mapo(engine)
            return redirect(url_for('castles'))
        elif(z=='saver'):
            savedb(engine)
            return redirect(url_for('castles'))

        return redirect(url_for(wanderer(z)))










@app.route('/armyins', methods = ['POST', 'GET'])
def armyi():
    return iu_handler(request, '../apps/7formarmy.html', "army", engine, 'armys', 'armyi')
        
@app.route('/heroins', methods = ['POST', 'GET'])
def heroi():
    return iu_handler(request, '../apps/6formhero.html', "hero", engine, 'armys', 'heroi') 

@app.route('/aconins', methods = ['POST', 'GET'])
def aconi():
    return iu_handler(request, '../apps/11formarmycon.html', "army_connect", engine, 'armys', 'aconi') 




@app.route('/armysel', methods = ['POST', 'GET'])
def armys():
    if (request.method=='GET'):
        fil=open('../apps/5army.html')
        cf=fil.read()
        #Zmiana HTML-a wyświetlanego: 3 tablice do zamiany; selector: wybór danych dla tabeli, selhtmler zamienia x-a i tabelę w html-a, supchanger zamienia 1 kod na 2.
        cf=select_preparer(engine, ["army", "hero", "army_connect"], cf)
        return changer(cf, ["army", "hero", "army_connect"])
    
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='insa' or z=='upda'):
            rs=microchecker(z, request.form)
            if (rs==-1):
                return redirect(url_for('armys'))
            return redirect(url_for('armyi')) 
        elif (z=='insh' or z=='updh'):
            rs=microchecker(z, request.form)
            if (rs==-1):
                return redirect(url_for('armys'))
            return redirect(url_for('heroi'))
        elif (z=='insc' or z=='updc'):
            rs=microchecker(z, request.form)
            if (rs==-1):
                return redirect(url_for('armys'))
            return redirect(url_for('aconi'))
            
        elif(z=='dela'):
            #Removal armii: szystko albo jedna
            if (not 'id_army' in request.form):
                mn=engine.execute('select id_army from army')
                for xvf in mn:
                    interactor(engine, "", tp='procp', arg=['army_slayer', [xvf[0]]])
            else:
                mwynn=interactor(engine, "", tp='procp', arg=['army_slayer', [request.form['id_army']]])

            inserto_creato_mapo(engine)
            return redirect(url_for('armys'))
        elif(z=='delh'):
            qry=dictvisioner(request.form, alter=0)
            qry=parser('hero', opera='delete', wher=qry)
            mwynn=interactor(engine, qry)
            inserto_creato_mapo(engine)
            return redirect(url_for('armys'))
        elif(z=='delc'):
            qry=dictvisioner(request.form, alter=0)
            qry=parser('army_connect', opera='delete', wher=qry)
            mwynn=interactor(engine, qry)
            inserto_creato_mapo(engine)
            return redirect(url_for('armys'))
        elif(z=='saver'):
            savedb(engine)
            return redirect(url_for('armys'))

        return redirect(url_for(wanderer(z)))








@app.route('/playerins', methods = ['POST', 'GET'])
def playeri():
    return iu_handler(request, '../apps/10formplayer.html', "player", engine, 'players', 'playeri') 

@app.route('/playersel', methods = ['POST', 'GET'])
def players():
    if (request.method=='GET'):
        fil=open('../apps/2player.html')
        cf=fil.read()
        #Zmiana HTML-a wyświetlanego: 3 tablice do zamiany; selector: wybór danych dla tabeli, selhtmler zamienia x-a i tabelę w html-a, supchanger zamienia 1 kod na 2.
        cf=select_preparer(engine, ["player"], cf)
        return changer(cf, ['player'])
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='ins' or z=='upd'):
            rs=microchecker(z, request.form)
            if (rs==-1):
                return redirect(url_for('players'))
            return redirect(url_for('playeri'))
        elif(z=='del'):
            if (not 'color' in request.form):
                mn=engine.execute('select color from player')
                for xvf in mn:
                    interactor(engine, "", tp='procp', arg=['player_slayer', [xvf[0]]])
            else:
                mwynn=interactor(engine, "", tp='procp', arg=['player_slayer', [request.form['color']]])
            inserto_creato_mapo(engine)
            return redirect(url_for('players'))
        elif(z=='saver'):
            savedb(engine)
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
            subprocess.call('../velvet_updater.sh', shell=True)
            interactor(engine, "", tp='proc', arg=['map_creator', [c['wid'], c['hei']]])
        elif(z=='loader'):
            c=request.form
            vv=request.form['disk']
            mstr="/"
            cmd1=f"docker cp {vv} posts:/home/"
            cmd2=f'docker exec posts sh -c "psql -U postgres postgres < /home/{vv.split(mstr)[-1]}"'
            subprocess.call(cmd1, shell=True)
            subprocess.call(cmd2, shell=True)

        inserto_creato_mapo(engine)
        return redirect(url_for('players'))


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response



if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://postgres:dayne@localhost:54320/postgres', echo = False)
    app.run()
