from . import post_bp
from flask import render_template, abort, flash, url_for, redirect, request
from .forms import PostForm
from .utils import load_posts, save_post, get_post


@post_bp.route('/add_post', methods=["GET", "POST"]) 
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        publish_date = form.publish_date.data
        is_active = form.is_active.data
        
        
        # Логіка створення нового посту
        new_post = {
            "id": len(load_posts()) + 1,  # Генерація ID на основі кількості постів
            "title": title,
            "content": content,
            "category": category,
            "publish_date": publish_date.strftime("%Y-%m-%d"),  # Форматування дати
            "is_active": is_active
        }
        save_post(new_post)
        flash(f"Post '{title}' added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash("Enter the correct data in the form!", "danger")
    
    return render_template("add_post.html", form=form)



@post_bp.route('/') 
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = get_post(id)
    if not post:
        return abort(404)
    return render_template("detail_post.html", post=post)
    
    # Error handler for 404
@post_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404