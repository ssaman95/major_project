from flask import render_template, flash, redirect, url_for, request
from flask import current_app
from app import db
from app.main.forms import EditProfileForm, TweetForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.main.rumour_app import run_rumour_app
from app.main import bp



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TweetForm()
    if form.validate_on_submit():
        tweet_url = form.tweet_url.data
        result = run_rumour_app(tweet_url)
        flash('Result: ' + result)
    return render_template('index.html', title='Home',form=form)





@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.twitter_id= form.twitter_id.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.twitter_id.data = current_user.twitter_id
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)



@bp.route('/results', methods=['GET', 'POST'])
@login_required
def results(tweet_url):
    return render_template('results.html', result=result)

