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


@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
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
        print(data[0], data[1])
        return render_template("index.html")

    return 'You are not logged in'


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