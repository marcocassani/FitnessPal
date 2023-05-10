
from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "SC3ypfBlK6RKvK2Gwg=="

# TODO: Fill in methods and routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if db_session.query(User).where((User.username == username) & (User.password == password)).first() != None:
            session["username"] = username
        else: 
            return render_template("login.html")

        return redirect(url_for("workouts"))



@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["retype-password"]
        age = request.form["age"]
        sex = request.form["sex"]

        if verify == password:
            newUser = User(username, password, age, sex)
            db_session.add(newUser)
            session["username"] = username
            db_session.commit()

        return redirect(url_for("workouts"))


        
@app.route("/workouts", methods = ["GET", "POST"])
def workouts():
        if "username" in session:
            currentUser = db_session.query(User).where(User.username == session["username"]).first()

            #compiles list of obj that meet criteria
            cardio = db_session.query(Workout).where((currentUser.age <= Workout.max_age) & (Workout.category == "cardio") & (currentUser.sex == Workout.sex or Workout.sex =="both")).all()
            upperbody = db_session.query(Workout).where((currentUser.age <= Workout.max_age) & (Workout.category == "upper body") & (currentUser.sex == Workout.sex or Workout.sex =="both")).all()
            lowerbody = db_session.query(Workout).where((currentUser.age <= Workout.max_age) & (Workout.category == "lower body") & (currentUser.sex == Workout.sex or Workout.sex =="both")).all()
            core = db_session.query(Workout).where((currentUser.age <= Workout.max_age) & (Workout.category == "cardio") & (currentUser.sex == Workout.sex or Workout.sex =="both")).all()

            return render_template("workouts.html", c = cardio, u = upperbody, l = lowerbody, co = core)

        else:
            return redirect(url_for("index"))

@app.route("/exercise")
def exercise():
    if request.method == "GET":
        if "username" in session:

            #header = db_session.query(Workout).where(header of the link that I clicked on)

            return render_template("exercise.html")
        else:
            return redirect(url_for("index"))

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
