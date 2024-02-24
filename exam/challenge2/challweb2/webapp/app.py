import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Import db from extensions module
from extensions import db

def create_app():
    print("Creating app...")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize extensions with the app instance
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    # Import models and routes here to avoid circular imports
    from models import User, Post, Subscription, Report
    # Define the user loader function

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Dummy database initialization for demonstration purposes
    with app.app_context():
        db.create_all()  # Create database tables
        # Initialize database with dummy data logic here
        if User.query.count() == 0:  # Check if users already exist to avoid duplicating initialization
            # Create dummy users
            user1 = User(username='User1', password_hash=generate_password_hash('password1'))
            user2 = User(username='User2', password_hash=generate_password_hash('password2'))
            admin = User(username='admin', password_hash=generate_password_hash(os.environ['ADMIN_PASSWORD']))
            # Add users to session
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(admin)

			# Commit to save users
            db.session.commit()
			# Create subscriptions
            sub1 = Subscription(subscriber_id=user1.id, subscribed_to_id=user2.id)
            sub2 = Subscription(subscriber_id=user2.id, subscribed_to_id=user1.id)
            db.session.add(sub1)
            db.session.add(sub2)
            db.session.commit()

			# Create posts
            post1 = Post(title='Public Post by User1', content='This is a public post by User1.', public=True, user_id=user1.id)
            post2 = Post(title='Private Post by User1', content='This is a private post by User1.', public=False, user_id=user1.id)
            post3 = Post(title='Public Post by User2', content='This is a public post by User2.', public=True, user_id=user2.id)
            post4 = Post(title='Private Post by User2', content='This is a private post by User2.', public=False, user_id=user2.id)
            welcome_post = Post(title='Welcome to the Blogging Platform', content='Welcome all users! I have secret posts only visible to my subscribers.', public=True, user_id=admin.id)
            secret_post = Post(title='Secret Post', content=os.environ['FLAG'], public=False, user_id=admin.id)  # FLAG is set in the environment
			# Add posts to session
            db.session.add_all([post1, post2, post3, post4, welcome_post, secret_post])
            # Commit to save posts
            db.session.commit()
    # Database models and Flask routes will go here
    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists.')
                return redirect(url_for('register'))

            new_user = User(username=username, password_hash=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password_hash, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page

            login_user(user, remember=True)
            return redirect(url_for('profile', username=username))

        return render_template('login.html')

    @app.route('/create-post', methods=['GET', 'POST'])
    @login_required
    def create_post():
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            public = request.form.get('public') == 'on'

            new_post = Post(title=title, content=content, public=public, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('profile', username=current_user.username))
        return render_template('create_post.html')

    @app.route('/delete-post/<post_id>')
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username))


    @app.route('/toggle-post-privacy/<post_id>')
    @login_required
    def toggle_post_privacy(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author == current_user:
            post.public = not post.public
            db.session.commit()
        return redirect(url_for('profile', username=current_user.username))

    @app.route('/subscribe/<username>', methods=['GET', 'POST'])
    @login_required
    def subscribe(username):
        user_to_subscribe = User.query.filter_by(username=username).first_or_404()
        
        if user_to_subscribe == current_user:
            flash('You cannot subscribe to yourself.')
            return redirect(url_for('profile', username=username))

        subscription = Subscription(subscriber_id=current_user.id, subscribed_to_id=user_to_subscribe.id)
        db.session.add(subscription)
        db.session.commit()
        return redirect(url_for('profile', username=username))

    @app.route('/unsubscribe/<username>', methods=['GET', 'POST'])
    @login_required
    def unsubscribe(username):
        user_to_unsubscribe = User.query.filter_by(username=username).first_or_404()
        subscription = Subscription.query.filter_by(subscriber_id=current_user.id, subscribed_to_id=user_to_unsubscribe.id).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
        return redirect(url_for('profile', username=username))

    @app.route('/profile/<username>')
    @login_required
    def profile(username):
        user = User.query.filter_by(username=username).first_or_404()

        # Check if the current user is subscribed to the profile user
        current_user_subscribed_to_user = Subscription.query.filter_by(subscriber_id=current_user.id, subscribed_to_id=user.id).first() is not None

        # Check if the profile user is subscribed to the current user
        user_subscribed_to_current_user = Subscription.query.filter_by(subscriber_id=user.id, subscribed_to_id=current_user.id).first() is not None

        # Determine if there's mutual subscription
        is_mutual_subscription = current_user_subscribed_to_user and user_subscribed_to_current_user

        if user == current_user or is_mutual_subscription:
            posts = user.posts
        else:
            posts = Post.query.filter_by(user_id=user.id, public=True).all()

        return render_template('profile.html', user=user, posts=posts, is_subscribed=current_user_subscribed_to_user, is_mutual_subscription=is_mutual_subscription)



    @app.route('/report', methods=['GET', 'POST'])
    @login_required
    def report():
        if request.method == 'POST':
            url = request.form.get('url')
            new_report = Report(url=url, reporter_id=current_user.id)
            db.session.add(new_report)
            db.session.commit()

            flash('URL reported successfully.')
            return redirect(url_for('index'))  # Assuming there's an index route/dashboard
        return render_template('report.html')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
