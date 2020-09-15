from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/mrnet/Desktop/TodoApp/todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

@app.route("/add",methods=["GET","POST"])
def add():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        content = Todo(title = request.form.get("content"),complete = False)
        db.session.add(content)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    delete_todo = Todo.query.filter_by(id = id).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<string:id>")
def update(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)