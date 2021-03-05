from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

# Demo Database
users = [
    {
        'id': '111',
        'username': 'admin',
        'password': 'admin'
    },
    {
        'id': '222',
        'username': 'admin2',
        'password': 'admin2'
    },
    {
        'id': '333',
        'username': 'thuan',
        'password': 'thuan'
    }
]

clients = [
    {
        'id': 2081113,
        'name': 'Shad Decker',
        'avatar': '/static/img/undraw_profile.svg',
        'email': 'RegionalDirector@gmail.com',
        'phone': '51',
        'company': 'Nextify',
        'plan': 'Plan',
        'active': 1,  # 1:active, 0:off
        'timestamp': '2021/01/03'
    },
    {
        'id': 2008111,
        'name': 'Shad Decker',
        'avatar': '/static/img/undraw_profile.svg',
        'email': 'RegionalDirector@gmail.com',
        'phone': '51',
        'company': 'Nextify',
        'plan': 'Plan',
        'active': 1,  # 1:active, 0:off
        'timestamp': '2021/01/04'
    }, {
        'id': 2008113,
        'name': 'Shad Decker',
        'avatar': '/static/img/undraw_profile.svg',
        'email': 'RegionalDirector@gmail.com',
        'phone': '51',
        'company': 'Nextify',
        'plan': 'Plan',
        'active': 1,  # 1:active, 0:off
        'timestamp': '2021/01/05'
    }, {
        'id': 2071113,
        'name': 'Shad Decker',
        'avatar': '/static/img/undraw_profile.svg',
        'email': 'RegionalDirector@gmail.com',
        'phone': '51',
        'company': 'Nextify',
        'plan': 'Plan',
        'active': 0,  # 1:active, 0:off
        'timestamp': '2021/01/06'
    }
]

voiceids = [
    {
        'id': 20081113,
        'name': 'Shad Decker',
        'avatar': '/static/img/undraw_profile.svg',
        'email': 'RegionalDirector@gmail.com',
        'phone': '51',
        'title': 'Nextify',
        'timestamp': '2021/01/06',
        'company': 'Plan',
        'department': 'Nhân sự',
        'tags': 'tag1'
    },
    {
        'id': 20081113,
        'name': 'Shad Decker',
        'avatar': '/static/img/undraw_profile.svg',
        'email': 'RegionalDirector@gmail.com',
        'phone': '51',
        'title': 'Nextify',
        'timestamp': '2021/01/06',
        'company': 'Plan',
        'department': 'Nhân sự',
        'tags': 'tag1'
    },
    {
        'id': 20081113,
        'name': 'Shad Decker',
        'avatar': '/static/img/undraw_profile.svg',
        'email': 'RegionalDirector@gmail.com',
        'phone': '51',
        'title': 'Nextify',
        'timestamp': '2021/01/06',
        'company': 'Plan',
        'department': 'Nhân sự',
        'tags': 'tag1'
    }
]

sttfiles = [
    {
        'id_user': '20130201',
        'id_voice': '20130201',
        'id_task': '20130201',
        'id_call': '20130201',
        'msg': 'Jennifer Acosta',
        'status': 1,  # 1: Đã xử lý, 2: Đang xử lý, 0: Không thành công
        'processing_time': 51,
        'audio_path': '/audio/audio1.wav',
        'audio_path_local': '/audio/audio1.wav',
        'content': 'Nextify',
        'update_at': '2021/01/02',
        'result_pattern': 'OK'
    },
    {
        'id_user': '20130201',
        'id_voice': '20130201',
        'id_task': '20130201',
        'id_call': '20130201',
        'msg': 'Jennifer Acosta',
        'status': 2,  # 1: Đã xử lý, 2: Đang xử lý, 0: Không thành công
        'processing_time': 51,
        'audio_path': '/audio/audio1.wav',
        'audio_path_local': '/audio/audio1.wav',
        'content': 'Nextify',
        'update_at': '2021/01/02',
        'result_pattern': 'OK'
    },
    {
        'id_user': '20130201',
        'id_voice': '20130201',
        'id_task': '20130201',
        'id_call': '20130201',
        'msg': 'Jennifer Acosta',
        'status': 0,  # 1: Đã xử lý, 2: Đang xử lý, 0: Không thành công
        'processing_time': 51,
        'audio_path': '/audio/audio1.wav',
        'audio_path_local': '/audio/audio1.wav',
        'content': 'Nextify',
        'update_at': '2021/01/02',
        'result_pattern': 'OK'
    }
]

tags = [
    {
        'id_user': '20130201',
        'name': 'Jennifer Acosta',
        'description': 'Edinburgh',
        'update_at': '2021/01/01'
    },
    {
        'id_user': '20130201',
        'name': 'Jennifer Acosta',
        'description': 'Edinburgh',
        'update_at': '2021/01/01'
    },
    {
        'id_user': '20130201',
        'name': 'Jennifer Acosta',
        'description': 'Edinburgh',
        'update_at': '2021/01/01'
    },
    {
        'id_user': '20130201',
        'name': 'Jennifer Acosta',
        'description': 'Edinburgh',
        'update_at': '2021/01/01'
    }
]

services = [
    {
        'id': '20130201',
        'name': 'Trial',
        'description': 'Edinburgh',
        'max_files': 10,
        'max_time_per_file': 120,
        'update_at': '2021/01/01'
    },
    {
        'id': '20130201',
        'name': 'VIP1',
        'description': 'Edinburgh',
        'max_files': 20,
        'max_time_per_file': 120,
        'update_at': '2021/01/01'
    },
    {
        'id': '20130201',
        'name': 'VIP2',
        'description': 'Edinburgh',
        'max_files': 30,
        'max_time_per_file': 120,
        'update_at': '2021/01/01'
    },
    {
        'id': '20130201',
        'name': 'VIP3',
        'description': 'Edinburgh',
        'max_files': 9999,
        'max_time_per_file': 99999,
        'update_at': '2021/01/01'
    }
]
# END DATABASE


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


@app.before_request
def before_request():
    g.user = None

    if 'user_name' in session:
        for x in users:
            if x.get('username') == session['user_name']:
                g.user = x
                break


@app.route('/', methods=['GET', 'POST'])
def index2():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_name=session['user_name'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_name', None)

        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user.get('username') == username and user.get('password') == password:
                session['user_name'] = user.get('username')
                return redirect(url_for('dashboard'))
        return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_name=session['user_name'])


@app.route('/client_add')
def client_add():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('client_add.html', user_name=session['user_name'], clients=clients)


@app.route('/client_delete')
def client_delete():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('client_delete.html', user_name=session['user_name'])


@app.route('/client_edit')
def client_edit():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('client_edit.html', user_name=session['user_name'])


@app.route('/index')
def index():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('index.html', user_name=session['user_name'])


@app.route('/manage_clients')
def manage_clients():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_clients.html', user_name=session['user_name'], clients=clients)


@app.route('/manage_services')
def manage_services():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_services.html', user_name=session['user_name'], services=services)


@app.route('/manage_speech_to_text_file')
def manage_speech_to_text_file():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_speech_to_text_file.html', user_name=session['user_name'], sttfiles=sttfiles)


@app.route('/manage_tags')
def manage_tags():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_tags.html', user_name=session['user_name'], tags=tags)


@app.route('/manage_voiceid')
def manage_voiceid():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('manage_voiceid.html', user_name=session['user_name'], voiceids=voiceids)


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


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
