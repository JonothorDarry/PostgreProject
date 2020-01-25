from flask import Flask, redirect, url_for, request
from beatsoup import changer

app = Flask(__name__)

@app.route('/overall.css')
def css_route():
    fil=open('../apps/overall.css')
    return fil.read() 


@app.route('/playersel')
def players():
    fil=open('../apps/2player.html')
    cf=fil.read()
    return changer(cf)



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
