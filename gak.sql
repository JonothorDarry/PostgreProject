--PostgreSQL 9.6
--';' is a delimiter

--Wyrzucanie starych tabel
drop function firepower(text);
drop function map_creator(uint, uint);

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
    attack uint,
    defence uint,
    health uint,
    speed uint,
    minimum_damage uint,
    maximum_damage uint,
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
    attack uint,
    defence uint,
    might uint,
    wisdom uint,
    constraint fk_playh foreign key(color) references player(color) on update cascade
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
	constraint fk_to_player foreign key(color) references Player(color) on update cascade
);

--Budynek w zamku na mapie: też modyfikowany przez usera
create table Building_in_castle_on_map(
	x int, 
	y int,
	build_name varchar(50),
	castle varchar(50),
	constraint pk_build_in_castle_on_map primary key(x, y, build_name, castle),
	constraint fk_castle_build_map foreign key(castle, build_name) references Castle_building(castle_name, build_name),
	constraint fk_xy_place foreign key(x, y) references Castle_on_map(x, y) on update cascade
);

--Wstawienie do mapy punktów : przepisać na procedurę po argumentach width, height
create or replace function map_creator(x1 uint, x2 uint)
	returns void as
$$
declare
	i integer:=1;
	j integer:=1;
begin
	loop
		exit when i>x1;
		loop
			exit when j>x2;
			insert into point_on_map values(i, j);
			j:=j+1;
		end loop;
		j:=1;
		i:=i+1;
	end loop;
end $$
language plpgsql volatile;

--Ścięcie gracza, usunięcie wszystkich jego bohaterów i armii, zmiana wszystkich jego miast na neutralne(color=NULL)
create or replace procedure player_slayer(x1 text)
	language plpgsql as
$$
begin
	delete from army_connect
	where id_army in(
		select a.id_army
		from army a
		left join hero h on h.id_army=a.id_army
		where h.color=x1
	);
	
	alter table hero disable trigger all;
	alter table army disable trigger all;
	
	delete from army
	where id_army in(
		select id_army
		from hero
		where color=x1
	);
	
	delete from hero
	where color=x1;

	alter table hero enable trigger all;
	alter table army enable trigger all;

	update castle_on_map
	set color=null
	where color=x1;
	
	delete from player
	where color=x1;

end $$;

create or replace function firepower(x1 text)
	returns table(max_d bigint, min_d bigint, att bigint, def bigint, health bigint, speed bigint) as
$$
begin
	return query
	select sum(a.number_of_units*u.maximum_damage), sum(a.number_of_units*u.minimum_damage), sum(a.number_of_units*u.attack), sum(a.number_of_units*u.defence),
   		sum(a.number_of_units*u.health), sum(a.number_of_units*u.speed)
	from unit u
	left join army_connect a on a.unit_name=u.unit_name
	left join army ar on ar.id_army=a.id_army
	left join hero h on h.id_army=ar.id_army
	where h.color=x1;
end $$
LANGUAGE plpgsql VOLATILE;




--budynek w zamku - wyzwalacz sprawdzający, czy zamki się pokrywają
create or replace function build_castle_trigger()
	returns trigger as
$$
declare
	cs1 varchar(50);
	cs2 varchar(50);
begin
	select castle into cs1
	from Castle_on_map c
	where c.x=new.x and c.y=new.y;
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




--Wyzwalcz czyszczący budynki po usunięciu/zmianie typu zamku
create or replace function build_dissolver()
	returns trigger as
$$
declare
	cs1 varchar(50);
	cs2 varchar(50);
begin
	if new is null or old.castle<>new.castle then
		delete from Building_in_castle_on_map b	where b.x=old.x and b.y=old.y;
	end if;
	if new is null then
		return old;
	end if;
	return new;
end;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

create trigger build_slayer
	before delete or update
	on castle_on_map
	for each row
	execute procedure build_dissolver();


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


--Usunięcie referencji z relacji army:
create or replace function delete_reference_hero_army()
	returns trigger as
$$	
begin
	update army set hero_name=NULL where old.id_army=id_army;
	return old;
end;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

create trigger refdelete_hero_army_trig
	before delete
	on hero
	for each row
	execute procedure delete_reference_hero_army();


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

/*
DO $$ BEGIN
    perform map_creator(150, 150);
END $$;

--firepower test
insert into castle_on_map values(50, 52, 'red', 'inferno');
insert into castle_on_map values(50, 57, 'green', 'inferno');
insert into castle_on_map values(50, 59, 'blue', 'inferno');
insert into castle_on_map values(57, 52, 'red', 'inferno');
insert into army values(12, 35, null);
insert into army values(12, 36, null);
insert into army values(12, 37, null);

insert into army_connect values(1, 1, 'Unicorn', 10);
insert into army_connect values(2, 2, 'Devil', 20);
insert into army_connect values(3, 7, 'Devil', 1);

insert into hero values('Jonasz', 'red', 1);
insert into hero values('Ozjasz', 'blue', 2);
insert into hero values('Elizeusz', 'red', 3);

	


DO $$ 
declare
	x1 bigint;
	x2 bigint;
	x3 bigint;
	x4 bigint;
	x5 uint;
	x6 uint;
BEGIN
 	select max_d, min_d, att, def into x1, x2, x3, x4
	from firepower('red');
	raise notice 'Value: %', x1;

	select x into x1
	from army
	where y=36;
	raise notice 'Value: %', x1;
END $$;


DO $$ BEGIN
	call player_slayer('red');
END $$;


select *
from Resources;
*/
