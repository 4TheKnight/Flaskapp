from flask import Flask, render_template,request,flash,redirect,url_for
from models import db, Property, User,PropertyImage
from sqlalchemy.exc import OperationalError
from flask_bcrypt import Bcrypt,bcrypt
from forms import RegistrationForm,Loginform,PropertyForm,adminRegistrationForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///properties.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



db.init_app(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app, db)

login_manager.login_view='login'

app.secret_key="your_secret_key"
admin_secret_key ="admin123" 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_tables():
    try:
        # Use SQLAlchemy's inspector to check if the table exists
        inspector = db.inspect(db.engine)
        if 'properties' not in inspector.get_table_names():
            db.create_all()
            print("Table 'properties' created.")
        else:
            print("Table 'properties' already exists.")
    except OperationalError as e:
        print(f"Error during table check/creation: {e}")

@app.route('/login',methods=['GET','POST'])
def login():
    form = Loginform()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, password):
            login_user(existing_user)
            return redirect(url_for('home'))
        else:
            return('username or password invalid')
    return render_template('login.html',form = form)


@app.route('/admin_register',methods = ['GET','POST'])
def admin_register():
    form=adminRegistrationForm()
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        adminkey = request.form['adminkey']
        if adminkey==admin_secret_key:

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return ('User already exists')
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(username=username,password=hashed_password,admin=True)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for('home'))
        
        else: return('You are not authorised to be admin')
    return render_template('admin_register.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return('user already exists')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

    
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/delet_user', methods=['POST'])
@login_required
def delete_user():
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return redirect(url_for('login'))
    
@app.route('/deletepost/<int:id>',methods=['POST'])
def deletepost(id):
    if request.method=="POST":
        if(current_user.admin==True):
            post = Property.query.filter_by(id=id).first()
            for image in post.images:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.image_file)
                if os.path.exists(image_path):
                    os.remove(image_path)
                db.session.delete(image)
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return('dont fuck with my system')

@app.route('/makepost',methods = ['GET','POST'])
@login_required
def makepost():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
    form = PropertyForm()
    if(current_user.admin==True):
        if request.method=="POST":
            contact_email = request.form['contact_email']
            contact_number = request.form['contact_number']
            location = request.form['location']
            price = request.form['price']
            bedrooms = request.form['bedrooms']
            bathrooms = request.form['bathrooms']
            carpet_area = request.form['carpet_area']

            new_post = Property(
                contact_email=contact_email,
                contact_number=contact_number,
                location=location,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                carpet_area=carpet_area
                )
            
            db.session.add(new_post)
            db.session.commit()
            
            images = form.images.data
            for image in images:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

                new_image = PropertyImage(
                    property_id=new_post.id,
                    image_file = filename
                )
                db.session.add(new_image)
            
            db.session.commit()
            return redirect (url_for('home'))
        return render_template('create_property.html',form=form)
    else:
        return('Stop fucking around my system')

@app.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('register'))


@app.route('/',methods=['GET','POST'])
@login_required
def home():
    post = Property.query.all()
    if(str(current_user.admin)=='True'):
        return render_template('index.html',data={current_user.username},admin=True,post=post)
    else:
        return render_template('index.html',data={current_user.username},admin=False,post=post)



with app.app_context():
    db.drop_all()
    create_tables()


if __name__=="__main__":
    app.run(debug=True)
