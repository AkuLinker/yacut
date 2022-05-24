import random
import string
from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URL_map


def get_unique_short_id():
    characters = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(characters) for _ in range(6))
    if URL_map.query.filter_by(short=short_id).first():
        short_id = get_unique_short_id()
    return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_url = form.custom_id.data
        if URL_map.query.filter_by(short=custom_url).first():
            flash('Такой вариант ссылки уже занят!')
            return render_template('index.html', form=form)
        if custom_url == '':
            custom_url = get_unique_short_id()
        url = URL_map(
            original=form.original_link.data,
            short=custom_url,
        )
        db.session.add(url)
        db.session.commit()
        return render_template(
            'index.html', form=form, short=custom_url
        ), HTTPStatus.OK
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    redirect_url = URL_map.query.filter_by(short=short).first()
    if redirect_url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(redirect_url.original)
