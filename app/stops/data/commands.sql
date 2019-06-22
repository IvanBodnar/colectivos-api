-- copy psql. Connect through localhost to the postgres container from local machine.
--\copy stops(tipo,calle,numero,entre1,entre2,lineas,dir_norm,metrobus,stop_desc,x,y,geom,geom_98334) from '/home/ivan/Projects/real/python/django/colectivos-api/app/stops/data/paradas-de-colectivo.csv' delimiter ';' encoding 'latin3' csv header

-- Populate geom columns
update stops s
set geom = st_setsrid(st_makepoint(s.x, s.y), 4326)
from (select id, x, y from stops) as xy
where s.id = xy.id;

update stops s
set geom_98334 = st_transform(st_setsrid(st_makepoint(s.x, s.y), 4326), 98334)
from (select id, x, y from stops) as xy
where s.id = xy.id;

select *
from stops;
