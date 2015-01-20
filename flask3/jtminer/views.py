from flask import render_template, redirect, g, request, url_for, abort
from jtminer import app, babel

@babel.localeselector
def get_locale():
    """Direct babel to use the language defined in the session."""
    return g.get('current_lang', 'en')

@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('zh_CN', 'en'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@app.route('/')
def root():
    return redirect(url_for('index', lang_code='en'))

@app.route('/<lang_code>')
def index():
    return render_template('index.html')

@app.route('/<lang_code>/about')
def about():
    return render_template('about.html')

@app.route('/<lang_code>/systemsetup')
def systemsetup():
    return render_template('systemsetup.html')

@app.route('/<lang_code>/miningsetup')
def miningsetup():
    return render_template('miningsetup.html')

@app.route('/<lang_code>/advanced')
def advanced():
    return render_template('advanced.html')

