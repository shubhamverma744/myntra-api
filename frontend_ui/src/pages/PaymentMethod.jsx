import './PaymentMethod.css';
import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function PaymentMethod() {
  const { state } = useLocation();
  const totalAmount = state?.total ?? 0;
  const [method, setMethod] = useState('CARD');
  const [isPaying, setIsPaying] = useState(false);
  const navigate = useNavigate();

  const loadRazorpay = () =>
    new Promise((resolve, reject) => {
      if (window.Razorpay) return resolve(true);
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => reject(new Error('Razorpay SDK failed to load'));
      document.body.appendChild(script);
    });

  const handlePayment = async () => {
    if (totalAmount <= 0) {
      alert('Invalid amount. Please go back to cart.');
      navigate(-1);
      return;
    }

    if (method === 'COD') {
      alert('Order placed with Cash on Delivery!');
      return;
    }

    try {
      setIsPaying(true);
      await loadRazorpay();

      // Ideally, create an order on your backend and pass order_id here.
      const options = {
        key: process.env.REACT_APP_RAZORPAY_KEY_ID || 'YOUR_RAZORPAY_KEY_ID',
        amount: Math.round(totalAmount * 100), // paise
        currency: 'INR',
        name: 'Myntra Clone',
        description: 'Test Payment',
        handler: function (response) {
          console.log('Razorpay success:', response);
          alert('Payment Successful!');
          // navigate('/order-success', { state: { total: totalAmount, method, paymentId: response.razorpay_payment_id } });
        },
        prefill: {
          name: 'Chirag Ramteke',
          email: 'chirag@example.com',
          contact: '9999999999',
        },
        theme: {
          color: '#ff3f6c',
        },
      };

      const rzp = new window.Razorpay(options);
      rzp.on('payment.failed', function (resp) {
        console.error('Payment failed:', resp.error);
        alert('Payment failed. Please try again.');
      });
      rzp.open();
    } catch (e) {
      console.error(e);
      alert('Unable to start Razorpay. Please try again later.');
    } finally {
      setIsPaying(false);
    }
  };

  return (
    <div className="payment-container">
      <h2 className="payment-title">Choose Payment Method</h2>

      <div className="payment-options">
        <label>
          <input
            type="radio"
            value="CARD"
            checked={method === 'CARD'}
            onChange={(e) => setMethod(e.target.value)}
          />
          Credit/Debit Card
        </label>
        <label>
          <input
            type="radio"
            value="UPI"
            checked={method === 'UPI'}
            onChange={(e) => setMethod(e.target.value)}
          />
          UPI / QR
        </label>
        <label>
          <input
            type="radio"
            value="NET_BANKING"
            checked={method === 'NET_BANKING'}
            onChange={(e) => setMethod(e.target.value)}
          />
          Net Banking
        </label>
        <label>
          <input
            type="radio"
            value="COD"
            checked={method === 'COD'}
            onChange={(e) => setMethod(e.target.value)}
          />
          Cash on Delivery
        </label>
      </div>

      <button
        onClick={handlePayment}
        disabled={isPaying || totalAmount <= 0}
        className="payment-btn"
        style={{
          opacity: isPaying || totalAmount <= 0 ? 0.7 : 1,
          cursor: isPaying || totalAmount <= 0 ? 'not-allowed' : 'pointer',
        }}
      >
        {isPaying ? 'Processing...' : `Pay ₹${totalAmount}`}
      </button>

      <button onClick={() => navigate(-1)} className="back-btn">
        Back
      </button>
    </div>
  );
}

export default PaymentMethod;
