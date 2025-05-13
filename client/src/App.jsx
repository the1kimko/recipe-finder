import { BrowserRouter, Router, Routes, Route } from "react-router-dom";
import { Provider } from "react-redux";
import Home from "./components/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Recipes from "./pages/Recipes";
import Favorites from "./components/Favorites";
import ShoppingList from "./components/ShoppingList";
import ProtectedRoute from "./components/ProtectedRoute";
//import store from "./redux/store";
import "./App.css";

function App() {
  return (
    <Routes>
      {/* PUBLIC ROUTES */}
      <Route path="/" element={<Home />} />
      <Route path="/recipes" element={<Recipes />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* PROTECTED ROUTES */}
      <Route element={<ProtectedRoute />}>
        <Route path="/favorites" element={<Favorites />} />
        <Route path="/shopping-list" element={<ShoppingList />} />
      </Route>
    </Routes>
  );
}

export default App;
