import PropTypes from 'prop-types';
import { useState } from 'react';

function PlaceOrder({ setCartItems }) {
  const [address, setAddress] = useState('');
  const [orderPlaced, setOrderPlaced] = useState(false);

  const handleOrder = () => {
    if (!address.trim()) {
      alert('Please enter your address.');
      return;
    }
    setCartItems([]); 
    setOrderPlaced(true);
  };

  if (orderPlaced) {
    return (
      <div className="p-4 text-center">
        <h2 className="text-2xl font-bold text-green-600 mb-2">
          Order Placed!
        </h2>
        <p>Your order has been placed successfully. Thank you!</p>
      </div>
    );
  }

  return (
    <div className="place-order-container">
      <div className="place-order-box">
        <h2>Place Your Order</h2>
        <textarea
          className="place-order-textarea"
          rows={4}
          placeholder="Enter delivery address"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        ></textarea>
        <button className="place-order-button" onClick={handleOrder}>
          Confirm Order
        </button>
      </div>
    </div>
  );
}
PlaceOrder.propTypes = {
  setCartItems: PropTypes.func.isRequired,
};

export default PlaceOrder;
