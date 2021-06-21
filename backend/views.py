from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Movie, Featured, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db


bp = Blueprint('main', __name__)

@bp.route('/')

def index():
    movies = Movie.query.order_by(Movie.rating.desc()).limit(4).all()
    return render_template('index.html', movies = movies)

@bp.route('/all')

def all():
    movies = Movie.query.order_by(Movie.title).all()
    return render_template('page.html',  movies = movies)


@bp.route('/horror')

def horror():
      movies = Movie.query.filter(Movie.genre.endswith('horror')).all()
      return render_template('page.html',  movies = movies)


@bp.route('/superhero')

def superhero():
      movies = Movie.query.filter(Movie.genre.endswith('superhero')).all()
      return render_template('page.html',  movies = movies)


@bp.route('/comedy')

def comedy():
    movies = Movie.query.filter(Movie.genre.endswith('comedy')).all()
    return render_template('page.html',  movies = movies)



@bp.route('/scifi')

def scifi():
      movies = Movie.query.filter(Movie.genre.endswith('Sci-Fi')).all()
      return render_template('page.html',  movies = movies)

@bp.route('/M.NightShyamalan')

def mnight():
      movies = Movie.query.filter(Movie.director.endswith('M. Night Shyamalan')).all()
      return render_template('page.html',  movies = movies)

@bp.route('/JeffWadlow')

def wadlow():
      movies = Movie.query.filter(Movie.director.endswith('Jeff Wadlow')).all()
      return render_template('page.html',  movies = movies)

@bp.route('/desc')

def desc():
    movies = Movie.query.order_by(Movie.title.desc()).all()
    return render_template('page.html', movies = movies)

@bp.route('/aesc')

def aesc():
    movies = Movie.query.order_by(Movie.title.asc()).all()
    return render_template('page.html', movies = movies)


@bp.route('/featured')

def rating():
    movies = Movie.query.filter(Movie.featured.endswith('1')).all()
    return render_template('page.html', movies = movies)

@bp.route('/oldest')

def oldest():
    movies = Movie.query.order_by(Movie.year.asc()).all()
    return render_template('page.html', movies = movies)

@bp.route('/newest')

def newest():
    movies = Movie.query.order_by(Movie.year.desc()).all()
    return render_template('page.html', movies = movies)



@bp.route('/<movies>')

def details(movies):
    movies = Movie.query.filter(Movie.title == movies)
    return render_template('details.html',  movies = movies)



@bp.route('/search')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    movies = Movie.query.filter(Movie.description.contains(search) | Movie.title.contains(search))
    if search == "":
            movies = Movie.query.order_by(Movie.year.desc()).all()
    else:
        movies = Movie.query.filter(Movie.description.contains(search) | Movie.title.contains(search))
    return render_template('page.html',  movies = movies)



# Referred to as "Basket" to the user
@bp.route('/order', methods=['POST','GET'])
def order():
    movie_id = request.values.get('movie_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for movie in order.movies:
            totalprice = totalprice + movie.price
    
    # are we adding an item?
    if movie_id is not None and order is not None:
        movie = Movie.query.get(movie_id)
        if movie not in order.movies:
            try:
                order.movies.append(movie)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.order'))
    
    return render_template('order.html', order = order, totalprice = totalprice)


# Delete specific basket items
@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        movie_to_delete = Movie.query.get(id)
        try:
            order.movies.remove(movie_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))


# Scrap basket
@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.order'))


@bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for movie in order.movies:
                totalcost = totalcost + movie.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                return redirect('/success')
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form = form)

@bp.route('/success')

def success():
 
    return render_template('success.html')