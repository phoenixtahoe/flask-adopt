from flask import Flask, request, redirect, render_template
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Work'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)
db.create_all()

@app.route('/')
def homePage():
    pets = Pet.query.all()
    return render_template("homepage.html", pets=pets)

@app.route('/add')
def petForm():
    form = AddPetForm()
    return render_template("petform.html", form=form)

@app.route('/add', methods=["POST"])
def petAdd():
    form = AddPetForm()

    new_pet = Pet(name=form.name.data, species=form.species.data, photo_url=form.photo_url.data, age=form.age.data, notes=form.notes.data)
    db.session.add(new_pet)
    db.session.commit()

    return redirect('/')

@app.route('/<int:pet_id>')
def petEdit(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    return render_template("editform.html", form=form, pet=pet)

@app.route('/<int:pet_id>', methods=["POST"])
def petUpdate(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    pet.notes = form.notes.data
    pet.available = form.available.data
    pet.photo_url = form.photo_url.data

    db.session.commit()

    return redirect('/')
