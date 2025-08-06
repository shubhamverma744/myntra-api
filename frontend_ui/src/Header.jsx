import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';
import {
  MdPerson,
  MdFavoriteBorder,
  MdShoppingCart,
  MdSearch,
  MdClose,
} from 'react-icons/md';

function Header({
  setCategory,
  cartItems,
  favorites,
  searchQuery,
  setSearchQuery,
}) {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    setIsLoggedIn(localStorage.getItem('isLoggedIn') === 'true');
  }, []);

  const handleCategoryClick = (selectedCategory) =>
    setCategory(selectedCategory);

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn');
    setIsLoggedIn(false);
    navigate('/login');
  };

  const onSubmit = (e) => {
    e.preventDefault();
    const q = searchQuery.trim();
    if (!q) return;
    // If you don’t have a /search route, delete the next line
    navigate(`/search?q=${encodeURIComponent(q)}`);
  };

  const clear = () => {
    setSearchQuery('');
    inputRef.current?.focus();
  };

  return (
    <header className="myntra-header">
      <div className="logo" onClick={() => handleCategoryClick('Home')}>
        MYNTRA
      </div>

      <nav className="nav-links">
        {['Home', 'Men', 'Women', 'Kids', 'Beauty', 'Books'].map((cat) => (
          <button
            key={cat}
            className="nav-btn"
            onClick={() => handleCategoryClick(cat)}
            onMouseEnter={
              ['Men', 'Women', 'Kids', 'Beauty', 'Books'].includes(cat)
                ? () => handleCategoryClick(cat)
                : undefined
            }
          >
            {cat}
          </button>
        ))}
      </nav>

      <form className="search-box" onSubmit={onSubmit}>
        <MdSearch size={20} className="search-icon" />
        <input
          ref={inputRef}
          type="text"
          placeholder='Search for products, brands and more… (e.g. "shirt", "book")'
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        {searchQuery && (
          <button type="button" className="search-clear" onClick={clear}>
            <MdClose size={18} />
          </button>
        )}
      </form>

      <div className="user-section">
        <div
          className="user-icon"
          onClick={() => handleCategoryClick('PROFILE')}
        >
          <MdPerson size={24} />
        </div>
        <div
          className="user-icon"
          onClick={() => handleCategoryClick('FAVORITE')}
        >
          <MdFavoriteBorder size={24} />
          <p>({favorites.length})</p>
        </div>
        <div className="user-icon" onClick={() => navigate('/cart')}>
          <MdShoppingCart size={24} />
          <p>({cartItems.length})</p>
        </div>

        {!isLoggedIn ? (
          <div className="auth-buttons">
            <button className="nav-btn" onClick={() => navigate('/login')}>
              Login
            </button>
            <button className="nav-btn" onClick={() => navigate('/signup')}>
              Sign Up
            </button>
          </div>
        ) : (
          <button className="nav-btn" onClick={handleLogout}>
            Logout
          </button>
        )}
      </div>
    </header>
  );
}

Header.propTypes = {
  setCategory: PropTypes.func.isRequired,
  cartItems: PropTypes.arrayOf(PropTypes.object).isRequired,
  favorites: PropTypes.arrayOf(PropTypes.object).isRequired,
  searchQuery: PropTypes.string.isRequired,
  setSearchQuery: PropTypes.func.isRequired,
};

export default Header;
