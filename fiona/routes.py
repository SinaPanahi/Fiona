from flask import render_template, redirect, url_for, flash, request, session, Markup
from fiona import app, db, mail
from fiona.models import User, Painting, Message, Post, Shopping_Cart_Item, Website, Painting_Photo
from werkzeug.security import check_password_hash, generate_password_hash
from fiona.utilities import Flash_Messages, validate_email, validate_password, generate_activation_token, create_activation_email

@app.route('/')
def home():
    website = Website.query.first()
    title = website.name
    carousel = Painting.query.filter(Painting.is_carousel_item == True).all()
    posts = Post.query.all()
    return render_template('home.html', website=website, title=title, carousel=carousel, posts=posts)

@app.route('/sign-up', methods=['GET','POST'])
def sign_up():

    if 'user_id' in session:
        flash('You are already signed in.', Flash_Messages.Warning)
        return redirect(url_for('home'))
    
    elif request.method == 'GET':
        website = Website.query.first()
        title = website.name + ' | Sign Up'
        return render_template('sign_up.html', title=title, website=website)
    
    elif request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        confirm_password = request.form.get('confirm-password').strip()
        activation_token = generate_activation_token()

        user = User.query.filter_by(email=email).first()

        if user: 
            flash(Markup(f'{email}" is already a member. <a href="sign-in">Sign In</a> to continue.'), Flash_Messages.Warning)
            return redirect(url_for('sign_up'))
        
        elif password != confirm_password:
            flash("The passwords are not the same.", Flash_Messages.error)
            return redirect(url_for('sign_up'))
        
        elif not validate_email(email):
            flash("Invalid email address.", Flash_Messages.error)
            return redirect(url_for('sign_up'))
        
        elif not validate_password(password):
            flash("Invalid password.", Flash_Messages.error)
            return redirect(url_for('sign_up'))
        
        else:
            password = generate_password_hash(password)
            user = User(email, password, activation_token)
            db.session.add(user)
            db.session.commit()

            website = Website.query.first()
            message = create_activation_email(website, user)
            mail.send(message)

            flash(f"Sign up successful. Activation email sent to: {email}.", Flash_Messages.info)
            return redirect(url_for('sign_in'))
        
@app.route('/sign-in', methods=['GET','POST'])
def sign_in():

    if 'user_id' in session:
        flash('You are already signed in.', Flash_Messages.Warning)
        return redirect(url_for('home'))
    
    elif request.method == 'GET':
        website = Website.query.first()
        title = website.name + ' | Sign In'
        return render_template('sign_in.html', title=title, website=website)
    
    elif request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Incorrect credentials.", Flash_Messages.error)
            return redirect(url_for('sign_in'))
        
        elif check_password_hash(user.password, password):
            if not user.is_activated:
                flash("Please, activate your account to continue.", Flash_Messages.Warning)
                return redirect(url_for('sign_in'))
            elif user.is_admin:
                session['user_id'] = user.id
                session['is_admin'] = True
                flash(Markup(f'Welcome to the admin panel, "{email}".'), Flash_Messages.info)
                return redirect(url_for('website'))
            else: 
                session['user_id'] = user.id
                flash(Markup(f'Welcome, "{email}".'), Flash_Messages.info)
                return redirect(url_for('home'))
        else:
            print(check_password_hash(user.password, password))
            print(user.password)
            print(password)
            flash("Incorrect credentials.", Flash_Messages.error)
            return redirect(url_for('sign_in'))
                        
@app.route('/reset-password', methods=['GET','POST'])
def reset_password():

    if 'user_id' in session:
        flash('You are already signed in.', Flash_Messages.Warning)
        return redirect(url_for('home'))
        
    elif request.method == 'GET':
        website = Website.query.first()
        title = website.name + ' | Reset Password'
        return render_template('reset_password.html', title=title, website=website)
    
    elif request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        confirm_password = request.form.get('password').strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Incorrect credentials.", Flash_Messages.error)
            return redirect(url_for('reset_password'))
        
        elif confirm_password != password:
            flash("Passwords are not the same.", Flash_Messages.error)
            return redirect(url_for('reset_password'))
        
        elif not validate_password(password):
            flash("Invalid password.", Flash_Messages.error)
            return redirect(url_for('reset_password')) 
        
        else:
            user.password = generate_password_hash(password)
            user.is_activated = False
            db.session.commit()

            website = Website.query.first()
            message = create_activation_email(website, user)
            mail.send(message)

            flash(f"Password reset successful. Activation email sent to: {user.email}.", Flash_Messages.info)
            return redirect(url_for('sign_in'))

@app.route('/gallery')
def gallery():
    website = Website.query.first()
    title = website.name + ' | Gallery'
    paintings = Painting.query.all()
    return render_template('gallery.html', website=website, title=title, paintings=paintings)

@app.route('/gallery/<painting_id>')
def painting(painting_id):
    website = Website.query.first()
    title = website.name + ' | Painting'
    
    if not painting_id:
        flash('Invalid request.', Flash_Messages.error)
        return redirect(url_for('home'))

    painting = Painting.query.filter_by(id=painting_id).first()
    painting_photos = Painting_Photo.query.filter_by(painting_id=painting_id).all()
    return render_template('painting_photos.html', website=website, title=title, painting=painting, painting_photos=painting_photos)


@app.route('/privacy-policy')
def privacy_policy():
    website = Website.query.first()
    title = website.name + ' | Privacy Policy'
    return render_template('privacy_policy.html', title=title, website=website)

@app.route('/terms-of-use')
def terms_of_use():
    website = Website.query.first()
    title = website.name + ' | Terms of User'
    return render_template('terms_of_use.html',title=title, website=website)

@app.route('/about')
def about():
    website = Website.query.first()
    title = website.name + ' | About'
    return render_template('about.html', title=title, website=website)

@app.route('/contact', methods=['GET','POST'])
def contact():

    if request.method == 'GET':
        website = Website.query.first()
        title = website.name + ' | Contact'
        subject = request.args.get('subject').replace('-', ' ').title().strip() if request.args.get('subject') else ''
        return render_template('contact.html', website=website, title=title, subject=subject)
    
    elif request.method == 'POST':
        subject = request.form.get('subject').replace('-', ' ').title() if request.form.get('subject') else 'No Subject'
        email = request.form.get('email').strip()
        message = request.form.get('message')

        if not validate_email(email):
            flash('Invalid email address.', Flash_Messages.error)
            return redirect(url_for('contact'))
        
        elif not message or message == '':
            flash('Message field is mandatory.', Flash_Messages.error)
            return redirect(url_for('contact'))
        
        else: 
            message = Message(email, subject, message)
            db.session.add(message)
            db.session.commit()
            flash('Your message was successfully sent.', Flash_Messages.info)
            return redirect(url_for('contact'))

@app.route('/shopping-cart')
def shopping_cart():

    if not 'user_id' in session:
        flash('Sign in to continue.', Flash_Messages.info)
        return redirect(url_for('sign_in'))
    
    else:
        website = Website.query.first()
        title = website.name + ' | Shopping Cart'

        user_id = session['user_id']
        shopping_cart_items = Shopping_Cart_Item.query.filter_by(user_id=user_id).all()
        paintings = []
        for item in shopping_cart_items:
            painting = Painting.query.filter_by(id = item.painting_id).first()
            paintings.append(painting)
        return render_template('shopping_cart.html', website=website, title=title, paintings=paintings)

       
      
