from app.lib.db.models import db
from main import app

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()  # TODO: This needs to be removed once live, this is just for re-creating the database
        db.create_all()
        print("Database tables created")
