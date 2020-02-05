import unittest
import numpy as np
from flask import Flask, redirect, url_for, request
from beatsoup import *
from alchlib import *

app = Flask(__name__)


def map_creator(x1, x2):
    z=f"""do $$ begin 
    perform map_creator({x1}, {x2}); 
    end $$;"""
    return z

class bazikunit(unittest.TestCase):

    @classmethod
    def tearDownClass(self):
        tables=['army_connect', 'building_in_castle_on_map', 'castle_on_map', 'hero', 'army', 'player', 'point_on_map']
        for x in tables:
            xv=interactor(engine, f"delete from {x}")
            if (xv[0]!=0):
                raise AssertionError
    
    @classmethod
    def setUp(self):
        self.mlst=['red', 'green', 'black', 'orange', 'purple', 'yellow']
        self.heroo=['Jonasz', 'Eliasz', 'Elizeusz', 'Abraham', 'Izaak', 'Hiob']
        
        tables=['army_connect', 'building_in_castle_on_map', 'castle_on_map', 'hero', 'army', 'player', 'point_on_map']
        for x in tables:
            xv=interactor(engine, f"delete from {x}")
            if (xv[0]!=0):
                raise AssertionError




    def test_mapCreator(self):
        mwynn=interactor(engine, "", tp='proc', arg=['map_creator', [200, 100]])   
        self.assertTrue(mwynn[0]==0)

        for i in range(15):
            x1, y1=np.random.randint(1, 200), np.random.randint(1, 100)
            x=engine.execute(f'select count(*) from point_on_map where x={x1} and y={y1};')
            for w in x:
                self.assertTrue(int(w[0])==1)

            x1, y1=np.random.randint(1, 200), np.random.randint(101, 200)
            x=engine.execute(f'select count(*) from point_on_map where x={x1} and y={y1};')
            for w in x:
                self.assertTrue(int(w[0])==0)
 
        mwynn=interactor(engine, "delete from point_on_map")
        self.assertTrue(mwynn[0]==0)




    def test_player(self):
        mlst=self.mlst
        heroo=self.heroo
        
        #Tworzenie graczy
        interactor(engine, "", tp='proc', arg=['map_creator', [200, 100]])   
        for w in mlst:
            mwynn=interactor(engine, f"insert into player values('{w}')" )
            self.assertTrue(mwynn[0]==0)
        
        #Czy liczba graczy się zgadza?
        x=engine.execute(f'select count(*) from player;')
        for w in x:
            self.assertTrue(int(w[0])==len(mlst))

        #Za długa nazwa, powtarzana nazwa
        mwynn=interactor(engine, f"insert into player values('OzjaszvsGoldbergvsCorvinvsMikkvsGratiaWielomianiIFFTido50znakowRaczejStarczi')" )
        self.assertTrue(mwynn[1]=="You cannot use names longer than 50 characters!")
        self.assertTrue(mwynn[0]==1)
        mwynn=interactor(engine, f"insert into player values('yellow')" )
        self.assertTrue(mwynn[1]=="Player already inserted!")
        mwynn=interactor(engine, f"update player set color='yellow' where color='green'" )
        self.assertTrue(mwynn[1]=="Player already inserted!")
        
        #Tworzenie paru zamków i bohaterów dla graczy
        for i in range(len(mlst)):
            mwynn=interactor(engine, f"insert into castle_on_map values(1, {i+1}, '{mlst[i]}', 'Necropolis');")
            self.assertTrue(mwynn[0]==0)
            mwynn=interactor(engine, f"insert into castle_on_map values(2, {i+1}, '{mlst[i]}', 'Inferno');")
            self.assertTrue(mwynn[0]==0)
            mwynn=interactor(engine, f"insert into army(x, y) values(3, {i+1});")
            self.assertTrue(mwynn[0]==0)

            for w in engine.execute('select max(id_army) from army'):
                ida=w[0]

            mwynn=interactor(engine, f"insert into hero(name, color, id_army) values('{heroo[i]}', '{mlst[i]}', {ida});")
            self.assertTrue(mwynn[0]==0)
        
        #Update koloru - czy zamki i bohaterowie się zgadzają?
        mwynn=interactor(engine, f"update player set color='brown' where color='red';")
        self.assertTrue(mwynn[0]==0)
        for w in engine.execute("select count(*) from castle_on_map where color='brown';"):
            self.assertTrue(w[0]==2)
        for w in engine.execute("select count(*) from hero where color='brown';"):
            self.assertTrue(w[0]==1)

        mwynn=interactor(engine, "", tp='procp', arg=['player_slayer', ['green']])
        for w in engine.execute("select count(*) from castle_on_map where color is null;"):
            self.assertTrue(w[0]==2)
        for w in engine.execute("select count(*) from castle_on_map;"):
            self.assertTrue(w[0]==12)

        for w in engine.execute("select count(*) from hero where color='green';"):
            self.assertTrue(w[0]==0)
        for w in engine.execute("select count(*) from hero;"):
            self.assertTrue(w[0]==5)
        for w in engine.execute("select count(*) from army;"):
            self.assertTrue(w[0]==5)

        for w in engine.execute("select count(*) from player where color='green';"):
            self.assertTrue(w[0]==0)


    def test_castle(self):
        mlst=self.mlst[:2]
        heroo=self.heroo[:2]
        
        #Tworzenie graczy
        interactor(engine, "", tp='proc', arg=['map_creator', [200, 100]])   
        for w in mlst:
            interactor(engine, f"insert into player values('{w}')" )
        #Wstawianie zamku i budynku: związanego z poprawnym zamkiem, niepoprawnym zamkiem(2 sposoby)
        for i in range(len(mlst)):
            tcast='Necropolis'
            interactor(engine, f"insert into castle_on_map values(1, {i+1}, '{mlst[i]}', '{tcast}');")
            mwynn=interactor(engine, f"insert into building_in_castle_on_map values(1, {i+1}, 'Capitol', '{tcast}')")
            self.assertTrue(mwynn[0]==0)
            mwynn=interactor(engine, f"insert into building_in_castle_on_map values(1, {i+1}, 'Capitol', 'Inferno')")

            self.assertTrue(mwynn[1]=='You merged incorrect types of castle!')
            mwynn=interactor(engine, f"insert into building_in_castle_on_map values(1, {i+1}, 'Pillar of Eyes', '{tcast}')")
            self.assertTrue(mwynn[1]=="This type of building doesn't exist for that castle!")
            
            #Zmiana koloru i punktu umiejscowienia zamku: nic złego nie powinno się dziać
            mwynn=interactor(engine, f"update castle_on_map set x=12, y={i+10} where x=1 and y={i+1}")
            self.assertTrue(mwynn[0]==0)
            mwynn=interactor(engine, f"update castle_on_map set color='green' where color='red'")
            self.assertTrue(mwynn[0]==0)
            

            #Zmiana typu zamku albo usunięcie: wszystkie budynki są usuwane
            for w in engine.execute(f"select count(*) from building_in_castle_on_map where x=12 and y={i+10};"):
                self.assertTrue(w[0]==1)

            mwynn=interactor(engine, f"update castle_on_map set castle='Inferno' where x=12 and y={i+10}")            
            self.assertTrue(mwynn[0]==0)
           
            for w in engine.execute(f"select count(*) from building_in_castle_on_map where x=12 and y={i+10};"):
                self.assertTrue(w[0]==0)
 
            mwynn=interactor(engine, f"insert into building_in_castle_on_map values(12, {i+10}, 'Forsaken Palace', 'Inferno');")            
            self.assertTrue(mwynn[0]==0)
            
            for w in engine.execute(f"select count(*) from building_in_castle_on_map where x=12 and y={i+10} and castle='Inferno';"):
                self.assertTrue(w[0]==1)
            
            mwynn=interactor(engine, f"delete from castle_on_map where x=12 and y={i+10};")            
            self.assertTrue(mwynn[0]==0)
            
            for w in engine.execute(f"select count(*) from building_in_castle_on_map where x=12 and y={i+10};"):
                self.assertTrue(w[0]==0)
            for w in engine.execute(f"select count(*) from castle_on_map where x=12 and y={i+10};"):
                self.assertTrue(w[0]==0)

    def test_armies(self):
        assertTrue(False)



if (__name__=='__main__'):
    engine = create_engine('postgresql+psycopg2://postgres:dayne@localhost:54320/postgres', echo = True)

    unittest.main()
