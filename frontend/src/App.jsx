import { useState, useEffect } from "react";
import axios from "axios";
import ProductGrid from "./ProductGrid";
import AIAssistant from "./AIAssistant";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [products, setProducts] = useState([]);
  const [highlightedIds, setHighlightedIds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`${API_URL}/products`)
      .then((res) => setProducts(res.data))
      .catch((err) => console.error("Failed to load products:", err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Perfume Shop</h1>
        <p>Ask our AI assistant for a recommendation</p>
      </header>

      <AIAssistant apiUrl={API_URL} onResults={setHighlightedIds} />

      {loading ? (
        <p className="loading">Loading products...</p>
      ) : (
        <ProductGrid products={products} highlightedIds={highlightedIds} />
      )}
    </div>
  );
}

export default App;
