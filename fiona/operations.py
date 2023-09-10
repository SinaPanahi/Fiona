import os
from flask import redirect, url_for, flash, request, session, jsonify, render_template
from fiona import app, db
from fiona.models import User, Painting, Message, Post, Shopping_Cart_Item, Painting_Photo
from fiona.utilities import Flash_Messages, generate_activation_token

@app.route('/sign-out')
def sign_out():
    if 'user_id' in session:
        session.clear()
        flash('Sign out successful.', Flash_Messages.info)
        return redirect(url_for('sign_in'))
    else:
        flash('You are not signed in.', Flash_Messages.Warning)
        return redirect(url_for('home'))
  
@app.route('/activate-account/<email>/<activation_token>')
def activate_account(email, activation_token):
    
    if request.method == 'GET' and email and activation_token:
        user = User.query.filter_by(email=email).first()
        if user and user.activation_token == activation_token:
            # Update activation token for the next time
            user.activation_token = generate_activation_token()
            user.is_activated = True
            db.session.commit()
            flash('Account activated. Sign in to continue.', Flash_Messages.info)
            return redirect(url_for('sign_in'))
        else:
            flash('Invalid request', Flash_Messages.error)
            return redirect(url_for('home'))
    else:
        flash('Invalid request', Flash_Messages.error)
        return redirect(url_for('home'))
        

# UNTIL HERE  
@app.route('/add-to-cart', methods=['GET', 'POST'])
def add_to_cart():
    # The add-to-cart route will respond to both GET and POST requests.
    # Normally, the items will be added to the cart using the JS fetch API with a POST request
    # However the GET section will also work even if JS is disabled.

    # Regardless of the method, the user can not use this route if they are not signed in
    if not 'user_id' in session:
        flash('Sign in to continue.', Flash_Messages.info)
        return redirect(url_for('sign_in'))

    # The user is signed in and is using GET (no Javascript fetch API)
    elif 'user_id' in session and request.method == "GET":
        painting_id = request.args.get('painting_id')
        user_id = session['user_id']

        # First check if the item is already in the cart
        shopping_cart_item = Shopping_Cart_Item.query.filter_by(user_id=user_id, painting_id=painting_id).first()
        
        # If the item is already in the users cart they will be returned to gallery
        if shopping_cart_item:
            flash('The item is already in your shopping card.', Flash_Messages.Warning)
            return redirect(url_for('gallery'))
        
        # If the item is NOT in the users cart, it will be added and the user will be returned to gallery
        # whatever page they made their request from
        elif not shopping_cart_item:
            shopping_cart_item = Shopping_Cart_Item(user_id, painting_id)
            db.session.add(shopping_cart_item)
            db.session.commit()
            flash('The item was added successfully to your shopping cart.', Flash_Messages.info)
            return redirect(url_for('gallery'))

    # The user is signed in and is using POST (Javascript fetch API)
    elif 'user_id' in session and request.method == "POST":
        painting_id = request.get_json()['painting_id']
        user_id = session['user_id']
        # First check if the item is already in the cart
        shopping_cart_item = Shopping_Cart_Item.query.filter_by(user_id=user_id, painting_id=painting_id).first()
        if shopping_cart_item:
            # Do not do anything. Just ignore!
            return jsonify(['The item is already in your shopping card.', Flash_Messages.Warning])
        # Add the item to the cart
        else:
            shopping_cart_item = Shopping_Cart_Item(user_id, painting_id)
            db.session.add(shopping_cart_item)
            db.session.commit()
            return jsonify(['The item was added successfully to your shopping cart.', Flash_Messages.info])
    
@app.route('/remove-from-cart', methods=['GET', 'POST'])
def remove_from_cart():
    # The remove-from-cart route will respond to both GET and Post requests.
    # Normally, the items will be removed from the cart using the JS fetch API with a POST request
    # However the GET section will also work even if JS is disabled.

    # Regardless of the method, the user can not use this route if they are not signed in
    if not 'user_id' in session:
        flash('Sign in to continue.', Flash_Messages.info)
        return redirect(url_for('sign_in'))
    
    # The user is signed in and is using GET (no Javascript fetch API)
    elif 'user_id' in session and request.method == "GET":
        painting_id = request.args.get('painting_id')
        user_id = session['user_id']

        # First check if the item is already in the cart
        shopping_cart_item = Shopping_Cart_Item.query.filter_by(user_id=user_id, painting_id=painting_id).first()

        # If the item is in the users cart, it will be removed and the user will be returned to gallery
        if shopping_cart_item:
            db.session.delete(shopping_cart_item)
            db.session.commit()
            flash('The item was successfully removed from your cart', Flash_Messages.info)
            return redirect(url_for('shopping_card'))
        # If the item is NOT in the users cart, the request will be ignore and the user will be returned to gallery
        elif not shopping_cart_item:
            flash('Invalid request', Flash_Messages.error)
            return redirect(url_for('gallery'))

    # The user is signed in and is using POST (Javascript fetch API)
    elif 'user_id' in session and request.method == "POST":
        painting_id = request.get_json()['painting_id']
        user_id = session['user_id']
        # First check if the item is already in the cart
        shopping_cart_item = Shopping_Cart_Item.query.filter_by(user_id=user_id, painting_id=painting_id).first()
        if shopping_cart_item:
            db.session.delete(shopping_cart_item)
            db.session.commit()
            return jsonify(['The item was successfully removed from your cart', Flash_Messages.info, painting_id])
        else:
            # Do not do anything. Just ignore!
            return jsonify(['Invalid request', Flash_Messages.error])
        
@app.route('/delete-message')
def delete_message():
    if 'user_id' in session and 'is_admin' in session:
        if request.args.get('message_id'):
            message_id = request.args.get('message_id')
            message = Message.query.filter_by(id = message_id).first()
            db.session.delete(message)
            db.session.commit()
            flash('The message was successfully deleted.', Flash_Messages.info)
            return redirect(url_for('messages'))
        else:
            flash('Invalid Request.', Flash_Messages.error)
            return redirect(url_for('messages'))
    else: 
        return render_template('404.html', title='404 - Not Found')
    
@app.route('/mark-message-read')
def mark_message_read():
    if 'user_id' in session and 'is_admin' in session:
        if request.args.get('message_id'):
            message_id = request.args.get('message_id')
            message = Message.query.filter_by(id = message_id).first()
            message.read = True
            db.session.commit()
            flash('The message was marked as read.', Flash_Messages.info)
            return redirect(url_for('messages'))
        else:
            flash('Invalid Request.', Flash_Messages.error)
            return redirect(url_for('messages'))
    else: 
        return render_template('404.html', title='404 - Not Found')
    
@app.route('/mark-message-unread')
def mark_message_unread():
    if 'user_id' in session and 'is_admin' in session:
        if request.args.get('message_id'):
            message_id = request.args.get('message_id')
            message = Message.query.filter_by(id = message_id).first()
            message.read = False
            db.session.commit()
            flash('The message was marked as unread.', Flash_Messages.info)
            return redirect(url_for('messages'))
        else:
            flash('Invalid Request.', Flash_Messages.error)
            return redirect(url_for('messages'))
    else: 
        return render_template('404.html', title='404 - Not Found')
    
@app.route('/delete-post')
def delete_post():
    if 'user_id' in session and 'is_admin' in session:
        if request.args.get('post-id'):
            post_id = request.args.get('post-id')
            post = Post.query.filter_by(id = post_id).first()
            db.session.delete(post)
            db.session.commit()
            flash('The post was deleted.', Flash_Messages.info)
            return redirect(url_for('posts'))
        else:
            flash('Invalid Request.', Flash_Messages.error)
            return redirect(url_for('posts'))
    else: 
        return render_template('404.html', title='404 - Not Found')
    
@app.route('/delete-painting')
def delete_painting():
    if 'user_id' in session and 'is_admin' in session:
        if request.args.get('painting-id'):
            painting_id = request.args.get('painting-id')
            painting = Painting.query.filter_by(id = painting_id).first()

            # DELETE THE PAINTINGS IN THE PAINTING PHOTOS TABLE AND THEIR IMAGES TOO!!!

            db.session.delete(painting)
            db.session.commit()
            flash('The painting was successfully deleted.', Flash_Messages.info)
            return redirect(url_for('paintings'))
        else:
            flash('Invalid Request.', Flash_Messages.error)
            return redirect(url_for('paintings'))
    else: 
        return render_template('404.html', title='404 - Not Found')
    

@app.route('/delete-photo')
def delete_photo():
    if 'user_id' in session and 'is_admin' in session:
        if request.args.get('photo-id'):
            photo_id = request.args.get('photo-id')
            photo = Painting_Photo.query.filter_by(id=photo_id).first()
            print(photo)

            # DELETE THE PAINTINGS IN THE PAINTING PHOTOS TABLE AND THEIR IMAGES TOO!!!
            db.session.delete(photo)
            db.session.commit()
            flash('The photo was successfully deleted.', Flash_Messages.info)
            return redirect(url_for('painting_photos')+'?painting-id='+str(photo.painting_id))
        else:
            flash('Invalid Request.', Flash_Messages.error)
            return redirect(url_for('painting_photos')+'?painting-id='+str(photo.painting_id))
    else: 
        return render_template('404.html', title='404 - Not Found')