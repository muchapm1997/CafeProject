from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, form
from wtforms.validators import DataRequired, Length
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField("Map url", validators=[DataRequired()])
    img_url = StringField("img url", validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired()])
    has_sockets = StringField(label="Sockets", validators=[DataRequired()])
    has_toilet = StringField(label="Toilet", validators=[DataRequired()])
    has_wifi = StringField(label="Wifi", validators=[DataRequired()])
    can_take_calls = StringField(label="Can take calls", validators=[DataRequired()])
    seats = StringField(label="Seats", validators=[DataRequired()])
    coffee_price = StringField(label="Coffee price", validators=[DataRequired()])
    add_button = SubmitField(label="Add")


class CaffeModel(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.String(250), nullable=False)
    has_wifi = db.Column(db.String(250), nullable=False)
    can_take_calls = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()  # Utwórz instancję formularza
    if form.validate_on_submit():
        new_cafe = CaffeModel(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
    cafes = CaffeModel.query.with_entities(
        CaffeModel.name,
        CaffeModel.map_url,
        CaffeModel.img_url,
        CaffeModel.location,
        CaffeModel.has_sockets,
        CaffeModel.has_toilet,
        CaffeModel.has_wifi,
        CaffeModel.can_take_calls,
        CaffeModel.seats,
        CaffeModel.coffee_price
    ).all()
    return render_template('cafes.html', cafes=cafes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        migrate = Migrate(app, db)
        app.run(debug=True)