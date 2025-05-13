import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { loginStart, loginSuccess, loginFailure } from "../redux/slices/authSlice";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    dispatch(loginStart());
    try {
      const response = await axios.post("http://127.0.0.1:5555/auth/login", { email, password });
      dispatch(loginSuccess(response.data));
      navigate("/dashboard");
    } catch (error) {
      dispatch(loginFailure(error.response?.data?.error || "Login failed"));
    }
  };

  return (
    <div className="page-wrapper">
      <div className="auth-container">
        <form onSubmit={handleLogin} className="auth-form">
          <h2>Welcome Back</h2>
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <button type="submit">Login</button>
        </form>
        <div className="auth-side">
          <h3>Recipe Finder</h3>
          <p>Find and save your favorite recipes with ease.</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
