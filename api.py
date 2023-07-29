from models import *

#API - CREATE,READ,DELETE ON USER
#API - READ,DELETE ON POST


class NotFoundError(HTTPException):
    def __init__(self,status_code):
        self.response = make_response("Not Found",status_code)

class BussinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code" : error_code, "error_message" : error_message}
        self.response = make_response(json.dumps(message),status_code)

user = {
    "id" : fields.Integer,
    "username" : fields.String,
    "name" : fields.String,
    "email" : fields.String,
    "image" : fields.String
    
}

posts = {
    "title":fields.String,
    "description":fields.String,
    "photo1":fields.String,
    "photo2":fields.String,
    "photo3":fields.String,
    "photo4":fields.String,
}

create_user = reqparse.RequestParser()
create_user.add_argument("username")
create_user.add_argument("password")

class UserAPI(Resource):
    @marshal_with(user)
    def get(self,username):
        user = User.query.filter(User.username==username).first()
        if user:
            return user
        else:
            raise NotFoundError(status_code=404)


    def post(self):
        args = create_user.parse_args()
        username=args.get("username")
        password=args.get("password")

        if username:
            data=User.query.filter(User.username==username).first()
            if not data:
                entry=User(username=username, password=password)
                db.session.add(entry)
                db.session.commit()
                print('done')
                return ("User created successfully",200)

            else:
                raise BussinessValidationError(status_code=401,error_code="BE1002", error_message="username already exists")
        else:
            raise BussinessValidationError(status_code=400,error_code="BE1001", error_message="username cant be empty")

    def delete(self,username):
        usr = User.query.filter(User.username==username).first()
        if usr:
            psd = User.query.filter(User.username==username,User.password==usr.password).first()
            if psd:
                db.session.delete(usr)
                db.session.commit()
                return ("Deleted Successfully",202)
            else:
                raise NotFoundError(404)
        return ('User Not Found',404)

class PostAPI(Resource):
    @marshal_with(posts)
    def get(self,username):
        usr = User.query.filter(User.username==username).first()
        if usr:
            posts = Post.query.filter(Post.author==usr.id).all()
            if posts:
                return posts
            else:
                raise NotFoundError(404)
        raise NotFoundError(404)
                

    def delete(self,username,title):
        usr = User.query.filter(User.username==username).first()
        post = Post.query.filter(Post.author==usr.id, Post.title==title).first()
        if post:
            del_post = Post.query.filter(Post.author==usr.id, Post.post_id==post.post_id).all()
            if del_post:
                db.session.delete(del_post[0])
                db.session.commit()
                return("Deleted Successfully",202)
            return ('Post Not Found',404)
        return (f'No post with title : {title}',404)
        



api.add_resource(UserAPI, '/api/user','/api/user/<string:username>')
api.add_resource(PostAPI, '/api/post/<string:username>','/api/post/<string:username>/<string:title>')
