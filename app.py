from models import *
from api import *
# -----------------------------------------------ERROR EXCEPTION ----------------------------------------------------------------

class NotFoundError(HTTPException):
    def __init__(self,status_code):
        self.response = make_response("Not Found",status_code)

class BussinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code" : error_code, "error_message" : error_message}
        self.response = make_response(json.dumps(message),status_code) 

# -------------------------------------------------------Home page(opening) ----------------------------------------------------
@app.route('/', methods=["POST","GET"])
def index():
    return render_template('index.html')

# --------------------------------------------------------sign up page-------------------------------------------------------
@app.route('/signup', methods=["POST","GET"])
def signup():
    if request.method=="GET":
        return render_template('signup.html')
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        data=User.query.filter(User.username==username).first()
        if data:
            flash('username already taken', category='error')
            return redirect(url_for('signup'))
        if not data:
            entry=User(username=username, password=password)
            db.session.add(entry)
            db.session.commit()
            return render_template('newuser.html')

        a = requests.post(BASE+f"/api/user",{"username":username,"password":password})
        if a.status_code==200:
            return render_template('newuser.html')
        else:
            flash('username already taken', category='error')
            return redirect(url_for('signup'))

#------------------------------------------------------Login page-------------------------------------------------------------------

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template('login.html')
    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')
        found_user = db.session.query(User).filter(User.username==user).first()
        if found_user:
            psd = db.session.query(User).filter(User.username==user,User.password==password).first()
            if psd:
                session['user'] = user
                flash('Login Successful!',category='success')
                return redirect(url_for('create_blog'))
            else:
                flash('Password is incorrect!',category='error')
        else:
            flash('User Not found, redirecting to sign up.....',category='error')
            return redirect(url_for('signup'))
    return render_template('login.html')

# function for login checking!
def login_check():
    if 'user' in session:
        return True
    else:
        return False 

# --------------------------------------- Blog ------------------------------------------------------------------------------------

@app.route('/createblog', methods=['GET','POST'])
def create_blog():
    if login_check():
        usr = session['user']
        user_obj=User.query.filter(User.username==usr).first()
        user_id = user_obj.id
        posts=Post.query.filter(Post.author==user_id).first()
        if posts==None:
            return render_template('nopost.html')
        return redirect(url_for('blog'))
    else:
        flash('please login to access this page.', category='info')
        return redirect(url_for('login')) 

@app.route('/blog', methods=['GET','POST'])
def blog():
    if login_check():
        usr=session['user']
        user_obj=User.query.filter(User.username==usr).first()
        user_id = user_obj.id
        if request.method=='POST':
            title = request.form.get('title')
            description = request.form.get('description')
            photos= request.files.getlist('photo[]')
            
            file_list = []
            for photo in photos:
                file_name = secure_filename(photo.filename)
                file_list.append(file_name)
                photo.save(os.path.join('static/photos/', file_name))
                
            if len(file_list) <= 4:
                if len(file_list) == 4:
                    p1 = file_list[0]
                    p2 = file_list[1]
                    p3 = file_list[2]
                    p4 = file_list[3]
                    posts = Post(title=title, description=description, author=user_id, photo1 = p1,photo2 = p2, photo3 = p3, photo4 = p4)   
                elif len(file_list) == 3:
                    p1 = file_list[0]
                    p2 = file_list[1]
                    p3 = file_list[2]
                    posts = Post(title=title, description=description, author=user_id, photo1 = p1,photo2 = p2, photo3 = p3)
                elif len(file_list) == 2:
                    p1 = file_list[0]
                    p2 = file_list[1]
                    posts = Post(title=title, description=description, author=user_id, photo1 = p1,photo2 = p2)
                else:
                    p1 = file_list[0]
                    posts = Post(title=title, description=description, author=user_id, photo1 = p1)
            else:
                flash('please select upto 4 images', category="error")
                return(redirect(url_for('blog')))

            db.session.add(posts)
            db.session.commit()    

            flash('Blog created!!', category='success')
            return redirect(url_for('home'))
        if request.method=='GET':        
            return render_template('posts.html')
    else:
        flash('please login to access this page.', category='info')
        return redirect(url_for('login'))

#---------------------------------------------------------------Profile--------------------------------------------------------------
@app.route("/profile")
def profile():
    if login_check():
        usr = session['user']
        user_obj=User.query.filter(User.username==usr).first()
        user_id = user_obj.id
        posts=Post.query.filter(Post.author==user_id).order_by(Post.datetime.desc()).all()
        return render_template('profile.html',user=user_obj,posts=posts)
    flash('please login to access this page.', category='info')
    return redirect(url_for('login'))


@app.route("/userblogs/<username>")
def userblogs(username):  
    if login_check():
        usr=session['user']
        user = User.query.filter(User.username==username).first()
        if user:
            posts=Post.query.filter(Post.author==user.id).order_by(Post.datetime.desc()).all()   
            return render_template('userblogs.html',user=user,posts=posts,usr=usr)
        flash(f'username : {username} doesnt exist!',category="error")
        return redirect(url_for('home'))
    flash('Login required!', category="error")
    return redirect(url_for('login'))


@app.route("/updateprofile", methods=["GET","POST"])
def updateprofile():
    if login_check():
        usr = session['user']
        user=User.query.filter(User.username==usr).one()
        user_one=db.session.query(User).filter(User.username==usr).first()
        if request.method == "GET":
            return render_template('updateprofile.html',user=user)
        if request.method == "POST":
            user_one.name = request.form.get('name')
            user_one.email = request.form.get('email')
            user_one.dob = request.form.get('dob')
            user_one.profession = request.form.get('prof')
            user_one.about_user = request.form.get('abt_usr')
            user_one.image = request.files.get('image')
            profile_pic = secure_filename(user_one.image.filename)
            user_one.image.save(os.path.join('static/profile/', profile_pic))
            user_one.image = profile_pic
            db.session.commit()
            flash('Your profile info has been set', category="info")
            return redirect(url_for('profile'))
    flash('Login required!', category="error")
    return redirect(url_for('login'))
        

# ------------------------------------------------------- View Blogs ---------------------------------------------------------
@app.route('/user/home', methods=['GET','POST'])
def home():
    if login_check():
        usr = session['user']
        usr = User.query.filter(User.username==usr).first()
        if request.method=='POST':
            s_un = request.form.get('s')
            u = User.query.filter(User.username.like('%'+s_un+'%')| User.username.like(s_un))
            return render_template('search.html', user = u)

        posts_of_followed = db.session.query(Post).select_from(Follows).filter(Follows.followingid==Post.author).filter(Follows.followerid == usr.id)
        mypost = Post.query.filter(Post.author==usr.id)
        uni = posts_of_followed.union(mypost)
        userfeed = uni.order_by(Post.datetime.desc()).all()
        return render_template("followedpost.html", pof = userfeed,user_name=usr.username)
    flash('Login required!', category="error")
    return redirect(url_for('login'))


@app.route('/user/view_post/<int:id>')
def view_post(id):
    if login_check():
        usr = session['user']
        usr = User.query.filter(User.username==usr).first().id
        blog = Post.query.get_or_404(id)
        return render_template('view_post.html', blog=blog , post=blog, usr=usr)
    flash('Login required!', category="error")
    return redirect(url_for('login'))

#------------------------------------------------------- Delete Blog--------------------------------------------------------------
@app.route('/posts/delete/<int:post_id>')
def deletepost(post_id):
    if login_check():
        delete_post=Post.query.get_or_404(post_id)
        usr = session['user']
        user_name = User.query.filter(User.username==usr).first()
        user_obj=user_name.id
        if user_obj == delete_post.author:
            try:
                db.session.delete(delete_post)
                db.session.commit()
                flash('Blog was deleted!!')
                return redirect(url_for('home'))
            except:
                flash('Problem occured while deleting, try again!!', category='info')
                return redirect(url_for('home'))
    flash('Login required!', category="error")
    return redirect(url_for('login'))


#------------------------------------- Update Blog -------------------------------------------------------------------
@app.route('/posts/update/<int:post_id>', methods=['GET','POST'])
def updatepost(post_id):
    if login_check():
        update_post=Post.query.filter(Post.post_id==post_id).one()
        if request.method == 'GET':
            title = update_post.title
            description = update_post.description
            return render_template('update_post.html',title=title,description=description)
        if request.method == 'POST':
            try:
                new_title=request.form.get('title')
                new_description=request.form.get('description')
                new_photos = request.files.getlist('photo[]')
                if new_photos:
                    file_list = []
                    for photo in new_photos:
                        file_name = secure_filename(photo.filename)
                        file_list.append(file_name)
                        photo.save(os.path.join('static/photos/', file_name))
                    if len(file_list) <= 4:
                        if len(file_list) == 4:
                                p1 = file_list[0]
                                p2 = file_list[1]
                                p3 = file_list[2]
                                p4 = file_list[3]
                                update_post.photo1=p1
                                update_post.photo2=p2
                                update_post.photo3=p3
                                update_post.photo4=p4
                        elif len(file_list) == 3:
                                p1 = file_list[0]
                                p2 = file_list[1]
                                p3 = file_list[2]
                                update_post.photo1=p1
                                update_post.photo2=p2
                                update_post.photo3=p3
                                update_post.photo4=None
                        elif len(file_list) == 2:
                                p1 = file_list[0]
                                p2 = file_list[1]
                                update_post.photo1=p1
                                update_post.photo2=p2
                                update_post.photo3=None
                                update_post.photo4=None
                        elif len(file_list) == 1:
                                p1 = file_list[0]
                                update_post.photo1=p1
                                update_post.photo2=None
                                update_post.photo3=None
                                update_post.photo4=None

                        update_post.title=new_title
                        update_post.description=new_description
                        db.session.commit()
                        flash('Post edited!',category='success')
                        return redirect(url_for('view_post',id=post_id))
                    else:
                        flash('Can update only 4 images', category="info")
                        return redirect(url_for('view_post',id=post_id))
            except:
                flash('Unable to update the post, try again!!',category="error")
                return redirect(url_for('view_post',id=post_id))
    flash('Login required!', category="error")
    return redirect(url_for('login'))
        

#--------------------------------------------------------Follow/Unfollow-------------------------------------------------------
@app.route('/follow/<string:username>')
def follow(username):
    if login_check():
        usr = session['user']
        user = User.query.filter(User.username==username).first()
        usr = User.query.filter(User.username==usr).first()
        if user:
            following = usr.following.filter(Follows.followingid==user.id).first() 
            if following == None:
                f = Follows(followerid=usr.id , followingid=user.id )
                db.session.add(f)
                db.session.commit()
                flash(f'Followed {username}', category="success")
                return redirect(url_for('userblogs', username=username))
            flash(f'Already Following {username}' , category="info")
            return redirect(url_for('userblogs', username=username))
        flash('Invaild username', category='error')
    flash('Login required!', category="error")
    return redirect(url_for('login'))

@app.route('/unfollow/<string:username>')
def unfollow(username):
    if login_check():
        usr = session['user']
        user = User.query.filter(User.username == username).first()
        usr = User.query.filter(User.username==usr).first()
        if user:    
            following = usr.following.filter(Follows.followingid==user.id).first()
            if following:
                db.session.delete(following)
                db.session.commit()
                flash(f'UnFollowed {username}', category="success")
                return redirect(url_for('userblogs', username=username))
            flash('User cannot be unfollowed without following!', category="error")
            return redirect(url_for('userblogs', username=username))
        flash('Invalid username',category="error")
    flash('Login required!', category="error")
    return redirect(url_for('login'))    
    
# --------------------------------------------------Followers/Following List -----------------------------------------------
@app.route('/<string:username>/followers')
def follower_list(username):
    if login_check():
        u = User.query.filter(User.username==username).first()
        if u:
            flr_list = u.followers.all()
            #print(flr_list)
            return render_template('flr_list.html',flr_list=flr_list, usr = u)
        flash('username doesn\'t exist',category="error")
        return redirect(url_for('home'))
    flash('Login required!', category="error")
    return redirect(url_for('login'))

@app.route('/<string:username>/following')
def fling_list(username):
    if login_check():
        u = User.query.filter(User.username==username).first()
        if u:
            fling_list = u.following.all()
            print(fling_list)
            return render_template('folling.html',fling_list=fling_list, usr = u)
        flash('username doesn\'t exist',category="error")
        return redirect(url_for('home'))
    flash('Login required!', category="error")
    return redirect(url_for('login'))

#List of followed posts with your post in home
@app.route('/followers/posts')
def f_posts():
    if login_check():
        usr = session['user']
        usr = User.query.filter(User.username==usr).first()
        posts_of_followed = db.session.query(Post).select_from(Follows).filter(Follows.followingid==Post.author).filter(Follows.followerid == usr.id)
        mypost = Post.query.filter(Post.author==usr.id).all()
        print(mypost)
        union = posts_of_followed.union(mypost)
        userfeed = union.order_by(Post.datetime.desc()).all()
        print(userfeed)
        return render_template("followedpost.html", pof = userfeed,user_name=usr.username)
    flash('Login required!', category="error")
    return redirect(url_for('login'))
    
#------------------------------------------------------------ Delete User permanetly-----------------------------------------------------------
@app.route('/delete/<int:id>', methods=['POST','GET'])
def delete_user(id):
    if login_check():
        usr = session['user']
        u_n = User.query.filter(User.username == usr).first()
        try:
            if id == u_n.id:
                delete_id = User.query.get_or_404(id)
                try:
                    if request.method == 'GET':
                        return render_template('del_u.html', user=u_n)
                    if request.method == "POST":
                        username = request.form.get('username') 
                        password = request.form.get('password')
                        if delete_id.id == u_n.id:
                            psd = User.query.filter(User.username==u_n.username,User.password==password).first()
                            if psd:
                                db.session.delete(delete_id)
                                db.session.commit()
                                #print('successful')
                                flash('Deactivated your Account successfully', category="success")
                                return redirect(url_for('index'))
                            
                            flash('Please enter correct credentials',category="error")
                            #print('no')
                            return render_template("del_u.html",user = u_n)
                except:
                    flash('Something went wrong :( Try Again!', category="error")
                    return (redirect(url_for('profile'))) 
        except:
            flash('Something went wrong :( Try Again!', category="error")
            return (redirect(url_for('login'))) 
    flash('Login required!', category="error")
    return redirect(url_for('login'))                


#-------------------------------------------------Add and Delete Comment-----------------------------------------------------------------------------
@app.route('/post/<int:post_id>/comment', methods=["POST"])
def cmt_create(post_id):
    if login_check():
        usr = session['user']
        usr = User.query.filter(User.username==usr).first()
        cmt = request.form.get('cmt')
        if cmt:
            p = Post.query.filter(Post.post_id==post_id)
            if p:
                cmmt = Comment(cmt_body=cmt,cmt_creater=usr.id,post_cmted=post_id)
                db.session.add(cmmt)
                db.session.commit()
                return redirect(url_for('view_post', id=post_id))
            flash('Post doesnt exsist', category="error")
            return redirect(url_for('view_post', id=post_id))
        return redirect(url_for('view_post', id=post_id))
    flash('Login required!', category="error")
    return redirect(url_for('login'))
            

@app.route('/delete/comment/<int:cmt_id>')
def cmt_delete(cmt_id):
    if login_check():
        usr=session['user']
        usr = User.query.filter(User.username==usr).first()
        cmt = Comment.query.filter(Comment.cmt_id==cmt_id).first() 
        user = Post.query.filter(Post.author==User.id).first()
        if cmt:
            if usr.id != cmt.cmt_creater:
                flash('cannot delete the comment as your not authorized')
            db.session.delete(cmt)
            db.session.commit()
            flash('successfully deleted comment', category='success')
        return redirect(url_for('home'))
    flash('Login required!', category="error")
    return redirect(url_for('login'))

@app.route('/post/like/<int:p_id>', methods=['GET'])
def likes(p_id):
    if login_check():
        usr=session['user']
        usr = User.query.filter(User.username==usr).first()
        pst_exist = Post.query.filter(Post.post_id == p_id)
        l = Like.query.filter(Like.liked_by==usr.id , Like.post_liked==p_id).first()

        if pst_exist:
            if not l :
                lk = Like(liked_by=usr.id,post_liked=p_id)
                db.session.add(lk)
                db.session.commit()
                return redirect(url_for('view_post',id=p_id))

            flash('already liked', category="info")
            return redirect(url_for('view_post',id=p_id))

        flash('blog doesnt exist',category="error")
        return redirect(url_for('view_post',id=p_id))

    flash('Login required!', category="error")
    return redirect(url_for('login'))

@app.route('/post/unlike/<int:p_id>', methods=['GET'])
def unlike(p_id):
    if login_check():
        usr=session['user']
        usr = User.query.filter(User.username==usr).first()
        pst_exist = Post.query.filter(Post.post_id == p_id)
        l = Like.query.filter(Like.liked_by==usr.id , Like.post_liked==p_id).first()

        if pst_exist:
            if l :
                db.session.delete(l)
                db.session.commit()
                return redirect(url_for('view_post',id=p_id))

            flash('Haven\'t like to unliked', category="info")
            return redirect(url_for('view_post',id=p_id))

        flash('blog doesnt exist',category="error")
        return redirect(url_for('view_post',id=p_id))

    flash('Login required!', category="error")
    return redirect(url_for('login'))

# ----------------------------------------- logout ----------------------------------------------------------------------------------        

@app.route('/logout', methods=["GET"])
def logout():
    if login_check():
        usr = session['user']
        flash(f'You have logged out {usr}!',category='info')
    session.pop('user',None)
    return redirect(url_for('login'))


if __name__=='__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')