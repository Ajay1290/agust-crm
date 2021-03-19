from manager import create_app, db, dbt
from manager.models.func import set_db_for_binders

app = create_app()
app.app_context().push()

def reset_all_db():
	# db.drop_all()
	db.create_all()

reset_all_db()