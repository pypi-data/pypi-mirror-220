# Zylo

Zylo is a lightweight web framework made with love.

## Features

- Simple and intuitive routing
- Template rendering using Jinja2
- Session management with the sessions library
- Static file serving

## Installation

You can install Zylo using pip:


```bash
pip install zylo

```

## Usage

```python
from zylo import Zylo

app = Zylo()

@app.route('/')
def home(request):
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
 
```

## changelogs

- Beta version 2.0.3
- Latest update of beta
- Bug fixed with update --> 2.0.3
- Updated Usage Guide 1.2.1
- Addedd more functions & Bug Fixes
- Bug fixes in Zylo
- Mailer updated to --> 1.0.3

```python

from zylo.limiter import Limiter, render_template

app = Zylo(__name__)
limiter = Limiter(app)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit('10/minutes')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

```

## Blueprint

```python

from zylo import Zylo, Response
from zylo.blueprint import Blueprint

app = Zylo(__name__)
blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/')
def home(request):
    return Response("Welcome to ZYLO blueprint route")

app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run()

```

## Sessions

```python

from zylo import Zylo, Response, render_template, redirect

app = Zylo(__name__)

@app.route('/')
def home(request):
    session = request.session
    session['id'] = 123
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard(request):
    session = request.session
    id = session.get('id')
    return render_template('dashboard.html', id=id)

@app.route('/logout')
def logout(request):
    request.session.clear()
    return Response("You have been successfully logged out")

if __name__ == "__main__":
    app.run()

```

## JwT

```python

from zylo.JwT import JwT, error_handler

jwt = JwT()

try:
    payload = {'user_id': 123, 'role': 'admin'}
    access_token = jwt.create_payload(payload, algorithm="HS256", time_limit_hours=1)

    decoded_payload = jwt.verify_payload(access_token)
    id = decoded_payload['user_id']
    print(f"id: {id}")

except Exception as e:
    error_message = error_handler(e)
    print('Error:', error_message)

```

## Limiter

```python

from zylo import Zylo, Response
from zylo.limiter import Limiter

app = Zylo(__name__)
limiter = Limiter(app)

@app.route('/')
@limiter.limit(limit=5, period=60)
def home(request):
    return Response("Limited route")

if __name__ == "__main__":
    app.run()

```

## Mailer

```python

from zylo import Zylo, Response
from zylo.mailer import Mailer

mailer = Mailer()
app = Zylo(__name__)

// Mailer config
mailer.config['SMTP'] = 'SMTP'
mailer.config['SMTP_PORT'] = 'SMTP_PORT'
mailer.config['SENDER_EMAIL'] = 'SENDER_EMAIL'
mailer.config['DEFAULT_SENDER'] = 'DEFAULT_SENDER'
mailer.config['SENDER_PASSWORD'] = 'SENDER_PASSWORD'
mailer.config['SSL'] = True
mailer.config['SSL_SECURITY'] = True

@app.route('/')
def home(request):
    email = "demo@demo.com"
    subject = "Welcome to ZYLO"
    body = "A user-friendly python web framework made with love"

    mail = mailer.send_email(email, subject, body)
    if mail:            
        return Response(f"Mail sent successfully to {email}")
    return Response("Something went wrong while sending email")

if __name__ == "__main__":
    app.run()

```

## Chiper

```python

// Input sanitization
from zylo.chiper import sanitize_input

name = "'name1'"
san_name = sanitize_input(name)
print(san_name)  // output --> name1

// Generate ID
from zylo.chiper import generate_id

print(generate_id(11))  // length defined 11, output --> y-909716817

// Secure password validation
from zylo.chiper import is_secure_password

password = "123"
sec_password = "secpassword@0000"

print(is_secure_password(password))  // output --> False
print(is_secure_password(sec_password))  // output --> True

// Email validation
from zylo.chiper import validate_email

print(validate_email("demo@1"))  // output -->
print(validate_email("email@email.com"))  // output --> True

// Hashing and verifying passwords
from zylo.chiper import hash_password, verify_password

pswd = "mypassword"
hashed_password = hash_password(pswd)
print(hashed_password)  // output --> $zylo.chiper@9e8b057a1f8e43c9e0d8d20769c8f516b5ba419998b5ed6fb877452db4c46049b2bd9560da6fef2c3afb047485cebfbab5cad85787b2be1de820ca5ee42ba3bcfb37c6395dcf4e27abf6a02d1926197a

print(verify_password(pswd, hashed_password))  // output --> True

```