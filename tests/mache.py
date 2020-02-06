import unittest
import numpy as np
from flask import Flask, redirect, url_for, request
from beatsoup import *
from alchlib import *
import sys

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
        mlst=self.mlst
        heroo=self.heroo
        ee=engine.execute
        armiez=[0]*6
        unitz=[('Devil', 3), ('Archangel', 5), ('Power Lich', 3), ('Silver Pegasus', 12), ('Naga', 1), ('Minotaur King', 5)]

        #Tworzenie graczy, bohatyrów i armii
        interactor(engine, "", tp='proc', arg=['map_creator', [200, 100]])
        for i, w in enumerate(mlst):
            interactor(engine, f"insert into player values('{w}')" )
            interactor(engine, f"insert into army(x,y) values(1,{i+1})")
            for kx in engine.execute("select max(id_army) from army;"):
                fx=kx[0]
            mwynn=interactor(engine, f"insert into hero values('{heroo[i]}', '{w}', {fx})")
            self.assertTrue(mwynn[0]==0)
            armiez[i]=fx
            mwynn=interactor(engine, f"insert into army_connect values({fx}, 2, '{unitz[i][0]}', {unitz[i][1]})")
            
            self.assertTrue(mwynn[0]==0)
        #Army connect - update, delete
        for f in ee("select hero_name from army where y=3"):
            self.assertTrue(f[0]==heroo[2])
        mwynn=interactor(engine, f"update army_connect set id_army={armiez[5]}, unit_name='Black Knight', position=3 where id_army={armiez[4]}")
        self.assertTrue(mwynn[0]==0)

        for f in ee("select id_army from army_connect group by id_army having count(*)>1;"):
            self.assertTrue(f[0]==armiez[5])
        
        mwynn=interactor(engine, f"delete from army_connect where id_army={armiez[0]}")
        self.assertEqual(mwynn[1], '')
        for f in ee("select count(*) from army_connect;"):
            self.assertTrue(f[0]==5)
        
        #Hero - zmiana nazwy, usuwanie, kolor
        mwynn=interactor(engine, f"update hero set name='Vulpes' where id_army={armiez[1]}")
        self.assertEqual(mwynn[1], '')

        for f in ee(f"select hero_name from army where id_army={armiez[1]};"):
            self.assertEqual(f[0], 'Vulpes')

        mwynn=interactor(engine, f"delete from hero where id_army={armiez[1]}")
        self.assertEqual(mwynn[1], '')

        for f in ee(f"select name from hero where id_army={armiez[1]};"):
            self.assertTrue(False)
        for f in ee(f"select hero_name from army where id_army={armiez[1]};"):
            self.assertTrue(f[0] is None)

        #Hero - zmiana id armii
        mwynn=interactor(engine, f"update hero set id_army={armiez[1]} where id_army={armiez[2]}")
        self.assertEqual(mwynn[1], '')
        
        for f in ee(f"select hero_name from army where id_army={armiez[2]};"):
            self.assertTrue(f[0] is None)

        for f in ee(f"select hero_name from army where id_army={armiez[1]};"):
            self.assertEqual(f[0],  heroo[2])
        
        #Usuwanie armii 2. z 3. herosem
        mwynn=interactor(engine, "", tp='procp', arg=['army_slayer', [armiez[1]]])
        self.assertEqual(mwynn[1], '')
        
        for f in ee(f"select hero_name from army where hero_name='{heroo[2]}';"):
            self.assertEqual('Hero is not dead', 'Hero should be dead')
         
        mwynn=interactor(engine, "", tp='procp', arg=['army_slayer', [armiez[1]]])
        self.assertEqual(mwynn[1], '')

        mwynn=interactor(engine, f"insert into army(x, y) values(1,1)")
        self.assertEqual(mwynn[1], '')
        mwynn=interactor(engine, f"insert into army(x, y) values(1,1)")
        self.assertEqual(mwynn[1], 'There are already two armies on this point!')
        
        for kx in ee("select max(id_army) from army;"):
            fx=kx[0]
         
        mwynn=interactor(engine, f"insert into hero(name, color, id_army) values('Arthur','green',{fx})")
        self.assertEqual(mwynn[1], '')



if (__name__=='__main__'):
    engine = create_engine('postgresql+psycopg2://postgres:dayne@localhost:54320/postgres', echo = True)

    unittest.main()
