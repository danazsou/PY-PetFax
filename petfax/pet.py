from flask import (Blueprint, render_template, request, redirect)
from . import models
import json

pets = json.load(open('pets.json'))
# print(pets)

bp = Blueprint("pet", __name__, url_prefix="/pets")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pet_name = request.form["petName"]
        pet_photo = request.form["petPhoto"]
        pet_fact = request.form["petFact"]

        new_pet = models.Pet(
            pet_name=pet_name,
            pet_photo=pet_photo,
            pet_fact=pet_fact)
        models.db.session.add(new_pet)
        models.db.session.commit()
        return redirect("/pets")

    results = models.Pet.query.all()

    return render_template("pets/index.html", pets=results)


@bp.route("/delete/<int:id>")
def delete(id):
    pet = models.Pet.query.get(id)
    models.db.session.delete(pet)
    models.db.session.commit()
    return redirect("/pets")


@bp.route("/<int:id>")
def show(id):
    pet = models.Pet.query.get(id)
    return render_template("pets/show.html", pet=pet)


@bp.route("/new")
def new():
    return render_template("pets/new.html")
