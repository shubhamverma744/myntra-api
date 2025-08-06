import offers from './image/offers.jpeg';

import image1 from './image/image1.jpg';
import image2 from './image/image2.jpg';
import image3 from './image/image3.jpg';

import woman1 from './image/woman1.jpg';
import woman2 from './image/woman2.jpg';
import woman3 from './image/woman3.jpg';

import kids1 from './image/kids1.jpg';
import kids2 from './image/kids2.jpg';
import kids3 from './image/kids3.jpg';

import book1 from './image/book1.jpeg';
import book2 from './image/book2.jpeg';
import book3 from './image/book3.jpeg';

import beauty1 from './image/beauty1.jpeg';
import beauty2 from './image/beauty2.jpeg';
import beauty3 from './image/beauty3.jpeg';

import PropTypes from 'prop-types';

const allProducts = [
  { name: 'Men 1', category: 'Men', src: image1, price: 599 },
  { name: 'Men 2', category: 'Men', src: image2, price: 799 },
  { name: 'Men 3', category: 'Men', src: image3, price: 899 },

  { name: 'Women 1', category: 'Women', src: woman1, price: 1499 },
  { name: 'Women 2', category: 'Women', src: woman2, price: 1299 },
  { name: 'Women 3', category: 'Women', src: woman3, price: 1399 },

  { name: 'Kidswear 1', category: 'Kids', src: kids1, price: 499 },
  { name: 'Kidswear 2', category: 'Kids', src: kids2, price: 599 },
  { name: 'Kidswear 3', category: 'Kids', src: kids3, price: 699 },

  { name: 'Beauty 1', category: 'Beauty', src: beauty1, price: 299 },
  { name: 'Beauty 2', category: 'Beauty', src: beauty2, price: 399 },
  { name: 'Beauty 3', category: 'Beauty', src: beauty3, price: 349 },

  { name: 'Book 1', category: 'Books', src: book1, price: 199 },
  { name: 'Book 2', category: 'Books', src: book2, price: 249 },
  { name: 'Book 3', category: 'Books', src: book3, price: 349 },
];

// import { listProducts } from './api.js';
// const allProducts = listProducts();

function Container({
  category,
  searchQuery,
  cartItems,
  setCartItems,
  favorites,
  setFavorites,
}) {
  const addToCart = (product) => {
    if (!cartItems.find((item) => item.name === product.name)) {
      setCartItems([...cartItems, product]);
    }
  };

  const removeFromCart = (product) => {
    setCartItems(cartItems.filter((item) => item.name !== product.name));
  };

  const addToFavorites = (product) => {
    if (!favorites.find((item) => item.name === product.name)) {
      setFavorites([...favorites, product]);
    }
  };

  const filteredProducts = allProducts.filter((product) =>
    product.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (category === 'PROFILE') {
    return (
      <div className="profile-details">
        <h3>Profile Details</h3>
        <p>Name: MYNTRA</p>
        <p>Email: myntra@gmail.com</p>
        <p>Location: Indore, M.P</p>
      </div>
    );
  }

  if (category === 'FAVORITE') {
    return (
      <div className="favorite-section">
        <h3>Favorite Items</h3>
        {favorites.length === 0 ? (
          <p>You have no favorites yet.</p>
        ) : (
          <div className="image-grid">
            {favorites.map((item) => (
              <div key={item.name} className="product-card">
                <img src={item.src} alt={item.name} className="image-style" />
                <p>{item.name}</p>
                <p>₹{item.price}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  if (category === 'CART') {
    return (
      <div className="cart-section">
        <h3>Your Cart</h3>
        {cartItems.length === 0 ? (
          <p>Your cart is currently empty.</p>
        ) : (
          <div className="image-grid">
            {cartItems.map((item) => (
              <div key={item.name} className="product-card">
                <img src={item.src} alt={item.name} className="image-style" />
                <p>{item.name}</p>
                <p>₹{item.price}</p>
                <button onClick={() => removeFromCart(item)}>❌ Remove</button>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  if (category === 'Home') {
    return (
      <div className="home-banner">
        <img src={offers} alt="offers" className="image-view" />
      </div>
    );
  }

  if (['Men', 'Women', 'Kids', 'Beauty', 'Books'].includes(category)) {
    const categoryProducts = allProducts.filter((p) => p.category === category);
    return (
      <div className="image-section">
        <h2>{category.toUpperCase()} Products</h2>
        <div className="image-grid">
          {categoryProducts.map((product) => {
            const isInCart = cartItems.some(
              (item) => item.name === product.name
            );
            return (
              <div key={product.name} className="product-card">
                <img
                  src={product.src}
                  alt={product.name}
                  className="image-style"
                />
                <p>{product.name}</p>
                <p>₹{product.price}</p>
                {isInCart ? (
                  <button onClick={() => removeFromCart(product)}>❌</button>
                ) : (
                  <button onClick={() => addToCart(product)}>🛒 Cart</button>
                )}
                <button onClick={() => addToFavorites(product)}>
                  Wishlist
                </button>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  if (searchQuery) {
    return (
      <div className="search-results">
        <h2>&quot;{searchQuery}&quot;</h2>
        {filteredProducts.length ? (
          <div className="image-grid">
            {filteredProducts.map((product) => (
              <div key={product.name} className="product-card">
                <img
                  src={product.src}
                  alt={product.name}
                  className="image-style"
                />
                <p>{product.name}</p>
                <p>₹{product.price}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>No products found.</p>
        )}
      </div>
    );
  }

  return null;
}

Container.propTypes = {
  category: PropTypes.string.isRequired,
  searchQuery: PropTypes.string.isRequired,
  cartItems: PropTypes.arrayOf(PropTypes.object).isRequired,
  setCartItems: PropTypes.func.isRequired,
  favorites: PropTypes.arrayOf(PropTypes.object).isRequired,
  setFavorites: PropTypes.func.isRequired,
};

export default Container;
