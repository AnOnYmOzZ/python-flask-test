from ast import Pass
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# //// is an absolute path
# /// is a relative path

db = SQLAlchemy(app) #< initialize database 

class Todo (db.Model):  #inherit the db.Model class, it 
    id = db.Column(db.Integer, primary_key=True) #holds id for each entry 
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) #set automatically with the time and date the entry was mad 

    def __repr__(self): 
        return '<Task %r>' % self.id


@app.route('/',methods=["POST","GET"])
def index(): 
    #C in CRUD for Create: POST
    if request.method == 'POST': 
        #create new entry and put data in database
        task_content = request.form['content'] #id of the form 
        new_task = Todo(content=task_content)#content is a member of Todo
        
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: 
            return 'An error occured while POSTING (creating)'
    
    #R in CRUD for READ: 'GET' 
    else: 
        tasks = Todo.query.order_by(Todo.date_created).all() #you can do .first() to grab just the first 
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id): 
    #D in CRUD for DELETE
    task_to_delete = Todo.query.get_or_404(id)
    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except: 
        return 'There was a problem DELETING'

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id): 
    #U in CRUD for UPDATE
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST': 
        task.content = request.form['content'] #id of the form 
        try: 
            db.session.commit()
            return redirect('/')
        except: 
            return 'There was a problem DELETING'
    else : 
        return render_template('update.html',task=task)

# @app.route('/hell')
# def index_hell(): 
#     return "hello nig"

if __name__ == "__main__": 
    app.run(debug=True) 


