import axios from 'axios';

export const exploreRecipes = async (query = "") => {
    const response = await axios.get(`http://127.0.0.1:5555/recipes/explore?q=${query}`);
    return response.data;
};
  