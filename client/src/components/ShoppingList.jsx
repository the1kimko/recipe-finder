import { useEffect, useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";

const ShoppingList = () => {
  const { token } = useSelector((state) => state.auth);
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchShoppingList = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5555/shopping_list", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setItems(response.data);
      } catch (error) {
        console.error("Error fetching shopping list:", error);
      }
    };

    fetchShoppingList();
  }, [token]);

  return (
    <div className="grid grid-3">
      <h2 className="text-2xl font-bold">Your Shopping List</h2>
      <ul className="list-disc ml-6">
        {items.map((item) => (
          <li key={item.id}>{item.item_name}</li>
        ))}
      </ul>
    </div>
  );
};

export default ShoppingList;
