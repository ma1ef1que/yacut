from flask import flash, render_template, url_for, redirect

from . import app, db
from .constants import SHORT_ID_LENGTH
from .forms import URLForm
from .models import URLMap
from .utils import check_unique_short_id, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()

        if len(short) > SHORT_ID_LENGTH:
            flash(
                (
                    f'Короткая ссылка не должна превышать '
                    f'{SHORT_ID_LENGTH} символов'
                )
            )
            return render_template('index.html', form=form)
        if not check_unique_short_id(short):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        url_map = URLMap(original=form.original_link.data, short=short)
        db.session.add(url_map)
        db.session.commit()

        flash('Получившаяся короткая ссылка:')
        return render_template(
            'index.html',
            form=form,
            short_link=url_for(
                'mapping_redirect',
                short_id=url_map.short,
                _external=True,
            ),
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', strict_slashes=False)
def mapping_redirect(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
