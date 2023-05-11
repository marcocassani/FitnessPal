
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

# check if username/password combo exist in database; if not, spit back out to index, if so, advance to workouts
        if db_session.query(User).where((User.username == username) & (User.password == password)).first() != None:
            session["username"] = username
            return redirect(url_for("workouts"))
        else:
            return render_template("index.html")


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
        #if is POST, save inputted data into variables to put into database if the password = check passcode. move onto workouts
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

            #compiles list of obj that meet criteria for each workout type
            cardio = db_session.query(Workout).where((currentUser.age <= Workout.max_age) & (Workout.category == "cardio") & ((currentUser.sex.lower() == Workout.sex) | (Workout.sex == "both"))).all()
            upperbody = db_session.query(Workout).where((currentUser.age <= Workout.max_age) & (Workout.category == "upper body") & ((currentUser.sex.lower() == Workout.sex) | (Workout.sex == "both"))).all()
            lowerbody = db_session.query(Workout).where((currentUser.age <= Workout.max_age) & (Workout.category == "lower body") & ((currentUser.sex.lower() == Workout.sex) | (Workout.sex == "both"))).all()
            core = db_session.query(Workout).where((currentUser.age <= Workout.max_age) & (Workout.category == "core") & ((currentUser.sex.lower() == Workout.sex) | (Workout.sex == "both"))).all()
            print(upperbody)
            return render_template("workouts.html", c = cardio, u = upperbody, l = lowerbody, co = core)
        else:
            return redirect(url_for("index"))

#pass in through URL
@app.route("/exercise/<workout_id>")
def exercise(workout_id):
    print(workout_id)
    if request.method == "GET":
        if "username" in session:
            #pass in desired information to fill exercise.html
            header = db_session.query(Workout.header).where((workout_id == Workout.id)).first()[0]
            info = db_session.query(Workout.info).where((workout_id == Workout.id)).first()[0]
            img = db_session.query(Workout.img).where((workout_id == Workout.id)).first()[0]

            return render_template("exercise.html", h = header, i = info, im = img)
        else:
            return redirect(url_for("index"))

@app.route("/logout")
def logout():
    if "username" in session:
        #remove from session so another can login
        session.pop("username")

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
