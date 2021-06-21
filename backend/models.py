from . import db

class Featured(db.Model):
    __tablename__='featured'
    id = db.Column(db.Integer, primary_key=True)
    featured_description = db.Column(db.String(500), nullable=False)
  
    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}\n" 
        str =str.format( self.id, self.featured_description)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('movie_id',db.Integer,db.ForeignKey('movies.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'movie_id') )

class Movie(db.Model):
    __tablename__='movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),nullable=False)
    year = db.Column(db.Integer,nullable=False)
    genre = db.Column(db.String(64),nullable=False)
    director = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    featured = db.Column(db.Integer,nullable=False)
    
    def __repr__(self):
        str = "Id: {}, Title: {}, Year: {}, Genre: {}, Director: {}, Description: {}, Image: {}, Price: {}, Rating: {}, Featured: {}\n" 
        str =str.format( self.id, self.title, self.title, self.genre, self.director, self.description,self.image, self.price, self.rating, self.featured)
        return str

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    movies = db.relationship("Movie", secondary=orderdetails, backref="orders")
    
    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, Date: {}, Movies: {}, Total Cost: {}\n" 
        str =str.format( self.id, self.status,self.firstname,self.surname, self.email, self.phone, self.date, self.movies, self.totalcost)
        return str
