from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from bson.objectid import ObjectId
import api
from datetime import datetime
# now = datetime.today().strftime('%Y-%m-%d')

# DATABASE
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


@app.template_filter('shorten_id')
def shorten_id(value):
    return abs(hash(value)) % (10 ** 8)


@app.before_request
def before_request():
    g.user = None

    if 'user_name' in session:
        if mydb.users.find_one({'username': session['user_name']}):
            g.user = mydb.users.find_one({'username': session['user_name']})


@app.route('/', methods=['GET', 'POST'])
def home():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_name=session['user_name'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_name', None)

        username = request.form['username']
        password = request.form['password']

        if mydb.users.find_one({'username': username, 'password': password}):
            session['user_name'] = username
            return redirect(url_for('dashboard'))

        return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_name=session['user_name'])


@app.route('/client_add', methods=['GET', 'POST'])
def client_add():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        inputName = request.form['inputName']
        inputEmail = request.form['inputEmail']
        inputPassword = request.form['inputPassword']
        inputCompany = request.form['inputCompany']
        inputPhoneNumber = request.form['inputPhoneNumber']
        inputPlan = request.form['inputPlan']
        inputActiveStatus = int(request.form['inputActiveStatus'])
        now = datetime.today().strftime('%Y-%m-%d')
        insert_data = {
            'name': inputName,
            'avatar': '/static/img/undraw_profile.svg',
            'email': inputEmail,
            'password': inputPassword,
            'phone': inputPhoneNumber,
            'company': inputCompany,
            'plan': inputPlan,
            'active': inputActiveStatus,
            'timestamp': now
        }

        mydb.clients.insert_one(insert_data)
        return redirect(url_for('manage_clients'))

    else:
        return render_template('client_add.html', user_name=session['user_name'], clients=mydb.clients.find())


@app.route('/client_delete_<client_id>')
def client_delete(client_id):
    if not g.user:
        return redirect(url_for('login'))

    print(type(client_id))
    find_user = api.get_client_info(client_id)
    return render_template('client_delete.html', user_name=session['user_name'], client=find_user)


@app.route('/client_edit_<client_id>')
def client_edit(client_id):
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        inputName = request.form['inputName']
        inputEmail = request.form['inputEmail']
        inputPassword = request.form['inputPassword']
        inputCompany = request.form['inputCompany']
        inputPhoneNumber = request.form['inputPhoneNumber']
        inputPlan = request.form['inputPlan']
        inputActiveStatus = int(request.form['inputActiveStatus'])
        now = datetime.today().strftime('%Y-%m-%d')
        myquery = {"_id": client_id}
        newvalues = {"$set": {'name': inputName,
                              'avatar': '/static/img/undraw_profile.svg',
                              'email': inputEmail,
                              'password': inputPassword,
                              'phone': inputPhoneNumber,
                              'company': inputCompany,
                              'plan': inputPlan,
                              'active': inputActiveStatus,
                              'timestamp': now}}

        mydb.clients.update_one(myquery, newvalues)
        return redirect(url_for('manage_clients'))

    else:
        print(client_id)
        find_user = api.get_client_info(client_id)
        return render_template('client_edit.html', user_name=session['user_name'], client=find_user)

# @app.route('/client_edit_<client_id>')
# def client_edit(client_id):
#     if not g.user:
#         return redirect(url_for('login'))

#     print(client_id)
#     find_user = api.get_client_info(client_id)
#     return render_template('client_edit.html', user_name=session['user_name'], client=find_user)


@app.route('/index')
def index():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('index.html', user_name=session['user_name'])


@app.route('/manage_clients')
def manage_clients():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_clients.html', user_name=session['user_name'], clients=mydb.clients.find())


@app.route('/manage_services')
def manage_services():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_services.html', user_name=session['user_name'], services=mydb.services.find())


@app.route('/manage_speech_to_text_file')
def manage_speech_to_text_file():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_speech_to_text_file.html', user_name=session['user_name'], sttfiles=mydb.sttfiles.find())


@app.route('/manage_tags')
def manage_tags():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_tags.html', user_name=session['user_name'], tags=mydb.tags.find())


@app.route('/manage_voiceid')
def manage_voiceid():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_voiceid.html', user_name=session['user_name'], voiceids=mydb.voiceids.find())


@app.route('/service_add')
def service_add():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('service_add.html', user_name=session['user_name'])


@app.route('/voice_id_delete')
def voice_id_delete():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('voice_id_delete.html', user_name=session['user_name'])


@app.route('/voice_id_edit')
def voice_id_edit():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('voice_id_edit.html', user_name=session['user_name'])


@app.route('/blank')
def blank():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('blank.html', user_name=session['user_name'])


@app.route('/remove_client_<client_id>')
def remove_client(client_id):
    # print(type(client_id))
    find_user = api.get_client_info(client_id)
    mydb.clients.remove({'_id': ObjectId(client_id)})
    return redirect(url_for('manage_clients'))


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8098, debug=True)
    app.run(debug=True)
