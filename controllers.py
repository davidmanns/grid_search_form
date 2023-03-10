"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

	http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

	http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

	http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL, Field, DAL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from pydal.validators import *
from py4web.utils.grid import Grid, GridClassStyleBulma, Column
from py4web.utils.form import Form, FormStyleBulma
from yatl.helpers import *

#Note, I put made this in the index controller. If it is called without
#the 'index' argument, the grid will display, and page turn buttons
#work, but Add, Details, Edit and Delete buttons all get '404' because
#of an extra '/' at the beginning of the URL!
@action("index", method=['POST', 'GET'])
@action('index/<path:path>', method=['POST', 'GET'])
@action.uses("index.html", db)
def index(path=None):
	
	query = db.people.id>0
	message = DIV(
				P("By experiment, this is the simplest way to make search form work"),
	)

	search_form=Form([
		Field('name_contains', 'string')],
		keep_values=True	#so filter values remain displayed and as defaults until changed
	)
	
	#preserve pagination and filter context from call parameters
	if len(search_form.vars) == 0:
		search_form.vars = request.query

	if search_form.vars.get('name_contains'):
		query = db.people.name.like('%'+search_form.vars.get('name_contains')+'%')

	grid = Grid(path, query,
			orderby=db.people.name,
			columns=[db.people.name],
			grid_class_style=GridClassStyleBulma,
			formstyle=FormStyleBulma,
			search_form=search_form,
			rows_per_page=5
			)
	return locals()
