import json
from app import app
from flask import render_template, request, redirect, session, Flask, url_for, escape
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s" %
                        ('anakena', 'alonsogjp', 'Alon'))

cur = conn.cursor()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/index.html')
def index():
    if 'rol' in session:
        print('sesion: ',session)
        sql="""select decreto from fichas group by(decreto);"""
        cur.execute(sql)
        data=cur.fetchall()
        print(data)
        decretouno=str(data[0])
        decretodos=str(data[1])
        print(decretodos[2:len(decretouno)-3],decretouno)
        decretouno=decretouno[2:len(decretouno)-3]
        decretodos=decretodos[2:len(decretodos)-3]
        data=[decretouno,decretodos]
        print(data)
        return render_template("index.html",valor=data )
    return 'You are not logged in'

@app.route('/curso', methods=['GET', 'POST'])
def curso():
    #PUEDEN ACCEDER TODOS LOS ROLES!
    print('ACA!!!')
    if request.method == 'POST':
        decreto = request.form['valor']
        print(decreto)
        sql = """select curso from fichas where decreto='%s' group by curso; """ % decreto
        cur.execute(sql)
        cursos = cur.fetchall()
        data = []
        for i in cursos:
            i = str(i)
            data.append(i[2:len(i)-3])
        print(data)
        return render_template("cursos.html", valor=data)

@app.route('/lista_alumnos', methods=['GET', 'POST'])
def lista_de_alumnos():
    #AQUI DIFIEREN LOS PERMISOS POR ROLES! 
    #LA SECRETARIA SOLO PUEDE TENER EL HTML QUE TENGA LAS PROPIEDADES DE AGREGAR, CORREJIR, Y VER
    #LA DIRECTORA SOLO PUEDE TENER EL HTML QUE TENGA REVISAR, TERMINAR, VER
    #LA PROFESORA SOLO PUEDE VER!
    print('ACA!!! lista de alumnos')
    if request.method == 'POST':
        curso = request.form['valor']
        print(curso)
        sql = """select nombre, apellido, rutentero, digitorut, estado from fichas where curso='%s'; """ % curso
        cur.execute(sql)
        cursos = cur.fetchall()
        data = []
        for i in cursos:
            i = str(i)
            i = i[2:len(i)-1]
            data.append(i)
            print(i, '\n')
        cursos = []
        rutas = []
        l=True
        for i in data:
            aux = ""
            aux2 = ""
            aux3=""   
            for j in i:
                if j is "'" or j is ",":
                    pass
                else:
                    try:
                        j = int(j)
                        aux2 = aux2+str(j)
                        l=False
                    except:
                        pass
                        if l is False:
                            #terminamos los numeros
                            aux3=aux3+j
                        else:
                            aux = aux+j
            l=True
            aux2 = aux2[0:len(aux2)-1]+'-'+aux2[len(aux2)-1]
            rutas = [aux, aux2, aux3]
            cursos.append(rutas)
        data = cursos
        del cursos
        print(data)

        #HASTA ACA TENEMOS LA LISTA DE LOS ALUMNOS, EN EL VALOR DATA, + FALTA AGREGAR EL JSON Y EL ESTADO!
        if session['rol']==roles[0]:
            #directora
            return render_template("lista_alumnos_secretaria.html", valor=data)
        else:
            if session['rol'] is roles[1]:
                #secretaria
                return render_template("lista_alumnos_secretaria.html", valor=data)
            else:
                if session['rol'] is roles[2]:
                    #profesora
                    return render_template("lista_alumnos_secretaria.html", valor=data)
                else:
                    return 'you not permission'
        

@app.route('/ver_ficha', methods=['GET', 'POST'])
def prueba():
    print('ACA!!! ver ficha')
    if request.method == 'POST':
        key = request.form['key']
        key=key[0:len(key)-2]
        sql = """select fichaj from fichas where rutentero=%s; """ % int(key)
        print(sql)
        cur.execute(sql)
        filejson = cur.fetchall()
        dict=filejson[0][0]
        #HASTA ACA TENEMOS LA LISTA DE LOS ALUMNOS, EN EL VALOR DATA, + FALTA AGREGAR EL JSON Y EL ESTADO!
        return render_template("ver_ficha.html", jason=dict)

@app.route('/nuevaficha', methods=['GET', 'POST'])
def nuevaficha():
    print('aca!!! ficharevision')
    if request.method == 'POST':
        print('nuevo fichas!!!!!!')
        return render_template("nueva_ficha.html")

@app.route('/ficha_revision', methods=['GET', 'POST'])
def ficharevision():
    print('aca!!! ficharevision')
    if request.method == 'POST':
        a = request.form['Pnombre']
        b = request.form['Snombre']
        c = request.form['apellidoP']
        d = request.form['apellidoM']
        e = request.form['edad']
        f = request.form['nacimientoF']
        g = request.form['nacional']
        h = request.form['rut']
        j = request.form['dig']
        k = request.form['dom']
        q = request.form['com']
        w = request.form['nombrePadre']
        r = request.form['nacionalPadre']
        t = request.form['rutPadre']
        y = request.form['edadPadre']
        u = request.form['celPadre']
        i = request.form['corPadre']
        o = request.form['nombreMadre']
        p = request.form['nacionalMadre']
        z = request.form['rutMadre']
        x = request.form['edadMadre']
        v = request.form['celMadre']
        n = request.form['corMadre']
        m = request.form['celEmerg']
        aa = request.form['ApodEme']
        vv = request.form['salud']
        vvv = request.form['seguro']
        # print((a,b,c,d,e,f,g,h,j,k,q,w,e,r,t,y,u,i,o,p,z,x,v,n,m,aa,vv,vvv))
        jsonfile = """{"Primer Nombre":"%s","Segundo Nombre":"%s","Apellido Padre":"%s","Apellido Madre":"%s","Edad":"%s","Fecha de nacimiento":"%s","Nacionalidad":"%s","RUT Alumno":"%s","Digito Verificador":"%s","Domicilio":"%s","Comuna":"%s","Nombre del padre":"%s","Nacionalidad":"%s","RUT Padre":"%s","Edad":"%s","Celular":"%s","Correo":"%s","Nombre de la Madre":"%s","Nacionalidad":"%s","RUT Madre":"%s","Edad":"%s","Celular":"%s","Correo":"%s","Antecedentes Medicos Importantes":"%s","Fono de emergencias":"%s","Nombre Apoderado":"%s","Servicio de Salud del Estudiante":"%s","Seguro Medico":"%s" }""" % (
            a, b, c, d, e, f, g, h, j, k, q, w, e, r, t, y, u, i, o, p, z, x, v, n, m, aa, vv, vvv)
        jsonn = json.loads(jsonfile)
        print(jsonn)

        return jsonfile

roles=['directora', 'secretaria', 'profesora']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        role=request.form['username']
        if role in roles:
            session['rol'] = role
            return redirect(url_for('index'))
        

    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index')) 