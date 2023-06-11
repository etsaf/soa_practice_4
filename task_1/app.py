from flask import Flask, jsonify, abort, request, make_response, url_for

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
