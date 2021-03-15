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
import os
from datetime import datetime
from werkzeug.utils import secure_filename
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
        elif mydb.clients.find_one({'email': session['user_name']}):
            g.user = mydb.clients.find_one({'email': session['user_name']})


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
            session['role'] = 'super_admin'
            return redirect(url_for('dashboard'))

        elif mydb.clients.find_one({'email': username, 'password': password}):
            session['user_name'] = username
            session['role'] = 'client'
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/index', methods=['GET'])
def index():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('index.html', user_name=session['user_name'])


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_name=session['user_name'], role=session['role'])


# CLIENT


@app.route('/manage_clients', methods=['GET'])
def manage_clients():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_clients.html', user_name=session['user_name'], role=session['role'], clients=mydb.clients.find())


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
        inputActiveStatus = (request.form.getlist(
            'inputActiveStatus')) and 1 or 0
        now = datetime.today().strftime('%Y-%m-%d')

        target = '/static/img/'
        filename = request.files['face_image']
        inputAvatar = target + filename.filename
        if inputAvatar == target:
            inputAvatar = '/static/img/undraw_profile.svg'

        insert_data = {
            'name': inputName,
            'avatar': inputAvatar,
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
        return render_template('client_add.html', user_name=session['user_name'], role=session['role'], clients=mydb.clients.find())


@app.route('/client_edit/<client_id>', methods=['GET', 'POST'])
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
        inputActiveStatus = (request.form.getlist(
            'inputActiveStatus')) and 1 or 0
        now = datetime.today().strftime('%Y-%m-%d')

        find_user = api.get_client_info(client_id)
        target = '/static/img/'
        filename = request.files['face_image']
        inputAvatar = target + filename.filename
        if inputAvatar == target:
            inputAvatar = find_user.get('avatar')

        myquery = {"_id": ObjectId(client_id)}
        newvalues = {"$set": {'name': inputName,
                              'avatar': inputAvatar,
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
        find_user = api.get_client_info(client_id)
        return render_template('client_edit.html', user_name=session['user_name'], role=session['role'], client=find_user)


@app.route('/client_delete/<client_id>', methods=['GET'])
def client_delete(client_id):
    if not g.user:
        return redirect(url_for('login'))

    find_user = api.get_client_info(client_id)
    return render_template('client_delete.html', user_name=session['user_name'], role=session['role'], client=find_user)


@app.route('/remove_client/<client_id>', methods=['GET'])
def remove_client(client_id):
    find_user = api.get_client_info(client_id)
    mydb.clients.delete_one({'_id': ObjectId(client_id)})
    return redirect(url_for('manage_clients'))


# SERVICE


@app.route('/manage_services', methods=['GET'])
def manage_services():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_services.html', user_name=session['user_name'], role=session['role'], services=mydb.services.find())


@app.route('/service_add', methods=['GET', 'POST'])
def service_add():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        inputName = request.form['inputName']
        inputDescription = request.form['inputDescription']
        inputMaxFiles = int(request.form['inputMaxFiles'])
        inputMaxTimePerFile = int(request.form['inputMaxTimePerFile'])
        now = datetime.today().strftime('%Y-%m-%d')
        insert_data = {
            'name': inputName,
            'description': inputDescription,
            'max_files': inputMaxFiles,
            'max_time_per_file': inputMaxTimePerFile,
            'update_at': now
        }

        mydb.services.insert_one(insert_data)
        return redirect(url_for('manage_services'))

    else:
        return render_template('service_add.html', user_name=session['user_name'], role=session['role'], services=mydb.services.find())


@app.route('/service_edit/<service_id>', methods=['GET', 'POST'])
def service_edit(service_id):
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        inputName = request.form['inputName']
        inputDescription = request.form['inputDescription']
        inputMaxFiles = int(request.form['inputMaxFiles'])
        inputMaxTimePerFile = int(request.form['inputMaxTimePerFile'])
        now = datetime.today().strftime('%Y-%m-%d')

        myquery = {"_id": ObjectId(service_id)}
        newvalues = {"$set": {'name': inputName,
                              'description': inputDescription,
                              'max_files': inputMaxFiles,
                              'max_time_per_file': inputMaxTimePerFile,
                              'update_at': now}}

        mydb.services.update(myquery, newvalues)

        return redirect(url_for('manage_services'))

    else:
        find_service = api.get_service_info(service_id)
        return render_template('service_edit.html', user_name=session['user_name'], role=session['role'], service=find_service)


@app.route('/service_delete/<service_id>', methods=['GET'])
def service_delete(service_id):
    if not g.user:
        return redirect(url_for('login'))

    find_service = api.get_service_info(service_id)
    return render_template('service_delete.html', user_name=session['user_name'], role=session['role'], service=find_service)


@app.route('/remove_service/<service_id>', methods=['GET'])
def remove_service(service_id):
    find_user = api.get_service_info(service_id)
    mydb.services.delete_one({'_id': ObjectId(service_id)})
    return redirect(url_for('manage_services'))

# SPEECH TO TEXT FILE


@app.route('/manage_speech_to_text_file', methods=['GET'])
def manage_speech_to_text_file():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_speech_to_text_file.html', user_name=session['user_name'], role=session['role'], sttfiles=mydb.sttfiles.find())


# TAGS


@app.route('/manage_tags', methods=['GET'])
def manage_tags():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_tags.html', user_name=session['user_name'], role=session['role'], tags=mydb.tags.find())


# VOICEID


@app.route('/manage_voiceids', methods=['GET'])
def manage_voiceids():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_voiceids.html', user_name=session['user_name'], role=session['role'], voiceids=mydb.voiceids.find())


@app.route('/voiceid_edit/<voiceid_id>', methods=['GET', 'POST'])
def voiceid_edit(voiceid_id):
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        inputName = request.form['inputName']
        inputEmail = request.form['inputEmail']
        inputPhoneNumber = request.form['inputPhoneNumber']
        inputCompany = request.form['inputCompany']
        inputDepartment = request.form['inputDepartment']
        inputTitle = request.form['inputTitle']
        inputTags = request.form['inputTags']
        now = datetime.today().strftime('%Y-%m-%d')

        find_user = api.get_voiceid_info(voiceid_id)
        target = '/static/img/'
        filename = request.files['face_image']
        inputAvatar = target + filename.filename
        if inputAvatar == target:
            inputAvatar = find_user.get('avatar')

        myquery = {"_id": ObjectId(voiceid_id)}
        newvalues = {"$set": {'name': inputName,
                              'avatar': inputAvatar,
                              'email': inputEmail,
                              'phone': inputPhoneNumber,
                              'company': inputCompany,
                              'department': inputDepartment,
                              'title': inputTitle,
                              'tags': inputTags,
                              'timestamp': now}}

        mydb.voiceids.update(myquery, newvalues)

        return redirect(url_for('manage_voiceids'))

    else:
        find_user = api.get_voiceid_info(voiceid_id)
        return render_template('voiceid_edit.html', user_name=session['user_name'], role=session['role'], voiceid=find_user)


@app.route('/voiceid_delete/<voiceid_id>', methods=['GET'])
def voiceid_delete(voiceid_id):
    if not g.user:
        return redirect(url_for('login'))

    find_voiceid = api.get_voiceid_info(voiceid_id)
    return render_template('voiceid_delete.html', user_name=session['user_name'], role=session['role'], voiceid=find_voiceid)


@app.route('/remove_voiceid/<voiceid_id>', methods=['GET'])
def remove_voiceid(voiceid_id):
    find_user = api.get_voiceid_info(voiceid_id)
    mydb.voiceids.delete_one({'_id': ObjectId(voiceid_id)})
    return redirect(url_for('manage_voiceids'))


@app.route('/blank', methods=['GET'])
def blank():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('blank.html', user_name=session['user_name'], role=session['role'])


@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_name', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8098, debug=True)
    app.run(debug=True)
