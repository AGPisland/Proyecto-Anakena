
import random
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s" %
                        ('anakena', 'alonsogjp', 'Alon'))

cur = conn.cursor()

sql = """DROP table fichas"""
try:
    #cur.execute(sql)
	pass
except:
    pass


sql = """create table fichas (id serial PRIMARY KEY, decreto varchar(20), curso varchar(20), nombre varchar(40), apellido varchar(40), rutentero int, digitorut varchar(2));"""
cur.execute(sql)

lista_de_decretos = ['DECRETO1', 'DECRETO2']
lista_de_curso_decreto1 = ['1-A', '2-A', '2-B', '3-A']
# 12    #10   #10     #10
lista_de_curso_decreto2 = ['Diferencial-1', 'Diferencial-2']
# 4             #4
lista_de_nombres = ['MARIA', 'MARIA CARMEN', 'JOSEFA', 'ISABEL', 'MARIA DOLORES', 'CARMEN', 'FRANCISCA', 'MARIA PILAR', 'DOLORES', 'MARIA JOSE', 'ANTONIA', 'ANA', 'MARIA ISABEL', 'MARIA ANGELES', 'PILAR', 'ANA MARIA', 'FRANCISCO JAVIER', 'RAFAEL', 'DANIEL', 'JUAN JOSE', 'LUIS', 'PABLO', 'JUAN ANTONIO',
                    'JOAQUIN', 'SERGIO', 'FERNANDO', 'JUAN CARLOS', 'ANDRES', 'JOSE MANUEL', 'JOSE MARIA', 'RAMON', 'RAUL', 'ALBERTO', 'ENRIQUE', 'ALVARO', 'VICENTE', 'EMILIO', 'FRANCISCO JOSE', 'DIEGO', 'JULIAN', 'JORGE', 'ALFONSO', 'ADRIAN', 'RUBEN', 'SANTIAGO', 'IVAN', 'JUAN MANUEL', 'PASCUAL', 'JOSE MIGUEL', 'MARIO']
lista_de_apellidos = ['GARCIA', 'MARTINEZ', 'LOPEZ', 'SANCHEZ', 'GONZALEZ', 'GOMEZ', 'FERNANDEZ', 'MORENO', 'JIMENEZ', 'PEREZ', 'RODRIGUEZ', 'NAVARRO', 'RUIZ', 'DIAZ', 'SERRANO', 'HERNANDEZ', 'MUÑOZ', 'SAEZ', 'ROMERO', 'RUBIO', 'ALFARO', 'MOLINA', 'LOZANO', 'CASTILLO',
                      'PICAZO', 'ORTEGA', 'MORCILLO', 'CANO', 'MARIN', 'CUENCA', 'GARRIDO', 'TORRES', 'CORCOLES', 'GIL', 'ORTIZ', 'CALERO', 'VALERO', 'CEBRIAN', 'RODENAS', 'ALARCON', 'BLAZQUEZ', 'NUÑEZ', 'PARDO', 'MOYA', 'TEBAR', 'REQUENA', 'ARENAS', 'BALLESTEROS', 'COLLADO', 'RAMIREZ']
lista_ruts = []


def remove(lista):
    va = random.choice(lista)
    lista.remove(va)
    return va


for i in range(4):
    rut = random.randint(22001944, 24555222)
    while rut not in lista_ruts:
        rut = random.randint(22001944, 24555222)
        lista_ruts.append(rut)
        digit = str(random.randint(0, 9))

    sql = """  insert into fichas (decreto, curso, nombre, apellido, rutentero, digitorut) values ('%s','%s','%s','%s',%s,'%s');""" % (
        lista_de_decretos[1], lista_de_curso_decreto2[0], remove(lista_de_nombres), remove(lista_de_apellidos), rut, digit)

    print(sql)
    cur.execute(sql)

for i in range(4):
    rut = random.randint(22001944, 24555222)
    while rut not in lista_ruts:
        rut = random.randint(22001944, 24555222)
        lista_ruts.append(rut)
        digit = str(random.randint(0, 9))

    sql = """  insert into fichas (decreto, curso, nombre, apellido, rutentero, digitorut) values ('%s','%s','%s','%s',%s,'%s');""" % (
        lista_de_decretos[1], lista_de_curso_decreto2[1], remove(lista_de_nombres), remove(lista_de_apellidos), rut, digit)

    print(sql)
    cur.execute(sql)

for i in range(12):
    rut = random.randint(22001944, 24555222)
    while rut not in lista_ruts:
        rut = random.randint(22001944, 24555222)
        lista_ruts.append(rut)
        digit = str(random.randint(0, 9))

    sql = """  insert into fichas (decreto, curso, nombre, apellido, rutentero, digitorut) values ('%s','%s','%s','%s',%s,'%s');""" % (
        lista_de_decretos[0], lista_de_curso_decreto1[0], remove(lista_de_nombres), remove(lista_de_apellidos), rut, digit)

    print(sql)
    cur.execute(sql)

for i in range(10):
    rut = random.randint(22001944, 24555222)
    while rut not in lista_ruts:
        rut = random.randint(22001944, 24555222)
        lista_ruts.append(rut)
        digit = str(random.randint(0, 9))

    sql = """  insert into fichas (decreto, curso, nombre, apellido, rutentero, digitorut) values ('%s','%s','%s','%s',%s,'%s');""" % (
        lista_de_decretos[0], lista_de_curso_decreto1[1], remove(lista_de_nombres), remove(lista_de_apellidos), rut, digit)

    print(sql)
    cur.execute(sql)

for i in range(10):
    rut = random.randint(22001944, 24555222)
    while rut not in lista_ruts:
        rut = random.randint(22001944, 24555222)
        lista_ruts.append(rut)
        digit = str(random.randint(0, 9))

    sql = """  insert into fichas (decreto, curso, nombre, apellido, rutentero, digitorut) values ('%s','%s','%s','%s',%s,'%s');""" % (
        lista_de_decretos[0], lista_de_curso_decreto1[2], remove(lista_de_nombres), remove(lista_de_apellidos), rut, digit)

    print(sql)
    cur.execute(sql)

for i in range(10):
    rut = random.randint(22001944, 24555222)
    while rut not in lista_ruts:
        rut = random.randint(22001944, 24555222)
        lista_ruts.append(rut)
        digit = str(random.randint(0, 9))

    sql = """  insert into fichas (decreto, curso, nombre, apellido, rutentero, digitorut) values ('%s','%s','%s','%s',%s,'%s');""" % (
        lista_de_decretos[0], lista_de_curso_decreto1[3], remove(lista_de_nombres), remove(lista_de_apellidos), rut, digit)

    print(sql)
    cur.execute(sql)

conn.commit()
cur.close()
conn.close()

'''

sql = """
insert into categorias (nombre) values ('Tecnologia '),('Video Juegos '),('Geek'),
('Cine'),('Mundo Marvel');
"""
cur.execute(sql)




'''
