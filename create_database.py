from app.lib.models import db
from main import app

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created")
