from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)


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
        'username': 'admin3',
        'password': 'admin3'
    }
]

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
    return redirect('/login')


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
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_name=session['user_name'])


@app.route('/client_add')
def client_add():
    return render_template('client_add.html')


@app.route('/client_delete')
def client_delete():
    return render_template('client_delete.html')


@app.route('/client_edit')
def client_edit():
    return render_template('client_edit.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/manage_clients')
def manage_clients():
    return render_template('manage_clients.html')


@app.route('/manage_services')
def manage_services():
    return render_template('manage_services.html')


@app.route('/manage_speech_to_text_file')
def manage_speech_to_text_file():
    return render_template('manage_speech_to_text_file.html')


@app.route('/manage_tags')
def manage_tags():
    return render_template('manage_tags.html')


@app.route('/manage_voiceid')
def manage_voiceid():
    return render_template('manage_voiceid.html')


@app.route('/service_add')
def service_add():
    return render_template('service_add.html')


@app.route('/voice_id_delete')
def voice_id_delete():
    return render_template('voice_id_delete.html')


@app.route('/voice_id_edit')
def voice_id_edit():
    return render_template('voice_id_edit.html')

@app.route('/blank')
def blank():
    return render_template('blank.html')


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
