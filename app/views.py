from app import app
from flask import render_template,request,redirect, session, Flask, url_for, escape
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s" %
                        ('anakena', 'alonsogjp', 'Alon'))

cur = conn.cursor()



@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
	if request.method == 'POST':
		comentario =  request.form['comentarios']
	
	return render_template("post.html") 

@app.route('/comentario/<id>', methods=['GET', 'POST'])
def comentario(id):
	if request.method == 'POST':
		pass

	return render_template("comentario.html") 

@app.route('/borrar/<id>', methods=['GET', 'POST'])
def borrar(id):
	return  redirect(request.referrer)

@app.route('/agregar_ficha_secretaria', methods=['GET','POST'])
def agregar_ficha_secretaria():
    if request.method == 'POST':
        print('Sacar las variables y cargarlo en la base de datos')
        pass
    else:
        print('es un metodo get y hay que entregar la pagina')


@app.route('/decretos', methods=['GET', 'POST'])
def decretos():
    if request.method == 'GET':
        print('entregar los decretos asignados en la base de datos')




app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/index.html')
def index():
    if 'username' in session:
        print(session)
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



@app.route('/curso.html', methods=['GET', 'POST'])
def curso():
    print('ACA!!!')
    if request.method == 'POST':
        decreto=request.form['valor']
        print(decreto)
        sql="""select curso from fichas where decreto='%s' group by curso; """%decreto
        cur.execute(sql)
        cursos=cur.fetchall()
        data=[]
        for i in cursos:
            i=str(i)
            data.append(i[2:len(i)-3])
        print(data)
        return render_template("cursos.html",valor=data )

@app.route('/lista_alumnos.html', methods=['GET', 'POST'])
def lista_de_alumnos():
    print('ACA!!!')
    if request.method == 'POST':
        curso=request.form['valor']
        print(curso)
        sql="""select nombre, apellido, rutentero, digitorut from fichas where curso='%s'; """%curso
        cur.execute(sql)
        cursos=cur.fetchall()
        data=[]
        for i in cursos:
            i=str(i)
            i=i[2:len(i)-1]
            data.append(i)
            print(i,'\n')
        cursos=[]
        rutas=[]
        for i in data:
            aux=""
            aux2=""
            for j in i:
                if j is "'" or j is ",":
                    pass
                else:
                    try:
                        j=int(j)
                        aux2=aux2+str(j)
                    except:
                        pass
                        aux=aux+j
            aux2=aux2[:len(aux2)-2]+'-'+aux2[len(aux2)-1]
            rutas=[aux,aux2]
            cursos.append(rutas)
        data=cursos
        del cursos
        print(data)
        return render_template("lista_alumnos.html",valor=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        session['username'] = request.form['username']
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