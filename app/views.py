import json
from psycopg2.extras import Json
from flask import render_template, request, redirect, session, Flask, url_for, escape
import psycopg2
from app import app, login_manager
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user
from app.models import users, User, get_user
from flask_login import login_required
from werkzeug.urls import url_parse


conn = psycopg2.connect("dbname=%s user=%s password=%s" %
                        ('anakena', 'alonsogjp', 'Alon'))

cur = conn.cursor()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/index')
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
        return render_template("index.html",valor=data)

    return redirect(url_for('logout')) 

@app.route('/curso', methods=['GET', 'POST'])
def curso():
    #PUEDEN ACCEDER TODOS LOS ROLES!
    print('ACA!!!')
    if request.method == 'POST':
        decreto = request.form['decreto']
        print(decreto)
        sql = """select curso from fichas where decreto='%s' group by curso; """ % decreto
        cur.execute(sql)
        cursos = cur.fetchall()
        data = []
        for i in cursos:
            i = str(i)
            data.append(i[2:len(i)-3])
        print(data)
        return render_template("cursos.html", valor=data, decreto=decreto)

@app.route('/lista_alumnos', methods=['GET', 'POST'])
def lista_de_alumnos():
    #AQUI DIFIEREN LOS PERMISOS POR ROLES! 
    #LA SECRETARIA SOLO PUEDE TENER EL HTML QUE TENGA LAS PROPIEDADES DE AGREGAR, CORREJIR, Y VER
    #LA DIRECTORA SOLO PUEDE TENER EL HTML QUE TENGA REVISAR, TERMINAR, VER
    #LA PROFESORA SOLO PUEDE VER!
    print('ACA!!! lista de alumnos')
    if request.method == 'POST':
        curso = request.form['curso']
        decreto = request.form['decreto']
        print(curso, decreto)
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
        

        #HASTA ACA TENEMOS LA LISTA DE LOS ALUMNOS, EN EL VALOR DATA, + FALTA AGREGAR EL JSON Y EL ESTADO!
        if session['rol']==roles[0]:
            #directora
            return render_template("lista_alumnos_directora.html", valor=data, curso=curso, decreto=decreto)
        else:
            if session['rol'] == roles[1]:
                #secretaria
                aux=data
                data=[]
                for i in aux:
                    if i[2] != '  TERMINADO':
                        data.append(i)  

                return render_template("lista_alumnos_secretaria.html", valor=data, curso=curso, decreto=decreto)
            else:
                if session['rol'] == roles[2]:
                    #profesora
                    print(data)
                    aux=data
                    data=[]
                    for i in aux:
                        if i[2] == '  APROBADO':
                            data.append(i)

                    return render_template("lista_alumnos_profesora.html", valor=data, curso=curso, decreto=decreto)
                else:
                    return 'you not permission'

@app.route('/ver_ficha', methods=['GET', 'POST'])
def prueba():
    print('ACA!!! ver ficha')
    #no importa el rol aca, todos pueden ver la ficha!
    if request.method == 'POST':
        key = request.form['key']
        curso = request.form['curso']
        decreto = request.form['decreto']
        key=key[0:len(key)-2]
        sql = """select fichaj from fichas where rutentero=%s; """ % int(key)
        print(sql)
        cur.execute(sql)
        filejson = cur.fetchall()
        dict=filejson[0][0]
        #HASTA ACA TENEMOS LA LISTA DE LOS ALUMNOS, EN EL VALOR DATA, + FALTA AGREGAR EL JSON Y EL ESTADO!
        return render_template("ver_ficha.html", jason=dict,  curso=curso, decreto=decreto)

@app.route('/nuevaficha', methods=['GET', 'POST'])
def nuevaficha():
    print('aca!!! ficharevision')
    if request.method == 'POST':
        curso = request.form['curso']
        decreto = request.form['decreto']
        print('nuevo fichas!!!!!!')
        return render_template("nueva_ficha.html", curso=curso, decreto=decreto)

@app.route('/eliminar_secre', methods=['GET', 'POST'])
def eliminar_secre():
    print('aca!!! eliminar FICHA SSI LO ESTA EN ESTADO DE RECHAZADO')
    if request.method == 'POST':
        key = request.form['key']
        curso = request.form['curso']
        decreto = request.form['decreto']
        key=key[0:len(key)-2]
        sql = """select estado from fichas where rutentero=%s; """ % int(key)
        print(sql)
        cur.execute(sql)
        estado=cur.fetchone()
        print(estado)
        if estado[0] == 'RECHAZADA' or estado[0] == 'BORRADOR':
            print('se procede a borrar ficha')
            sql="""delete from fichas where rutentero=%s; """ % int(key)
            print(sql)
            cur.execute(sql)
            conn.commit()
            return render_template("borrado_secre.html", curso=curso, decreto=decreto)
        else:
            print('es otra cosa el estado!')
            return render_template("error_borrado_secre.html", curso=curso, decreto=decreto)
        
@app.route('/reparar', methods=['GET', 'POST'])
def reparar():
    print('ACA!!! reparar')
    #no importa el rol aca, todos pueden ver la ficha!
    if request.method == 'POST':
        key = request.form['key']
        curso = request.form['curso']
        decreto = request.form['decreto']
        key=key[0:len(key)-2]
        sql = """select fichaj from fichas where rutentero=%s; """ % int(key)
        print(sql)
        cur.execute(sql)
        filejson = cur.fetchall()
        dict=filejson[0][0]
        #HASTA ACA TENEMOS LA LISTA DE LOS ALUMNOS, EN EL VALOR DATA, + FALTA AGREGAR EL JSON Y EL ESTADO!
        return render_template("reparar_ficha.html", jason=dict, curso=curso, decreto=decreto)

@app.route('/ficha_revision', methods=['GET', 'POST'])
def ficharevision():
    print('aca!!! ficharevision')
    if request.method == 'POST':
        curso = request.form['curso']
        decreto = request.form['decreto']
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
        json1 = """{"Primer Nombre":"%s","Segundo Nombre":"%s","Apellido Padre":"%s","Apellido Madre":"%s","Edad":"%s","Fecha de nacimiento":"%s","Nacionalidad":"%s","RUT Alumno":"%s","Digito Verificador":"%s","Domicilio":"%s","Comuna":"%s","Nombre del padre":"%s","Nacionalidad":"%s","RUT Padre":"%s","Edad":"%s","Celular":"%s","Correo":"%s","Nombre de la Madre":"%s","Nacionalidad":"%s","RUT Madre":"%s","Edad":"%s","Celular":"%s","Correo":"%s","Antecedentes Medicos Importantes":"%s","Fono de emergencias":"%s","Nombre Apoderado":"%s","Servicio de Salud del Estudiante":"%s","Seguro Medico":"%s" }""" % (
            a, b, c, d, e, f, g, h, j, k, q, w, e, r, t, y, u, i, o, p, z, x, v, n, m, aa, vv, vvv)
        jsonn=json.loads(json1)
        json1=Json(jsonn)
        sql = """  insert into fichas (decreto, curso, nombre, apellido, rutentero, digitorut, estado, fichaj) values ('%s','%s','%s','%s',%s,'%s','%s', %s);""" % (
            decreto, curso, a+' '+b, c +' '+ d, h, j, 'BORRADOR', json1)
        print(sql)
        try:
            cur.execute(sql)
        except:
            conn.commit()    
            return render_template("envio_ficha_error.html", curso=curso, decreto=decreto)
        
        conn.commit()
        return render_template("envio_ficha_exito.html", curso=curso, decreto=decreto)

@app.route('/terminar', methods=['GET', 'POST'])
def termianardict():
    print('aca terminar ficha desde directora')
    if request.method == 'POST':
        key = request.form['key']
        curso = request.form['curso']
        decreto = request.form['decreto']
        key=key[0:len(key)-2]
        sql = """select estado from fichas where rutentero=%s; """ % int(key)
        print(sql)
        cur.execute(sql)
        estado=cur.fetchone()
        print(estado)
        if estado[0] == 'APROBADO':
            print('se procede a CAMBIAR EL ESTADO A TERMINADO DE LA  ficha')
            sql="""UPDATE fichas set estado = 'TERMINADO' where rutentero=%s; """ % int(key)
            print(sql)
            cur.execute(sql)
            conn.commit()
            return render_template("borrado_secre.html", curso=curso, decreto=decreto)
        else:
            print('es otra cosa el estado!')
            return render_template("error_borrado_secre.html", curso=curso, decreto=decreto)

roles=['directora', 'secretaria', 'profesora']




@app.route('/revisar', methods=['GET', 'POST'])
def revisardirectora():
    print('ACA!!! revisar directora')
    #no importa el rol aca, todos pueden ver la ficha!
    if request.method == 'POST':
        key = request.form['key']
        curso = request.form['curso']
        decreto = request.form['decreto']
        key=key[0:len(key)-2]
        sql = """select fichaj from fichas where rutentero=%s; """ % int(key)
        print(sql)
        cur.execute(sql)
        filejson = cur.fetchall()
        dict=filejson[0][0]
        #HASTA ACA TENEMOS LA LISTA DE LOS ALUMNOS, EN EL VALOR DATA, + FALTA AGREGAR EL JSON Y EL ESTADO!
        return render_template("revisar_ficha.html", jason=dict,  curso=curso, decreto=decreto, key=key)


@app.route('/aprobar', methods=['GET', 'POST'])
def aprobardirectora():
    print('ACA!!! aprobar directora')
    #no importa el rol aca, todos pueden ver la ficha!
    if request.method == 'POST':
        val = request.form['eva']
        key = request.form['key']
        curso = request.form['curso']
        decreto = request.form['decreto']
        if val == "aprobado":
            sql="""UPDATE fichas set estado = 'APROBADO' where rutentero=%s; """ % int(key)
            print(sql)
            cur.execute(sql)
            conn.commit()
            return render_template("aprobado.html", curso=curso, decreto=decreto)
        else:
            if val == "rechazado":
                sql="""UPDATE fichas set estado = 'RECHAZADA' where rutentero=%s; """ % int(key)
                print(sql)
                cur.execute(sql)
                conn.commit()
                return render_template("rechazado.html", curso=curso, decreto=decreto)



@app.route("/logout")
def logout():
    logout_user()
    return redirect( url_for( "login" ) )




@app.route( "/"  )
@app.route( "/login" , methods = [ 'GET' , 'POST' ] )
def login():
    print('login:=')
    if current_user.is_authenticated :
        print('lo=')
        return redirect( url_for( 'index' ) )

    form = LoginForm() 
    if form.validate_on_submit():
        print('lo=asd')
        user = get_user( form.email.data )
        password = form.password.data  

        if user is not None and user.check_password(password):
            print('lsadasdo=')
            login_user( user, remember = form.remember_me.data )
            next_page = request.args.get( "next" )

            if not next_page or url_parse( next_page ).netloc != "" :
                next_page = url_for( "index" )
        
            return redirect(next_page)

    return render_template ( "login.html" , title = "Ingreso", form = form )

@app.route("/signup", methods = [ 'GET', 'POST' ] )
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = SignUpForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data
        rol = form.rol.data

        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, email, password, rol)
        print (user)
        users.append(user)
        print (users)
        session['rol'] = rol
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template("signup.html", form=form)

@login_manager.user_loader
def load_user( user_id ) :
    for user in users:
        if user.id == int ( user_id ) :
            return user
        
    return None
    


