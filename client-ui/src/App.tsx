import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ProductList from "./components/ProductList";
import type { TProduct } from "./components/ProductCard";

const prompt = `
  Give me 5 best {productType} in the range of {minPrice}-{maxPrice} by comaparing at least {productLimit} available. While comparing take description, user rating, reviews count into consideration.
  Give the response having following fields in nice json format - name, price, features in array of strings, image_url, product_url, user_rating. The result should be under suggesitons field.
  Please don't add any new line characters.
`;

export default function App() {
  const [products, setProducts] = useState<TProduct[]>([]);

  const handleSearch = async (query: string) => {
    const reqPayload = {
      query: prompt
        .replace("{productType}", query)
        .replace("{minPrice}", "10000")
        .replace("{maxPrice}", "30000")
        .replace("{productLimit}", "30"),
    };

    const response = await fetch("http://localhost:3000/product/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(reqPayload),
    });

    const { products } = await response.json();

    setProducts(products);
  };

  return (
    <div className="max-w-5xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Find Your Ideal Product</h1>
      <SearchBar onSearch={handleSearch} />
      <ProductList products={products} />
    </div>
  );
}
