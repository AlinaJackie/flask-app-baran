from pathlib import Path
from typing import List, Dict
import json
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, request, session, current_app
from . import posts_bp
from .forms import PostForm
from datetime import datetime
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

POSTS_FILE = r'C:\Users\alina\flask_students\posts\posts.json'

def read_posts_from_json() -> List[Dict]:
    if Path(POSTS_FILE).exists():
        with Path(POSTS_FILE).open('r', encoding='utf-8') as file:
            posts = json.load(file)

            for post in posts:
                post['is_active'] = bool(post.get('is_active', False))
                post['publication_date'] = post.get('publication_date', post.get('posted', '1970-01-01'))
            return posts
    return []


def write_posts_to_json(posts: List[Dict]) -> None:
    with Path(POSTS_FILE).open('w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4)

@posts_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_active = form.is_active.data
        category = form.category.data
        publish_date = form.publish_date.data
        author = session.get('username', 'Anonymous')

        # Обробка зображення
        image_filename = 'default.jpg'  # Значення за замовчуванням, якщо зображення не додано
        if form.image.data:
            image = form.image.data
            if image and allowed_file(image.filename):

                image_filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.root_path, UPLOAD_FOLDER, image_filename))

        posts = read_posts_from_json()

        post_id = len(posts) + 1
        post_new = {
            'id': post_id,
            'title': title,
            'content': content,
            'is_active': is_active,
            'category': category,
            'author': author,
            'posted': publish_date.strftime('%Y-%m-%d'),
            'image': image_filename
        }

        posts.append(post_new)

        write_posts_to_json(posts)

        flash(f'Post "{title}" added successfully!', 'success')
        return redirect(url_for('.get_posts'))

    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")

    return render_template('posts/add_post.html', form=form, edit=False)

@posts_bp.route('/')
def get_posts():
    posts = read_posts_from_json()
    return render_template('posts/posts.html', posts=posts)

@posts_bp.route('/<int:id>')
def detail_post(id):
    posts = read_posts_from_json()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        return render_template('posts/404.html'), 404
    return render_template('posts/detail_post.html', post=post)

@posts_bp.route('/delete_post/<int:id>')
def delete_post(id):
    posts = read_posts_from_json()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        flash(f'Post not found!', 'danger')
        return redirect(url_for('.get_posts'))


    posts = [post for post in posts if post['id'] != id]


    write_posts_to_json(posts)

    flash(f'Post deleted successfully!', 'success')
    return redirect(url_for('.get_posts'))


@posts_bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    posts = read_posts_from_json()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        flash(f'Post not found!', 'danger')
        return redirect(url_for('.get_posts'))

    form = PostForm(obj=post)

    publish_date_str = post.get('publication_date') or post.get('posted')

    if publish_date_str:
        try:
            form.publish_date.data = datetime.strptime(publish_date_str, '%Y-%m-%d')
        except ValueError:
            flash(f"Date format is incorrect for post ID {id}.", "danger")
            return redirect(url_for('.get_posts'))

    if form.validate_on_submit():
        post['title'] = form.title.data
        post['content'] = form.content.data
        post['is_active'] = form.is_active.data
        post['category'] = form.category.data
        post['posted'] = form.publish_date.data.strftime('%Y-%m-%d')


        if form.image.data:
            image = form.image.data
            if image and allowed_file(image.filename):
                if post['image'] and post['image'] != 'default.jpg':
                    old_image_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, post['image'])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)


                image_filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.root_path, UPLOAD_FOLDER, image_filename))
                post['image'] = image_filename
        else:
            if not post['image']:
                post['image'] = 'default.jpg'


        write_posts_to_json(posts)

        flash(f'Post updated successfully!', 'success')
        return redirect(url_for('.get_posts'))
    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")

    return render_template('posts/add_post.html', form=form, edit=True)
