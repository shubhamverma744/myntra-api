import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    const users = JSON.parse(localStorage.getItem('users')) || [];
    const matchedUser = users.find(
      (user) => user.email === email && user.password === password
    );

    if (matchedUser) {
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('currentUser', JSON.stringify(matchedUser));
      alert(`${matchedUser.name || matchedUser.email}!`);
      navigate('/');
    } else {
      alert('Login Succesfully');
    }
  };

  return (
    <form onSubmit={handleLogin} className="login-form">
      <h2 className="login-title">Login</h2>

      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
        className="login-input"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
        className="login-input"
      />

      <button type="submit" className="login-button">
        Login
      </button>
    </form>
  );
}

export default Login;
