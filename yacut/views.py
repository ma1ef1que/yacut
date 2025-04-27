from flask import flash, render_template, url_for, redirect

from . import app
from .forms import URLForm
from .services import ShortLinkService


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        try:
            url_map = ShortLinkService.create_short_link(
                original_url=form.original_link.data,
                custom_id=form.custom_id.data
            )
        except ShortLinkService.InvalidShortIdError as e:
            flash(str(e))
            return render_template('index.html', form=form)
        except ShortLinkService.ShortIdExistsError as e:
            flash(str(e))
            return render_template('index.html', form=form)

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
    try:
        original_url = ShortLinkService.get_original_url(short_id)
    except ShortLinkService.ShortLinkError:
        return render_template('404.html'), 404
    return redirect(original_url)
