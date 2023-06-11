from flask import Flask, jsonify, abort, request, make_response, url_for, send_file
from fpdf import FPDF
from PIL import Image
import io

app = Flask(__name__, static_url_path = "")

def get_picture(filename):
    if filename == "":
        return []
    with open(filename, "rb") as picture:
        f = picture.read()
        b = bytearray(f)
        return b

users = [
    {
        'id': 1,
        'name': u'John',
        'gender': u'Male', 
        'email': 'johntheguy',
        'picture': get_picture('miles.jpg')
    },
    {
        'id': 2,
        'name': u'Doe',
        'gender': u'Female', 
        'email': 'doethegirl',
        'picture': []
    }
]

pdfs = {}

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_user', user_id = user['id'], _external = True)
        elif field == 'picture':
            new_user[field] = 'picture hidden'
        else:
            new_user[field] = user[field]
    return new_user


@app.route('/')
def index():
    return "Hello, World!"
    

@app.route('/profiles/api/v1.0/users', methods = ['GET'])
def get_users():
    return jsonify( { 'users': list(map(make_public_user, users)) } )


@app.route('/profiles/api/v1.0/users/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    user = list(filter(lambda u: u['id'] == user_id, users))
    print(user)
    if len(user) == 0:
        abort(404)
    return jsonify( { 'user': make_public_user(user[0]) } )



@app.route('/profiles/api/v1.0/users', methods = ['POST'])
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'name': request.json['name'],
        'gender': request.json.get('gender', ""),
        'email': request.json.get('email', ""),
        'picture': get_picture(request.json.get('picture', ""))
    }
    users.append(user)
    return jsonify( { 'user': make_public_user(user) } ), 201


@app.route('/profiles/api/v1.0/users/<int:user_id>', methods = ['PUT'])
def update_user(user_id):
    user = list(filter(lambda u: u['id'] == user_id, users))
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != type(u''):
        abort(400)
    if 'gender' in request.json and type(request.json['gender']) != type(u''):
        abort(400)
    if 'email' in request.json and type(request.json['email']) != type(u''):
        abort(400)
    user[0]['name'] = request.json.get('name', user[0]['name'])
    user[0]['gender'] = request.json.get('gender', user[0]['gender'])
    user[0]['email'] = request.json.get('email', user[0]['email'])
    new_picture = get_picture(request.json.get('picture', ""))
    if new_picture != []:
        user[0]['picture'] = new_picture
    return jsonify( { 'user': make_public_user(user[0]) } )


@app.route('/profiles/api/v1.0/users/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    user = list(filter(lambda u: u['id'] == user_id, users))
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify( { 'result': True } )

@app.route('/profiles/api/v1.0/users/pdf/<int:user_id>', methods = ['GET'])
def get_pdf(user_id):
    static_file = open("/"+str(user_id)+".pdf", 'rb')
    return send_file(static_file, mimetype="attachment/pdf")

@app.route('/profiles/api/v1.0/users/make_pdf/<int:user_id>', methods = ['POST'])
def make_pdf(user_id):
    user = list(filter(lambda u: u['id'] == user_id, users))
    if len(user) == 0:
        abort(404)
    user = user[0]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    name_text = "Name: " + user['name']
    pdf.cell(200, 10, txt = name_text,
            ln = 1, align = 'C')
    gender_text = "Gender: " + user['gender']
    pdf.cell(200, 10, txt = gender_text,
            ln = 2, align = 'C')
    email_text = "E-mail: " + user['email']
    pdf.cell(200, 10, txt = email_text,
            ln = 2, align = 'C')
    if user['picture'] != []:
        img = Image.open(io.BytesIO(user['picture']))
        img.save('/img.jpg')
        pdf.image('/img.jpg')
    else:
        pdf.cell(200, 10, txt = "no picture yet :(",
            ln = 2, align = 'C')
    pdf.output("/"+str(user_id)+".pdf")
    return jsonify( { 'pdf': url_for('get_pdf', user_id = user['id'], _external = True) } )