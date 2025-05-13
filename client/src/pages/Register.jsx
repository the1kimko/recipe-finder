import { useState } from "react";
import { useDispatch } from "react-redux";
import axios from "axios";
import { registerStart, registerSuccess, registerFailure } from "../redux/slices/authSlice";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    dispatch(registerStart());
    try {
      const response = await axios.post("http://127.0.0.1:5555/auth/register", formData);
      dispatch(registerSuccess(response.data));
      navigate("/login");
    } catch (error) {
      dispatch(registerFailure(error.response?.data?.error || "Registration failed"));
    }
  };

  return (
    <div className="page-wrapper">
      <div className="auth-container">
      <form onSubmit={handleRegister} className="auth-form">
        <h2>Register</h2>
        <input type="text" name="username" placeholder="Username" onChange={handleChange} />
        <input type="email" name="email" placeholder="Email" onChange={handleChange} />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} />
        <button type="submit">Register</button>
      </form>
      </div>
    </div>
  );
};

export default Register;
