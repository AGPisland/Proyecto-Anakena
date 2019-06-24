'''
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
    session.pop('rol', None)
    return redirect(url_for('index')) 
'''