import { useEffect, useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";

const Favorites = () => {
  const { token } = useSelector((state) => state.auth);
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5555/favorites", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setFavorites(response.data);
      } catch (error) {
        console.error("Error fetching favorites:", error);
      }
    };

    fetchFavorites();
  }, [token]);

  return (
    <div className="grid grid-3">
      <h2 className="text-2xl font-bold">Your Favorite Recipes</h2>
      <div className="grid grid-cols-3 gap-4">
        {favorites.map((fav) => (
          <div key={fav.id} className="border p-4 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold">{fav.recipe_title}</h3>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Favorites;
