import './App.css';
import axios from 'axios';
import Header from './Header.jsx';
import Footer from './Footer.jsx';
import Container from './Container.jsx';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Cart from './pages/Cart';
import PlaceOrder from './pages/PlaceOrder';
import PaymentMethod from './pages/PaymentMethod.jsx'; 
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState , useEffect } from 'react';

function App() {
  const [category, setCategory] = useState('Home');
  const [cartItems, setCartItems] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(()=>{
  axios.get()
  .then (() =>{

  }
)
.catch ((error)=>{
 console.log(error)
})
  })
  
  return (
    <Router> 
      <Header
        category={category}
        setCategory={setCategory}
        cartItems={cartItems}
        favorites={favorites}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/"
          element={
            <Container
              category={category}
              searchQuery={searchQuery}
              cartItems={cartItems}
              setCartItems={setCartItems}
              favorites={favorites}
              setFavorites={setFavorites}
            />
          }
        />
        <Route
    path="/cart"
    element={<Cart cartItems={cartItems} />}
  />
  <Route
    path="/place-order"
    element={<PlaceOrder setCartItems={setCartItems} />}
  />
<Route path="/payment" element={<PaymentMethod />} />

      </Routes>

      <Footer />
    </Router>
  );
}

export default App;
