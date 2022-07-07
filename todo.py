from flask import Flask,render_template,redirect,url_for,request,flash

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/efeca/Desktop/python_projects/todo-app-flask/todo.db"

db = SQLAlchemy(app)

# Table Class for ORM
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

# Main Page
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

# Add Todo
@app.route("/add",methods=["POST"])
def add():
    title = request.form.get("title")
    newTodo = Todo(title = title, complete = False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

# Complete/Not Complete Todo
@app.route("/complete/<string:id>")
def complete(id):
    status = Todo.query.filter_by(id = id).first()
    status.complete = not status.complete
    db.session.commit()  
    return redirect(url_for("index"))

# Delete Todo
@app.route("/delete/<string:id>")
def delete(id):
    deleteTodo = Todo.query.filter_by(id = id).first()
    db.session.delete(deleteTodo)
    db.session.commit()
    return redirect(url_for("index"))
   
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
