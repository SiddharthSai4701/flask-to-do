# from datetime import datetime
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=db.datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    # content is the id of the form tag defined in index.html
    task_content = request.form['content']
    new_task = Todo(content=task_content)
    
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return "Something went wrong"
  else:
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)