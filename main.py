from datetime import datetime
from pytz import timezone
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

date = datetime.now(timezone('UTC'))
date_now = date.astimezone(timezone('Asia/shanghai')).strftime('%d-%m-%Y')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
Bootstrap(app)
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(500), nullable=False)
    bd_color = db.Column(db.String(8), default="#000", nullable=False)
    bd_outline = db.Column(db.String(4), default="1px", nullable=False)
    done_line = db.Column(db.String(20), default="none", nullable=False)
    done_display = db.Column(db.String(20), default="flex", nullable=False)


db.create_all()


@app.route("/")
def main():
    all_notes = db.session.query(Todo).all()
    return render_template("index.html", notes=all_notes)


@app.route("/", methods=["POST"])
def add():
    if request.method == "POST":
        get_notes = request.form['note']
        save_note = Todo(date=date_now, notes=f"{get_notes}")
        db.session.add(save_note)
        db.session.commit()
    return redirect("/")


@app.route("/mark")
def mark():
    note_id = request.args.get("id")
    note = Todo.query.get(note_id)
    if note.bd_color == "#000":
        note.bd_color = "#FF0000"
        note.bd_outline = "2px"
        db.session.commit()
    else:
        note.bd_color = "#000"
        note.bd_outline = "1px"
        db.session.commit()
    return redirect("/")


@app.route("/done")
def done():
    note_id = request.args.get("id")
    note = Todo.query.get(note_id)
    if note.done_line == "none":
        note.done_line = "line-through"
        note.bd_color = "#CCC"
        note.bd_outline = "1px"
        note.done_display = "none"
        db.session.commit()
    else:
        note.done_line = "none"
        note.bd_color = "#000"
        note.done_display = "flex"
        db.session.commit()
    return redirect("/")


@app.route("/delete")
def delete():
    note_id = request.args.get("id")
    note = Todo.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
