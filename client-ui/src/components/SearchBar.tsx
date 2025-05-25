import { useState } from "react";

type TSearchBarProps = {
  onSearch: (
    query: string,
    minPrice: string,
    maxPrice: string,
    count: string
  ) => void;
};

export default function SearchBar({ onSearch }: TSearchBarProps) {
  const [query, setQuery] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [count, setCount] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    await onSearch(query, minPrice, maxPrice, count);
    setIsLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-4 flex-wrap">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Product name..."
        className="border px-4 py-2 rounded w-full sm:w-auto"
      />
      <input
        type="number"
        value={minPrice}
        onChange={(e) => setMinPrice(e.target.value)}
        placeholder="Min product price..."
        className="border px-4 py-2 rounded w-full sm:w-auto"
        min="0"
      />
      <input
        type="number"
        value={maxPrice}
        onChange={(e) => setMaxPrice(e.target.value)}
        placeholder="Max product price..."
        className="border px-4 py-2 rounded w-full sm:w-auto"
        min="0"
      />
      <input
        type="number"
        value={count}
        onChange={(e) => setCount(e.target.value)}
        placeholder="Product count..."
        className="border px-4 py-2 rounded w-full sm:w-auto"
        min="1"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {isLoading ? "Finding Products..." : "Find Products"}
      </button>
    </form>
  );
}
