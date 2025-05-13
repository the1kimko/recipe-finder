import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import SearchBar from '../components/SearchBar';
import RecipeCard from '../components/RecipeCard';

export default function Home() {
  const [recipes, setRecipes] = useState([]);
  const [view, setView] = useState("all");
  const [error, setError] = useState(null);

  const API_BASE = "http://127.0.0.1:5555";

  const fetchRecipes = useCallback(async (query = "") => {
    try {
      const res = await axios.get(`${API_BASE}/recipes/explore`, { params: { q: query } });
      const { local, spoonacular } = res.data;
      setRecipes(
        view === "local" ? local :
        view === "spoonacular" ? spoonacular :
        [...local, ...spoonacular]
      );
    } catch {
      setError("Failed to fetch recipes.");
    }
  }, [view]);

  useEffect(() => {
    fetchRecipes();
  }, [fetchRecipes]);

  return (
    <div className="container">
      <h1 className="header">Recipe Finder</h1>

      <SearchBar onResults={data => {
        const { local = [], spoonacular = [] } = data;
        setRecipes(view === "local" ? local : view === "spoonacular" ? spoonacular : [...local, ...spoonacular]);
      }} />

      <label htmlFor="filter">Filter:</label>
      <select id="filter" value={view} onChange={e => setView(e.target.value)}>
        <option value="all">All</option>
        <option value="local">Local</option>
        <option value="spoonacular">Spoonacular</option>
      </select>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div className="recipe-grid">
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id || recipe.spoonacular_id} recipe={recipe} />
        ))}
      </div>

      <Link to="/recipes">Explore All Recipes →</Link>
    </div>
  );
}
