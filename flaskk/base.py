from flask import Flask, redirect, url_for, request
from beatsoup import *
from alchlib import *

app = Flask(__name__)

def wanderer(pname):
    if (pname=='cast'):
        return 'castles'
    elif (pname=='met'):
        return ('metas')
    elif (pname=='play'):
        return 'players'
    return 'armys'

@app.route('/overall.css')
def css_route():
    fil=open('../apps/overall.css')
    return fil.read() 




@app.route('/metasel', methods = ['POST', 'GET'])
def metas():
    if (request.method=='GET'):
        fil=open('../apps/4meta.html')
        cf=fil.read()
        arr=["unit", "resources", "castles", "castle_building"]
        for x in arr:
            y=selector(engine, x)
            z=selhtmler(x, y)
            cf=supchanger(cf, x, z)

        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        return redirect(url_for(wanderer(z)))







@app.route('/castleins', methods = ['POST', 'GET'])
def castlei():
    if (request.method=='GET'):
        fil=open('../apps/8formcastle.html')
        cf=fil.read()
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            pass
        return redirect(url_for('castles'))
        
@app.route('/buildins', methods = ['POST', 'GET'])
def buildi():
    if (request.method=='GET'):
        fil=open('../apps/9formbuild.html')
        cf=fil.read()
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            pass
        return redirect(url_for('castles'))



@app.route('/castlesel', methods = ['POST', 'GET'])
def castles():
    if (request.method=='GET'):
        fil=open('../apps/3castle.html')
        cf=fil.read()
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
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            pass
        return redirect(url_for('armys'))
        
@app.route('/heroins', methods = ['POST', 'GET'])
def heroi():
    if (request.method=='GET'):
        fil=open('../apps/6formhero.html')
        cf=fil.read()
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            pass
        return redirect(url_for('armys'))

@app.route('/armysel', methods = ['POST', 'GET'])
def armys():
    if (request.method=='GET'):
        fil=open('../apps/5army.html')
        cf=fil.read()
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='insa' or z=='upda'):
            return redirect(url_for('armyi'))
            
        elif (z=='insh' or z=='updh'):
            return redirect(url_for('heroi'))
            
        elif(z=='dela'):
            return redirect(url_for('armys'))
        elif(z=='delh'):
            return redirect(url_for('armys'))

        return redirect(url_for(wanderer(z)))










@app.route('/playerins', methods = ['POST', 'GET'])
def playeri():
    if (request.method=='GET'):
        fil=open('../apps/10formplayer.html')
        cf=fil.read()
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        
        if (z=='pure'):
            pass

        return redirect(url_for('players'))

@app.route('/playersel', methods = ['POST', 'GET'])
def players():
    if (request.method=='GET'):
        fil=open('../apps/2player.html')
        cf=fil.read()
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
        return redirect(url_for('players'))

if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://postgres:dayne@localhost:54320/postgres', echo = True)
    app.run()
