from sqlalchemy.orm import Session
from db.config import Base, engine
from utils.db_helpers import get_session, commit_with_rollback
from models.models_all import Category, SubCategory, SubSubCategory

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = get_session()

    categories_data = {
        "Men": {
            "Topwear": ["T-Shirts", "Casual Shirts", "Formal Shirts", "Jackets"],
            "Bottomwear": ["Jeans", "Trousers", "Shorts", "Joggers"],
            "Footwear": ["Casual Shoes", "Formal Shoes", "Sports Shoes", "Sandals"],
        },
        "Women": {
            "Indian & Fusion Wear": ["Kurtas & Suits", "Sarees", "Lehengas"],
            "Western Wear": ["Dresses", "Tops", "Jeans", "Skirts"],
            "Footwear": ["Heels", "Flats", "Boots", "Sports Shoes"],
        },
        "Kids": {
            "Boys Clothing": ["T-Shirts", "Shirts", "Jeans", "Shorts"],
            "Girls Clothing": ["Dresses", "Tops", "Leggings", "Skirts"],
            "Footwear": ["Casual Shoes", "Sandals", "Sports Shoes"],
        },
        "Beauty": {
            "Makeup": ["Lipstick", "Eyeliner", "Mascara", "Foundation"],
            "Skincare": ["Face Wash", "Moisturizer", "Sunscreen"],
            "Haircare": ["Shampoo", "Conditioner", "Hair Oil"],
            "Fragrances": ["Perfumes", "Deodorants", "Body Mists"],
        },
    }

    try:
        for cat_name, subcats in categories_data.items():
            # Check if category exists
            category = db.query(Category).filter_by(name=cat_name).first()
            if not category:
                category = Category(name=cat_name)
                db.add(category)
                db.flush()  # get category.id

            for subcat_name, subsubcats in subcats.items():
                subcat = db.query(SubCategory).filter_by(name=subcat_name, category_id=category.id).first()
                if not subcat:
                    subcat = SubCategory(name=subcat_name, category_id=category.id)
                    db.add(subcat)
                    db.flush()

                for subsubcat_name in subsubcats:
                    subsubcat = db.query(SubSubCategory).filter_by(
                        name=subsubcat_name, subcategory_id=subcat.id
                    ).first()
                    if not subsubcat:
                        subsubcat = SubSubCategory(name=subsubcat_name, subcategory_id=subcat.id)
                        db.add(subsubcat)

        commit_with_rollback(db)
        print("✅ Categories seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
