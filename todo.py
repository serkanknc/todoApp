from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/monster/Desktop/TodoApp/todo.db"
db = SQLAlchemy(app)

#! todo class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

#! index home
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

#! todo update
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))
#! todo delete
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

#! add todo
@app.route("/add",methods= ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title=title,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
