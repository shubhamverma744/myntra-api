import './Cart.css';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';

function Cart({ cartItems }) {
  const navigate = useNavigate();
  const total = cartItems.reduce(
    (sum, item) => sum + (item.price || 0) * (item.qty || 1),
    0
  );
  const handlePlaceOrder = () => {
    navigate('/payment', { state: { total } });
  };
  return (
    <div className="cart-container">
      <h2 className="cart-header">Your Cart</h2>

      {cartItems.length === 0 ? (
        <p className="cart-empty">No items in cart.</p>
      ) : (
        <>
          <ul className="cart-list">
            {cartItems.map((item) => (
              <li key={item.id} className="cart-item">
                <img src={item.image} alt={item.name} />
                <div className="cart-item-info">
                  <p className="cart-item-name">{item.name}</p>
                  <p className="cart-item-qty">Qty: {item.qty}</p>
                </div>
                <div className="cart-item-price">
                  ₹{(item.price || 0) * (item.qty || 1)}
                </div>
              </li>
            ))}
          </ul>

          <div className="cart-summary">
            <span>Total: ₹{total}</span>
            <button className="cart-btn" onClick={handlePlaceOrder}>
              Place Order
            </button>
          </div>
        </>
      )}
    </div>
  );
}

Cart.propTypes = {
  cartItems: PropTypes.array.isRequired,
};

export default Cart;
