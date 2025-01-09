from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return f"Email: {email}, Password: {password}"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
