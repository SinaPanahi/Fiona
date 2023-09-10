import os
from flask import render_template, redirect, url_for, flash, request, session
from fiona import app, db
from fiona.models import Painting, Message, Post, Painting_Photo, Website
from fiona.utilities import Flash_Messages, format_price, generate_unique_filename, validate_filename, convert_text_to_html, convert_html_to_text

@app.route('/admin', methods=['GET','POST'])
@app.route('/admin/website', methods=['GET','POST'])
def website():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Website Settings'

    # Strip the texts coming from DB of their tags
    website.about_content = convert_html_to_text(website.about_content)
    website.privacy_policy_content = convert_html_to_text(website.privacy_policy_content)
    website.terms_of_use_content = convert_html_to_text(website.terms_of_use_content)

    if 'user_id' in session and 'is_admin' in session and request.method == 'GET':
        return render_template('admin/website.html', title=title, website=website)
    if 'user_id' in session and 'is_admin' in session and  request.method == 'POST':
        website_name = request.form.get('name').strip()
        about_page_content = convert_text_to_html(request.form.get('about-content'))
        privacy_policy_content = convert_text_to_html(request.form.get('privacy-policy-content'))
        terms_of_use_content = convert_text_to_html(request.form.get('terms-of-use-content'))
        website_address = request.form.get('address').strip()
        
        website = Website()
        website.name=website_name
        website.about_content=about_page_content 
        website.privacy_policy_content=privacy_policy_content 
        website.terms_of_use_content=terms_of_use_content
        website.address=website_address

        db.session.query(Website).delete()
        db.session.add(website)
        db.session.commit()

        return redirect(url_for('website'))
    else:
        return render_template('404.html',website=website, title='404 - Not Found')
    
@app.route('/admin/messages')
def messages():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Messages'

    if 'user_id' in session and 'is_admin' in session:
        messages = Message.query.all()
        return render_template('admin/messages.html', website=website, title=title, messages=messages)
    else:
        return render_template('404.html',website=website, title='404 - Not Found')
    
@app.route('/admin/posts')
def posts():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Posts'

    if 'user_id' in session and 'is_admin' in session:
        posts = Post.query.all()
        return render_template('admin/posts.html', website=website, title=title, posts=posts)
    else:
        return render_template('404.html',website=website, title='404 - Not Found')
    
@app.route('/admin/posts/add-post', methods=['GET','POST'])
def add_post():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Add Post'

    if 'user_id' in session and 'is_admin' in session and request.method == 'GET':
        return render_template('admin/add_post.html', title=title, website=website)
    if 'user_id' in session and 'is_admin' in session and  request.method == 'POST':
        title = request.form.get('title').strip()
        text = convert_text_to_html(request.form.get('text').strip())
        image = request.files['image']
        
        if image:
            if validate_filename(image.filename):
                # Save the file to the desired directory
                filename = generate_unique_filename() + os.path.splitext(image.filename)[1]
                image.save(os.path.join('fiona/static/images/posts/', filename))
                post = Post (title=title, text=text, url='static/images/posts/'+filename)
            else:
                flash('Invalid file type.', Flash_Messages.error)
                return redirect(url_for('add_post'))
        else:
            post = Post (title=title, text=text)

        db.session.add(post)
        db.session.commit()

        flash('Post was successfully added.', Flash_Messages.info)
        return redirect(url_for('posts'))
    else:
        return render_template('404.html',website=website, title='404 - Not Found')
    
@app.route('/admin/posts/update-post', methods=['GET','POST'])
def update_post():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Update Post'

    if 'user_id' in session and 'is_admin' in session and request.method == 'GET':
        if request.args.get('post-id'):
            post_id = request.args.get('post-id')
            post = Post.query.filter_by(id=post_id).first()
            post.text = convert_html_to_text(post.text)
            return render_template('admin/update_post.html', title=title, website=website, post=post)
        else:
            flash('Invalid request.', Flash_Messages.error)
            return redirect(url_for('posts'))
    if 'user_id' in session and 'is_admin' in session and  request.method == 'POST':
        post_id = request.args.get('post-id')
        title = request.form.get('title').strip()
        text = convert_text_to_html(request.form.get('text').strip())
        image = request.files['image']
        
        # Find the post which needs to be updated
        post = Post.query.filter_by(id=post_id).first()

        url = None
        if image:
            if validate_filename(image.filename):
                # Save the file to the desired directory
                filename = generate_unique_filename() + os.path.splitext(image.filename)[1]
                image.save(os.path.join('fiona/static/images/posts/', filename))
                url ='static/images/posts/'+filename
            else:
                flash('Invalid file type.', Flash_Messages.error)
                return redirect(url_for('add_post'))
        
        post.title = title
        post.text = text
        post.url = url
        db.session.commit()

        flash('Post was successfully updated.', Flash_Messages.info)
        return redirect(url_for('posts'))
    else:
        return render_template('404.html',website=website, title='404 - Not Found')
    
@app.route('/admin/paintings')
def paintings():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Paintings'

    if 'user_id' in session and 'is_admin' in session:
        paintings = Painting.query.all()
        return render_template('admin/paintings.html', website=website, title=title, paintings=paintings)
    else:
        return render_template('404.html',website=website, title='404 - Not Found')
    
@app.route('/admin/paintings/add-painting', methods=['GET','POST'])
def add_painting():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Add Painting'

    if 'user_id' in session and 'is_admin' in session and request.method == 'GET':
        return render_template('admin/add_painting.html', title=title, website=website)
    if 'user_id' in session and 'is_admin' in session and  request.method == 'POST':

        name= request.form.get('name').strip()
        description= convert_text_to_html(request.form.get('description'))
        width= request.form.get('width').strip()
        height= request.form.get('height').strip()
        price= format_price(request.form.get('price').strip())
        image= request.files['image']
        is_carousel_item= True if request.form.get('is-carousel-item') == 'on' else False
        
        if image:
            if validate_filename(image.filename):
                # Save the file to the desired directory
                filename = generate_unique_filename() + os.path.splitext(image.filename)[1]
                image.save(os.path.join('fiona/static/images/paintings/', filename))
                painting = Painting(
                    name=name, 
                    description=description, 
                    width=width,
                    height=height,
                    price=price,
                    url='static/images/paintings/'+filename,
                    is_carousel_item=is_carousel_item
                    )
            else:
                flash('Invalid file type.', Flash_Messages.error)
                return redirect(url_for('add_post'))

        db.session.add(painting)
        db.session.commit()

        flash('Painting was successfully added.', Flash_Messages.info)
        return redirect(url_for('paintings'))
    else:
        return render_template('404.html',website=website, title='404 - Not Found')

@app.route('/admin/painting/update-painting', methods=['GET','POST'])
def update_painting():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Update Painting'

    if 'user_id' in session and 'is_admin' in session and request.method == 'GET':
        if request.args.get('painting-id'):
            painting_id = request.args.get('painting-id')
            painting = Painting.query.filter_by(id=painting_id).first()
            painting.description = convert_html_to_text(painting.description)
            return render_template('admin/update_painting.html', title=title, website=website, painting=painting)
        else:
            flash('Invalid request.', Flash_Messages.error)
            return redirect(url_for('paintings'))
    if 'user_id' in session and 'is_admin' in session and request.method == 'POST':

        painting_id = request.args.get('painting-id')
        
        name= request.form.get('name').strip()
        description= convert_text_to_html(request.form.get('description'))
        width= request.form.get('width').strip()
        height= request.form.get('height').strip()
        price= format_price(request.form.get('price').strip())
        image= request.files['image']
        is_carousel_item= True if request.form.get('is-carousel-item') == 'on' else False
        
        # Find the painting which needs to be updated
        painting = Painting.query.filter_by(id=painting_id).first()

        url = None
        if image:
            if validate_filename(image.filename):
                # Save the file to the desired directory
                filename = generate_unique_filename() + os.path.splitext(image.filename)[1]
                image.save(os.path.join('fiona/static/images/paintings/', filename))
                url ='static/images/paintings/'+filename
            else:
                flash('Invalid file type.', Flash_Messages.error)
                return redirect(url_for('add_painting'))
        else:
            flash('Painting must have a photo.', Flash_Messages.error)
            return redirect(url_for('add_painting'))
        
        painting.name = name
        painting.description = description
        painting.width = width
        painting.height = height
        painting.price = price
        painting.url = url
        painting.is_carousel_item = is_carousel_item
        db.session.commit()

        flash('Painting was successfully updated.', Flash_Messages.info)
        return redirect(url_for('paintings'))
    else:
        return render_template('404.html',website=website, title='404 - Not Found')
    

@app.route('/admin/paintings/painting-photos', methods=['GET','POST'])
def painting_photos():
    # Get website info to be used in the template
    website = Website.query.first()
    title = website.name + ' | Add Painting Photos'
    painting_id = request.args.get('painting-id')
    painting = Painting.query.filter_by(id=painting_id).first()
    painting_photos = Painting_Photo.query.filter_by(painting_id=painting_id).all()

    if 'user_id' in session and 'is_admin' in session and request.method == 'GET':

        painting_id = request.args.get('painting-id')
        if not painting_id:
            flash('invalid request.', Flash_Messages.error)
            return redirect(url_for('paintings'))
        
        return render_template('admin/painting_photos.html', painting_photos=painting_photos, painting=painting, title=title, website=website)
    
    if 'user_id' in session and 'is_admin' in session and  request.method == 'POST':

        painting_id = request.args.get('painting-id')
        photos = request.files.getlist('photos')

        if not painting_id:
            flash('invalid request.', Flash_Messages.error)
            return redirect(url_for('paintings'))
        # For some reason there is always something at location 0!!! Ghosts?????
        if len(photos) < 2:
            flash('You must add at least one photo.', Flash_Messages.Warning)
            return redirect(url_for('painting_photos')+'?painting-id='+str(painting_id))
        for photo in photos:
            if validate_filename(photo.filename):
                # Save the file to the desired directory
                filename = generate_unique_filename() + os.path.splitext(photo.filename)[1]
                photo.save(os.path.join('fiona/static/images/painting_photos/', filename))
                url ='static/images/painting_photos/'+filename
                painting_photo = Painting_Photo(painting_id=painting_id, url=url)
                db.session.add(painting_photo)
            else:
                flash('Invalid file type.', Flash_Messages.error)
        
        db.session.commit()
        flash('Photo(s) were added successfully.', Flash_Messages.info)
        return redirect(url_for('painting_photos')+'?painting-id='+str(painting_id))
    else:
        return render_template('404.html',website=website, title='404 - Not Found')

  