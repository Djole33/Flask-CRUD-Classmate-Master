from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    surname = db.Column(db.String(20), unique=True, nullable=False)
    indeks = db.Column(db.String(6), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Classmate %r>' % self.id
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        classmate_name = request.form['name']
        classmate_surname = request.form['surname']
        classmate_indeks = request.form['indeks']
        classmate_phone = request.form['phone']
        new_classmate = Todo(name=classmate_name, surname=classmate_surname, indeks=classmate_indeks, phone=classmate_phone)

        try:
            db.session.add(new_classmate)
            db.session.commit()
            return redirect('/')
        except Exception as e: 
            print(f"An error occurred: {e}")
        
    classmates = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', clasmates=classmates)
   
@app.route('/delete/<int:id>')
def delete(id):
    classmate_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(classmate_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that classmate'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    classmate = Todo.query.get_or_404(id)

    if request.method == 'POST':
        try:
            classmate.name = request.form['name']
            classmate.surname = request.form['surname']
            classmate.indeks = request.form['indeks']
            classmate.phone = request.form['phone']
            
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'There was an issue updating your classmate: {e}'

    else:
        return render_template('update.html', classmate=classmate)

    

if __name__ == '__main__':
    app.run(debug=True)
