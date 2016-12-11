from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class login_data(db.Model):
    __tablename__ = 'user'
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    user_id=db.Column(db.Integer, primary_key=True)

    def __init__(self, username,password):
        self.username = username
        self.password = password

class post_data(db.Model):
    __tablename__ = 'post'
    id=db.Column(db.Integer,primary_key=True)
    post=db.Column(db.String(1000))
    title=db.Column(db.String(50))
    tags=db.Column(db.String(50))
    date=db.Column(db.DateTime(100))
    user_id=db.Column(db.Integer)

    def __init__(self, post,title,tags,date,user_id):
        self.post = post
        self.title = title
        self.tags = tags
        self.date = date
        self.user_id = user_id