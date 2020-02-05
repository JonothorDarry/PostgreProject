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
        
        mwynn=interactor(engine, "", tp='proc', arg=['map_creator', [200, 100]])   
        for w in mlst:
            mwynn=interactor(engine, f"insert into player values('{w}')" )
            self.assertTrue(mwynn[0]==0)
        
        x=engine.execute(f'select count(*) from player;')
        for w in x:
            self.assertTrue(int(w[0])==len(mlst))

        mwynn=interactor(engine, f"insert into player values('OzjaszvsGoldbergvsCorvinvsMikkvsGratiaWielomianiIFFTido50znakowRaczejStarczi')" )
        self.assertTrue(mwynn[1]=="You cannot use names longer than 50 characters!")
        self.assertTrue(mwynn[0]==1)
        
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
        
        mwynn=interactor(engine, f"update player set color='brown' where color='red';")
        self.assertTrue(mwynn[0]==0)
        
        for w in engine.execute("select count(*) from castle_on_map where color='brown';"):
            self.assertTrue(w[0]==2)
        
        for w in engine.execute("select count(*) from hero where color='brown';"):
            self.assertTrue(w[0]==1)

        #mwynn=interactor(engine, "delete from player")
        #print(mwynn)
        #self.assertTrue(mwynn[0]==0)

    def test_dritte(self):
        self.assertTrue(True)

if (__name__=='__main__'):
    engine = create_engine('postgresql+psycopg2://postgres:dayne@localhost:54320/postgres', echo = True)

    unittest.main()
