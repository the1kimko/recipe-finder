import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllRecipes } from "../redux/slices/recipeSlice";
import RecipeCard from "../components/RecipeCard";

const Recipes = () => {
  const dispatch = useDispatch();
  const { items: recipes, loading, error } = useSelector((state) => state.recipes);

  useEffect(() => {
    dispatch(fetchAllRecipes());
  }, [dispatch]);

  return (
    <section className="px-6 py-10">
      <h1 className="text-3xl font-bold mb-4">🍳 Explore All Recipes</h1>

      {loading && <p>Loading recipes...</p>}
      {error && <p className="text-red-500">{error.msg || error.toString()}</p>}

      <div className="grid sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6">
        {recipes.map((r) => (
          <RecipeCard key={r.id || r.spoonacular_id} recipe={r} />
        ))}
      </div>
    </section>
  );
};

export default Recipes;
