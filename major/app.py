from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# In-memory user storage (for demo purposes only)
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')

    if not email or not password:
        flash('Please fill in all fields', 'error')
        return redirect(url_for('index'))

    user = users.get(email)

    if user and user['password'] == password:
        session['user'] = email
        session.permanent = True if remember else False
        flash('Logged in successfully!', 'success')
        return redirect(url_for('welcome'))
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    agree_terms = request.form.get('agree_terms')

    if not all([name, email, phone, password, confirm_password]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('index'))

    if not agree_terms:
        flash('You must agree to the terms and conditions', 'error')
        return redirect(url_for('index'))

    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('index'))

    if len(password) < 6:
        flash('Password must be at least 6 characters long', 'error')
        return redirect(url_for('index'))

    if email in users:
        flash('Email already registered. Please log in.', 'error')
        return redirect(url_for('index'))

    # Save user to the in-memory store
    users[email] = {
        'name': name,
        'email': email,
        'phone': phone,
        'password': password,
    }

    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('index'))

@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    user_info = users.get(session['user'], {})
    return render_template('welcome.html', user=user_info)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
