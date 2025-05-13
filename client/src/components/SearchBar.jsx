import React, { useState, useEffect } from 'react';
import axios from 'axios';

let cancelToken;

export default function SearchBar({ onResults }) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query.trim()) return;

    const delayDebounce = setTimeout(() => {
      const fetchSearchResults = async () => {
        setLoading(true);

        if (cancelToken) cancelToken.cancel();
        cancelToken = axios.CancelToken.source();

        try {
          const response = await axios.get(`http://127.0.0.1:5555/recipes/explore`, {
            params: { q: query },
            cancelToken: cancelToken.token,
          });
          onResults({
            local: response.data.local || [],
            spoonacular: response.data.spoonacular || []
          });
        } catch (error) {
          if (!axios.isCancel(error)) console.error('Search failed:', error);
        } finally {
          setLoading(false);
        }
      };

      fetchSearchResults();
    }, 500);

    return () => clearTimeout(delayDebounce);
  }, [query, onResults]);

  return (
    <div className="my-4">
      <input
        type="text"
        className="border-2 border-primary rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-secondary"
        placeholder="Search recipes by ingredient or title..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {loading && <p className="text-sm text-gray-500 mt-1">Searching...</p>}
    </div>
  );
}
