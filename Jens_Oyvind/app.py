from flask import Flask, render_template, request, redirect, url_for, g, flash, session, abort, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from functions import get_db, valid_login, valid_user_password, is_admin, allowed_file, calculate_percentage

database = 'database.db'
app = Flask(__name__)
app.secret_key = "verysecret"
app.config['UPLOAD_FOLDER'] = 'static/uploads' 

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Sender logged_in_user, darkmode, isadmin, og profile_pic til template hver gang en side lastes inn
@app.context_processor
def inject_user_data():
    logged_in_user = session.get("username", None)
    darkmode = None
    if logged_in_user is not None:
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT name FROM users WHERE name = ?", (logged_in_user,))
            cur.fetchone()[0] # TypeError hvis session cookie er for en bruker som ikke eksister
            cur.execute("SELECT darkmode FROM users WHERE name = ?", (logged_in_user,))
            result = cur.fetchone()
            if result:
                darkmode = result[0]
            cur.execute('SELECT profile_pic FROM users WHERE name = ?', (logged_in_user,))
            result = cur.fetchone()
            profile_pic = result[0] if result else None
        except TypeError:
            session.pop("username")
            logged_in_user = None
            profile_pic = None
    else:
        profile_pic = None
    isadmin = is_admin(logged_in_user)
    return dict(logged_in_user=logged_in_user, darkmode=darkmode, isadmin=isadmin, profile_pic=profile_pic)

######################################## ROUTES #########################################

#### User handling ####

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":  
        if valid_login(request.form["username"], request.form["password"]):
            session["username"] = request.form["username"]
            if session["username"] == 'admin':
                return redirect(url_for("admin"))
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password! Username and password are case-sensitive.", "error")
            return render_template("login.html")
    else:
        if session.get("username", None) is None:
            return render_template("login.html")
        flash("You are already logged in.", "success")
        return render_template("index.html") 

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("index"))

# Oppretter bruker/admin
@app.route("/users/new", methods=["GET", "POST"])
def register():
    logged_in_user = session.get("username", None)
    isadmin = is_admin(logged_in_user)
    if request.method == "POST":
        if valid_user_password(request.form["password"], request.form["password_retype"]):
                username = request.form["username"]
                password_hashed = generate_password_hash(request.form["password"])
                if isadmin: # Dobbeltsjekk om admin er logget inn
                    register_as_admin  = request.form.get("admin") == "on" # returnerer True/False. 
                else:
                    register_as_admin = False
                conn = get_db()
                cur = conn.cursor()
                # Tildeler id_user nummer. Laveste tilgjengelige blir tildelt
                cur.execute("""
                        SELECT MIN(id_user + 1) 
                        FROM users
                        WHERE id_user + 1 NOT IN (SELECT id_user FROM users)
                    """)
                lowest_available_id = cur.fetchone()[0]
                sql_add_user = """
                INSERT INTO users (id_user, name, password, isadmin, profile_pic, darkmode, tokens) 
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """
                try:
                    cur.execute(sql_add_user, (lowest_available_id, username, password_hashed, register_as_admin, None,  0, 0))
                    conn.commit()
                    flash(f"New user created with name {username}", "success")
                    if not isadmin:
                        session["username"] = username
                        logged_in_user = username
                        return render_template("index.html")
                    else:
                        return render_template("register_user.html")
                except sqlite3.IntegrityError:
                    flash(f"Username is taken.", "error")
                    return render_template("register_user.html")
        else:
            flash("Please try again", "error")
    return render_template("register_user.html")


# Sletter egen bruker. Admin kan slette andre brukere.
@app.route("/users/<username>/delete", methods=["DELETE"])
def delete_user(username):
    try:
        logged_in_user = session.get("username", None)
        conn = get_db()
        cur = conn.cursor()
        if username == logged_in_user or is_admin(logged_in_user):
            if username == logged_in_user:
                session.pop("username")
            cur.execute('SELECT profile_pic FROM users WHERE name=?', (username, ))
            result = cur.fetchone()
            if result:
                file_path = result[0]
                if file_path is not None:
                    folder_path = os.path.dirname(file_path)
                    # Sletter bilde:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        os.rmdir(folder_path) #sletter den tomme mappen
            cur.execute('SELECT id_user FROM users WHERE name=?', (username, ))
            id_user = cur.fetchone()[0]
            cur.execute("DELETE FROM answers WHERE id_user = ?", (id_user,))
            cur.execute("DELETE FROM users WHERE id_user = ?", (id_user,))
            conn.commit()
            return jsonify({"message": "User successfully deleted."}), 200
        else:
            return jsonify({"message": "You do not have permission to delete this user."}), 403
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
    

@app.route("/api/availability")
def check_username_availability():
    username = request.args.get("username", "")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE name = ?", (username,))
    result = cur.fetchone()
    if result:
        return jsonify({"available": False, "message": "Username is already taken"})
    else:
        return jsonify({"available": True, "message": "Username is available"})

@app.route("/user/account")
def account():
    logged_in_user = session.get("username", None)
    if logged_in_user is not None:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT tokens FROM users WHERE name = ?", (logged_in_user,))
        result = cur.fetchone()
        if result:
            tokens = result[0]   
        return render_template("account.html", tokens=tokens)
    else:
        abort(401)

@app.route('/api/user/upload', methods=['POST'])
def upload_profile_pic():
    if request.method == 'POST':
        logged_in_user = session.get("username", None)
        if logged_in_user is None:
            abort(401)
        file = request.files['image']
        if file and file.filename != '':
            if not allowed_file(file.filename):
                return 'File type not allowed. Only PNG, JPG, and JPEG are accepted'
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], logged_in_user)
            os.makedirs(user_folder, exist_ok=True) # Oppretter folder
            filename = secure_filename(file.filename)
            filepath = os.path.join(user_folder, filename) # path blir static/uploads/username/filename
            file.save(filepath)
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE users SET profile_pic = ? WHERE name = ?', (filepath, logged_in_user))
            conn.commit()
            return redirect(url_for('account'))
        return 'No file uploaded', 400


@app.route('/api/user/preferences', methods=['PUT'])
def update_preferences():
    logged_in_user = session.get("username", None)
    if logged_in_user:
        darkmode = request.json.get('darkmode', None) # Mottatt fra darkModeToggle() js
        if darkmode is not None:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("UPDATE users SET darkmode = ? WHERE name = ?", (darkmode, logged_in_user))
            db.commit()
            return jsonify({"message": "Success"}), 200
        else:
            return jsonify({"error": "Error"}), 400 #Bad request
    return jsonify({"error": "User not logged in"}), 401 #Unauthorized

@app.route("/admin")
def admin():
    if is_admin(session["username"]):
        return render_template("admin.html")
    else:
        abort(401)

@app.route("/admin/users")
def manage_users():
    if is_admin(session["username"]):
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT name, id_user FROM users ORDER BY id_user')
        users = cur.fetchall()
        user_list = [{'name': name, 'id_user': id_user} for name, id_user in users] # liste av dict
        return render_template("manage_users.html", user_list=user_list)
    else:
        return abort(401)
    
# Viser prosentandel av brukere som har gjennomført undersøkelsene
@app.route("/admin/statistics")
def statistics():
    if is_admin(session.get("username")):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) AS total_users FROM users;")
        result = cur.fetchone()
        total_users = result[0]
        sql_users_answered_per_questionnaire = """
        SELECT questionnaires.id_questionnaire, questionnaires.name_questionnaire, COUNT(DISTINCT id_user) AS users_answered FROM questionnaires
        LEFT JOIN answers ON questionnaires.id_questionnaire = answers.id_questionnaire
        GROUP BY questionnaires.id_questionnaire, questionnaires.name_questionnaire
        ORDER BY questionnaires.id_questionnaire;
        """
        # LEFT JOIN for å inkludere ubesvarte undersøkelser
        # GROUP BY for å inkludere hver undersøkelse kun 1 gang
        cur.execute(sql_users_answered_per_questionnaire)
        rows = cur.fetchall()
        questionnaire_data = [
            {
                "id_questionnaire": row[0],
                "name_questionnaire": row[1],
                "users_answered": row[2],
                "percentage_answered": calculate_percentage(row[2], total_users)
            }
            for row in rows
        ]
        return render_template("statistics.html", questionnaire_data=questionnaire_data, total_users=total_users)
    else:
        return abort(401)


############### Questionnaires handling ###############

# This route lists the questionnaires
@app.route('/api/questionnaires')
def questionnaires():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id_questionnaire, name_questionnaire FROM questionnaires')
    questionnaires: list = cur.fetchall()
    conn.close()
    questionnaire_list_of_dict: list = []
    for id_questionnaire, name_questionnaire in questionnaires:
        questionnaire_dict: dict = {
            'id_questionnaire': id_questionnaire, 
            'name_questionnaire': name_questionnaire
        }
        questionnaire_list_of_dict.append(questionnaire_dict)
    return jsonify(questionnaire_list_of_dict)

# Oppretter ny undersøkelse
@app.route('/questionnaire/new', methods=['GET', 'POST'])
def make_query():
    logged_in_user = session.get("username", None)
    if logged_in_user is None:
        abort(401)
    if is_admin(logged_in_user):
        if request.method == 'POST':
            num_questions = request.form.get('num_questions')
            name_questionnaire = request.form.get('name_questionnaire')
            try:
                num_questions = int(num_questions)
            except:
                flash('Not a number', 'error')
                return render_template("make_query.html")
            return redirect(url_for('add_query', num_questions=num_questions, name_questionnaire=name_questionnaire))
        return render_template("make_query.html")
    else:
        abort(401)

# Route mottar spørsmål fra F-E og sender inn i database, setter inn i tabell questionnaires og questionnaire
@app.route('/questionnaire/questions', methods=['GET','POST'])
def add_query():
    logged_in_user = session.get("username", None)
    if logged_in_user is None:
        abort(401)
    num_questions = request.args.get('num_questions', default=0, type=int)
    if num_questions > 100:
        flash("Too many questions", "error")
        return render_template("add_query.html", num_questions=num_questions, name_questionnaire=name_questionnaire) 
    name_questionnaire = request.args.get('name_questionnaire', default='', type=str)
    if len(name_questionnaire) == 0:
        flash("No name", "error")
        return render_template("add_query.html", num_questions=num_questions, name_questionnaire=name_questionnaire) 
    if request.method == 'POST':
        questionnaire_recived = request.form
        question_list = []
        for key in questionnaire_recived:
            question_list.append(questionnaire_recived[key])
            conn = get_db()
            cur = conn.cursor()
            cur.execute('SELECT MAX(id_questionnaire) FROM questionnaires')
            last_id_questionnaire = cur.fetchone()[0]
            cur.execute('SELECT MAX(id_question) FROM questionnaire')
            last_id_question = cur.fetchone()[0]
            if last_id_questionnaire is None:
                last_id_questionnaire = 0
            new_id_questionnaire = last_id_questionnaire + 1
            if last_id_question is None:
                last_id_question = 0
            new_id_question = last_id_question + 1
        try:    
            cur.execute('INSERT INTO questionnaires (id_questionnaire, name_questionnaire) VALUES (?, ?)', (new_id_questionnaire, name_questionnaire))
            for question in question_list:
                if len(question) == 0:
                    flash("Empty question", "error")
                    return render_template("add_query.html", num_questions=num_questions, name_questionnaire=name_questionnaire) 
                cur.execute('INSERT INTO questionnaire (id_questionnaire, id_question, question) VALUES (?, ?, ?)', (new_id_questionnaire, new_id_question, question))
                new_id_question += 1
            conn.commit()
            flash(f'Questionnaire {new_id_questionnaire}: {name_questionnaire} inserted into database', 'success')
            return redirect(url_for('make_query'), )
        except Exception as e:
            flash('Questionnaires table input failed', 'error')
    return render_template("add_query.html", num_questions=num_questions, name_questionnaire=name_questionnaire) 

# Legg til, eller endre svar på undersøkelse
@app.route('/questionnaire/<int:id_questionnaire>', methods=['GET', 'POST'])
def add_answers(id_questionnaire):
    logged_in_user = session.get('username', None)
    if logged_in_user is None:
        abort(401)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id_user FROM users WHERE name=?', (logged_in_user, ))
    id_user = cur.fetchone()[0]
    cur.execute('SELECT name_questionnaire FROM questionnaires WHERE id_questionnaire= ?', (id_questionnaire, ))
    name_questionnaire = cur.fetchone()[0]
    cur.execute('SELECT id_question, question FROM questionnaire WHERE id_questionnaire= ?', (id_questionnaire, ))
    questions_received = cur.fetchall()
    questions = []
    id_questions_list = []
    for question in questions_received:
        id_questions_list.append(question[0])
        questions.append(question[1])
    # sjekker om brukeren har svart på undersøkelsen:
    cur.execute('''
        SELECT COUNT(*) FROM answers 
        WHERE id_user=? AND id_questionnaire=?
    ''', (id_user, id_questionnaire))
    already_answered = cur.fetchone()[0] > 0 # returnerer True/False
    user_answers = {}
    if already_answered:
        cur.execute('''
            SELECT id_question, answer FROM answers
            WHERE id_user = ? AND id_questionnaire = ?
        ''', (id_user, id_questionnaire))
        for row in cur.fetchall():
            user_answers[row[0]] = row[1]
    if request.method == 'POST':
        answers_received = request.form
        answers_list = [value for key, value in answers_received.items() if key != '_method'] # legger ikke inn _method
        # Sjekker om svarene som mottas er gyldig
        for answer in answers_list:
            try:
                if int(answer) < 1 or int(answer) > 5:
                    flash('Each answer must be an integer between 1 and 5.', 'error')
                    return render_template('add_answers.html', id_questionnaire=id_questionnaire, name_questionnaire=name_questionnaire, questions=questions, already_answered=already_answered, user_answers=user_answers, id_questions_list=id_questions_list)
            except ValueError:
                flash('All answers must be valid integers.', 'error')
                return render_template('add_answers.html', id_questionnaire=id_questionnaire, name_questionnaire=name_questionnaire, questions=questions, already_answered=already_answered, user_answers=user_answers, id_questions_list=id_questions_list)

        try:
            if request.form.get('_method') == 'PUT': # Endre svar
                sql = '''
                UPDATE answers 
                SET answer = ? 
                WHERE id_questionnaire = ? AND id_question = ? AND id_user = ?
                '''
                for index ,answer in enumerate(answers_list):
                    cur.execute(sql, (answer, id_questionnaire, id_questions_list[index], id_user))
                conn.commit()
                flash('Answers updated', 'success')
                return redirect(url_for('index'))
            else: # Lagre nytt svar
                sql = 'INSERT INTO answers (id_questionnaire, id_question, id_user, answer) VALUES (?, ?, ?, ?)'
                for index ,answer in enumerate(answers_list):
                    cur.execute(sql, (id_questionnaire, id_questions_list[index], id_user, answer))
                conn.commit()
                flash('Answers submitted', 'success')
                session['questionnaire_completed'] = True #lagrer at bruker har faktisk svart
                return redirect(url_for('game'))
        except:
            flash('Answers not submitted', 'error')
            return render_template('add_answers.html', id_questionnaire=id_questionnaire, name_questionnaire=name_questionnaire, questions=questions, already_answered=already_answered, user_answers=user_answers, id_questions_list=id_questions_list)
        
    if request.method == 'GET':
        return render_template('add_answers.html', id_questionnaire=id_questionnaire, name_questionnaire=name_questionnaire, questions=questions, already_answered=already_answered, user_answers=user_answers, id_questions_list=id_questions_list)

# Sjekker hvilke undersøkelser brukeren har gjennomført. Fetches fra listQuestionnaires() i script.js
@app.route("/api/questionnaire/completed")
def completed_questionnaires():
    logged_in_user = session.get("username", None)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id_user FROM users WHERE name=?', (logged_in_user, ))
    id_user = cur.fetchone()[0]
    cur.execute('SELECT id_questionnaire FROM answers WHERE id_user =?', (id_user, ))
    completed = cur.fetchall()
    completed_ids = [row[0] for row in completed]
    return jsonify(completed_ids)


# Route for game, legger til tokens i databasen
@app.route('/game', methods=['GET', 'PUT'])
def game():
    if request.method == 'PUT':    
        new_tokens = request.json.get('tokens')
        if new_tokens:
            logged_in_user = session.get("username", None)
            conn = get_db()
            cur = conn.cursor()
            cur.execute('SELECT tokens FROM users WHERE name=?', (logged_in_user, ))
            old_tokens = cur.fetchone()[0]
            current_tokens = new_tokens + old_tokens
            cur.execute('UPDATE users SET tokens=? WHERE name=?', (current_tokens, logged_in_user))
            conn.commit()
            flash(f'You won {new_tokens} tokens! You now have {current_tokens} tokens.', 'success')
            session['questionnaire_completed'] = False
            return jsonify({'status': 'success'})
        else:
            flash("You didn't win, sorry!", 'error')
            session['questionnaire_completed'] = False
            return jsonify({}) # Nothing because it needs a return and redirect does not work from flask directly
    if request.method == 'GET':
        # Sjekker at brukeren svarte på undersøkelsen
        if not session['questionnaire_completed']:
                flash('You must complete the questionnaire first.', 'error')
                return redirect(url_for('index'))
        return render_template('game.html')

if __name__ == "__main__":
    app.run(debug=True)