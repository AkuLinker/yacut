from http import HTTPStatus

from flask import flash, redirect, render_template

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URL_map
from yacut.utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if URL_map.query.filter_by(short=short_id).first():
            flash(f'Имя {short_id} уже занято!')
            return render_template('index.html', form=form)
        if short_id is None or short_id == '':
            short_id = get_unique_short_id()
        url = URL_map(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(url)
        db.session.commit()
        return render_template(
            'index.html', form=form, short=short_id
        ), HTTPStatus.OK
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    redirect_url = URL_map.query.filter_by(short=short_id).first_or_404()
    return redirect(redirect_url.original)
