from apis import *

class UserLogin(Resource):
    def get(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def post(self):

        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                return 'Logged in successfully', 200
            else:
                raise incorrect_login(status_code=404, errorin='Password')
        else:
            raise incorrect_login(status_code=404, errorin='Username')

    def put(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def delete(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')

class UserSignup(Resource):
    def get(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')

    def post(self):
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']
        name = request.get_json()['name']
       
        phn = request.get_json()['phn']
    
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
           raise UserExists(status_code=404, errorin='Username')

        emailval = User.query.filter_by(email=email).first()
        if emailval:
            raise UserExists(status_code=404, errorin='Email')
            
        # Create new user
        new_user = User(username=username, email=email, name=name, phn=phn, password=password)
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return 'User Created', 200
    
    def put(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def delete(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')

class UserLogout(Resource):
    def get(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
        # return 'Logged out successfully', 200
    
    def post(self):
        print(current_user)
        logout_user()
        # raise request_not_allowed(status_code=404, messasge='Not a valid request method')
        return {
            'message' : 'Logged out successfully'
        }, 200

    def put(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def delete(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
