from flask import Flask, redirect, url_for, request
from beatsoup import changer

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
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        return redirect(url_for(wanderer(z)))

@app.route('/castlesel', methods = ['POST', 'GET'])
def castles():
    if (request.method=='GET'):
        fil=open('../apps/3castle.html')
        cf=fil.read()
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='ins' or z=='upd' or z=='del'):
            pass

        return redirect(url_for(wanderer(z)))


@app.route('/armysel', methods = ['POST', 'GET'])
def armys():
    if (request.method=='GET'):
        fil=open('../apps/5army.html')
        cf=fil.read()
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='ins' or z=='upd' or z=='del'):
            pass

        return redirect(url_for(wanderer(z)))




@app.route('/playersel', methods = ['POST', 'GET'])
def players():
    if (request.method=='GET'):
        fil=open('../apps/2player.html')
        cf=fil.read()
        return changer(cf)
    if (request.method=='POST'):
        z=request.form['which']
        if (z=='ins' or z=='upd'):
            redirect(url_for('playeri'))

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
    app.run()
