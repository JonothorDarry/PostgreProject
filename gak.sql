--PostgreSQL 9.6
--';' is a delimiter

--Wyrzucanie starych tabel
drop table Building_in_castle_on_map;
drop table Castle_on_map;
drop table Army_connect cascade;
drop table Army cascade;
drop table Hero;
drop table Player;
drop table Point_on_map;
drop table Unit;
drop table Castle_Building;
drop table Castles;
drop table Resources;
drop domain uint;

--dziedzina unsigned inta
create domain uint as int
check(value>=0);

--Zasoby: metawiedza
create table Resources(
    gold uint,
    wood uint,
    stone uint,
    gems uint, 
    sulfur uint,
    mercury uint,
    crystal uint,
    id_resource serial unique,
    constraint pk_resources primary key(gold, wood, stone, gems, sulfur, mercury, crystal)
);

--Zamki: metawiedza
create table Castles(
    castle_name varchar(50),
    constraint pk_castles primary key(castle_name)
);

--Budynki w zamku: metawiedza
create table Castle_Building(
    build_name varchar(50),
    castle_name varchar(50),
    id_resources int not null,
    constraint fk_idres foreign key(id_resources) references Resources(id_resource),
    constraint fk_castle foreign key(castle_name) references Castles(castle_name),
    constraint pk_castle_builds primary key(castle_name, build_name)
);

--Jednostki: metawiedza
create table Unit(
    unit_name varchar(50) primary key,
    castle_name varchar(50),
    id_resources int not null,
    constraint fk_idresu foreign key(id_resources) references Resources(id_resource),
    constraint fk_castleu foreign key(castle_name) references Castles(castle_name)
);

--Punkt na mapie: konstruowane na początku, zależnie od widzimisię usera
create table Point_on_map(
    x int,
    y int,
    constraint pk_point primary key(x, y)
);

--Gracze: modyfikowane przez usera
create table Player(
    color varchar(50) primary key
);

--Bohater: modyfikowane przez usera
create table Hero(
    name varchar(50) primary key,
    color varchar(50) not null,
    id_army int unique not null,
    constraint fk_playh foreign key(color) references player(color)
);

--Armia: modyfikowana przez usera
create table Army(
    x int not null,
    y int not null,
    hero_name varchar(50) unique,
    id_army serial primary key,
    constraint fk_armyxy foreign key(x, y) references point_on_map(x, y),
    constraint fk_tohero foreign key(hero_name) references hero(name)
);
--Klucz obcy w obie strony: a do b, b do a
alter table hero add constraint fk_toarmy foreign key(id_army) references army(id_army);

--Połączenie armii: tabela modyfikowana przez usera, przy czym user modyfikuje ją modyfikując relację army
create table Army_connect(
	id_army int,
	position uint check(position>0 and position<8), 
	unit_name varchar(50) not null,
	number_of_units uint default 1 check(number_of_units>0),
	constraint fk_armycon foreign key(id_army) references Army(id_army),
	constraint fk_unit_from_army foreign key(unit_name) references Unit(unit_name),
	constraint pk_army_connect primary key(id_army, position)
);

--Konkretny zamek na mapie: modyfikowany przez usera
create table Castle_on_map(
	x int, 
	y int,
	color varchar(50),
	castle varchar(50) not null,
	constraint pk_castle_on_map primary key(x, y),
	constraint fk_castle_map_point foreign key(x, y) references point_on_map(x, y),
	constraint fk_castle_merge foreign key(castle) references Castles(castle_name),
	constraint fk_to_player foreign key(color) references Player(color)
);

--Budynek w zamku na mapie: też modyfikowany przez usera
create table Building_in_castle_on_map(
	x int, 
	y int,
	build_name varchar(50),
	castle varchar(50),
	constraint pk_build_in_castle_on_map primary key(x, y, build_name, castle),
	constraint fk_castle_build_map foreign key(castle, build_name) references Castle_building(castle_name, build_name),
	constraint fk_xy_place foreign key(x, y) references Castle_on_map(x, y)
);

--Wstawienie do mapy punktów : przepisać na procedurę po argumentach width, height
do $$
declare
	i integer:=0;
	j integer:=0;
begin
	loop
		exit when i>150;
		loop
			exit when j>150;
			insert into point_on_map values(i, j);
			j:=j+1;
		end loop;
		j:=0;
		i:=i+1;
	end loop;
end $$;


--budynek w zamku - wyzwalacz sprawdzający, czy zamki się pokrywają
create or replace function build_castle_trigger()
	returns trigger as
$$
declare
	cs1 varchar(50);
	cs2 varchar(50);
begin
	select castle into cs1
	from Castle_on_map
	where Castle_on_map.x=new.x and Castle_on_map.y=new.y;
	if cs1<>new.castle then
		raise exception 'You merged incorrect types of castle!';
	end if;
	return new;
end;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

create trigger build_castle_correct
	before insert or update
	on building_in_castle_on_map
	for each row
	execute procedure build_castle_trigger();




--Dodanie referencji do relacji army:
create or replace function update_reference_hero_army()
	returns trigger as
$$	
begin
	update army set hero_name=new.name where new.id_army=id_army;
	return new;
end;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

create trigger refupdate_hero_army_trig
	after insert or update
	on hero
	for each row
	execute procedure update_reference_hero_army();



--Ograniczenie do 2 armii na punkt
create or replace function two_armies()
	returns trigger as
$$
declare
	kappa int:=0;
begin
	select count(*) into kappa
	from army
	where x=new.x and y=new.y;
	if kappa>1 then
		raise exception 'There are already two armies on this point!';
	end if;
	return new;
end;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

create trigger dual_army_checker
	before insert or update of x, y
	on army
	for each row
	execute procedure two_armies();

--metawiedza
insert into Resources values(1000, 0, 0, 0, 0, 0, 0);
insert into Resources values(1021, 0, 0, 0, 0, 0, 0);
insert into Resources values(1021, 3, 0, 0, 0, 0, 0);
insert into Player values('red');
insert into Player values('blue');
insert into Player values('green');
insert into Castles values('rampart');
insert into Castles values('inferno');
insert into castle_building values('Kapitol', 'rampart', 2);
insert into castle_building values('Kapitol', 'inferno', 2);
insert into castle_on_map values(32,23,null,'rampart');
insert into unit values('Unicorn', 'rampart', 3);
insert into unit values('Devil', 'inferno', 2);


select *
from Resources;
