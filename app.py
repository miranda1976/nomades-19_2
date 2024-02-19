from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firebase Authentication
firebase_auth = auth

# δημιουργω εναν χρηστη admin αν δεν υπαρχει (για τεστ) 
user_data = {
    'username': 'Miranda3',
    'type': 'Administrator',
    'userid': '0',
    'password': '123456',
}

# δημιουργω εναν χρηστη professor αν δεν υπαρχει (για τεστ) 
user_data = {
    'username': 'Antonio',
    'type': 'Professor',
    'userid': '1',
    'password': '123456',
}
user_query = db.collection('users').where('username', '==', user_data['username'])
existing_users = user_query.stream()
if not any(existing_users):
    db.collection('users').add(user_data)
    print(f"User with UID {user_data['username']} added.")
else:
    print(f"User with UID {user_data['username']} already exists.")
#τελος δημιουργιας χρηστη

#η default συναρτηση που ανοιγει την αρχικη σελιδα (Login page)
@app.route('/')
def index():
    return render_template('index.html')

#οταν ο χρηστης παταει να απαντησει σαν ανωνυμος χρηστης καλει το ερωτηματολογιο
@app.route('/questions')
def questions():
    return render_template('questions.html')

#οταν ο χρηστης κανει submit το ερωτηματολογιο, καλειται αυτη η συναρτηση
#request.form.get is a method commonly used in web development frameworks to retrieve data from an HTML form submitted by a user
@app.route('/questionnairesubmit', methods=['POST'])
def questionnairesubmit():
    questionnaire_data = {
        'formationSelect': request.form.get('formationSelect'),
        'startDate': request.form.get('startDate'),
        'endDate': request.form.get('endDate'),
        'sessionsSelect': request.form.get('sessionsSelect'),
        'trimestreSelect': request.form.get('trimestreSelect'),
        'firstName': request.form.get('firstName'),
        'profession': request.form.get('profession'),
        'lastName': request.form.get('lastName'),
        'evaluationDate': request.form.get('evaluationDate'),
        'formationPrincipale': request.form.get('formationPrincipale'),
        'perspectivesPro': request.form.get('perspectivesPro'),
        'situationActuelle': request.form.get('situationActuelle'),
        'utilisationConnaissances': request.form.get('utilisationConnaissances'),
        'utiliteFuture': request.form.get('utiliteFuture'),
        'utiliteFormation': request.form.get('utiliteFormation'),
        'utiliteConnaissance': request.form.get('utiliteConnaissance'),
        'utiliteDeviez': request.form.get('utiliteDeviez'),
        'utiliteGlobale': request.form.get('utiliteGlobale'),
        'niveauConnaissances': request.form.get('niveauConnaissances'),
        'utiliteMethode': request.form.get('utiliteMethode'),
        'utiliteCompetences': request.form.get('utiliteCompetences'),
        'utiliteClarte': request.form.get('utiliteClarte'),
        'utiliteDisponibilite': request.form.get('utiliteDisponibilite'),
        'utiliteCompe1': request.form.get('utiliteCompe1'),
        'utiliteCompe2': request.form.get('utiliteCompe2'),
        'utiliteCompe3': request.form.get('utiliteCompe3'),
        'utiliteCompe4': request.form.get('utiliteCompe4'),
        'apprécié': request.form.get('apprécié'),
        'appréciéMoins': request.form.get('appréciéMoins'),
        'enseignants': request.form.get('enseignants'),
        'enseignantevaluation1': request.form.get('enseignantevaluation1'),
        'enseignantPedagogue1': request.form.get('enseignantPedagogue1'),
        'enseignantevaluation2': request.form.get('enseignantevaluation2'),
        'enseignantPedagogue2': request.form.get('enseignantPedagogue2'),
        'commentaires': request.form.get('commentaires'),
        'enseignantsAvis': request.form.get('enseignantsAvis'),
        'commentaireséquipe': request.form.get('commentaireséquipe'),
        'enseignantExperience': request.form.get('enseignantExperience'),
        'enseignantEnseignement': request.form.get('enseignantEnseignement'),
        'enseignantMethode': request.form.get('enseignantMethode'),
        'enseignantSupport': request.form.get('enseignantSupport'),
        'commentairesEns': request.form.get('commentairesEns'),
        'StaffCompetentes': request.form.get('StaffCompetentes'),
        'StaffDisponibles': request.form.get('StaffDisponibles'),
        'StaffRepondu': request.form.get('StaffRepondu'),
        'commentaireStaff': request.form.get('commentaireStaff'),
        'formationC': request.form.get('formationC'),
        'formationOui': request.form.get('formationOui'),
        'Institut': request.form.get('Institut'),
        'Niveau': request.form.get('Niveau'),
        'commentaireAttentes': request.form.get('commentaireAttentes'),
        'formationClasser': request.form.get('formationClasser'),
        'commentairesN': request.form.get('commentairesN'),
        'formationP': request.form.get('formationP'),
        'formationD': request.form.get('formationD'),
        'commentairesS': request.form.get('commentairesS'),
        'DateToday': request.form.get('DateToday'),
        'submissiontime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db.collection('questionnaires').add(questionnaire_data) #προσθεσε το ερωτηματολογιο στη βαση
    return redirect(url_for('submitted'))
    
@app.route('/submitted')
def submitted():
    return render_template('submitted.html')

# η συναρτηση αυτη καλειται απο το Login page οταν ο χρηστης βαλει το username κ password
@app.route('/login', methods=['POST'])
def login():
    try:
        # παιρνω τα στοιχεια που εβαλε ο χρηστης
        username = request.form.get('username')
        password = request.form.get('password')

        # ελεγχω αν αυτα τα στοιχεια υπαρχουν στη βαση users
        users = db.collection('users')
        query = users.where('username', '==', username).where('password', '==', password)
        existing_users = query.get()
        
        if not any(existing_users): # login failed
            print('Invalid username or password')
            return render_template('index.html', error_message='Invalid username or password')
        else: #login success
            user_data = existing_users[0].to_dict()
            # περναω τα στοιχεια του χρηστη στην επομενη σελιδα ωστε να μπορει να δει το καταλληλο περιεχομενο
            session['username'] = username
            session['usertype'] = user_data.get('type')
            print('Welcome', user_data['username'], "!")
            return redirect(url_for('dashboard')) # πηγαινε στην σελιδα dashboard
    except Exception as e:
        print(e);

@app.route('/dashboard')
def dashboard():
    # ελεγχω αν ο χρηστης ειναι authenticated
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'], usertype=session['usertype'])

@app.route('/dashboard/displayquestionnaires', methods=['GET'])
def displayquestionnaires():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = db.collection('questionnaires')
    documents = query.stream()
    data = [doc.to_dict() for doc in documents] 
    print(data[0].get('firstName'))
    flag = 1
    return jsonify({'data': data, 'flag': flag})

# κανω logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) # ξεχναω το login
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)
