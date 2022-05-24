from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URL_map


def get_unique_short_id():
    ...


@app.route('/', methods=['GET', 'POST'])
def index():
    ...
