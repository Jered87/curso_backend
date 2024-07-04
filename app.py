from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

print(f"Template directory: {template_dir}")

print(template_dir)


app = Flask(__name__, template_folder = template_dir)


#Rutas de la aplicacion
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT id, username, name, password FROM users")
    myresult = cursor.fetchall()
    #convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames,record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la base de datos
@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if username and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users Where id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE users SET username = %s, name = %s, password = %s Where id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)