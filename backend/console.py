from app import create_app
from db.config import SessionLocal
from models.buyer import Buyer
from models.product import Product
from models.orders import Order
from models.review import Review
# from models.comment import Comment
# from models.review import Review
import code  # ✅ This is key


# Create the Flask app using the factory
app = create_app()

# Push the app context to allow DB/session use
app.app_context().push()

# Create DB session
session = SessionLocal()

print("✅ Flask console ready.")
print("👉 Available: session, Buyer, Product, Order, Review, Comment")


code.interact(local=globals())
