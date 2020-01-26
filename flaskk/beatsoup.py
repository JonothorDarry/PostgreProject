from bs4 import BeautifulSoup

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
