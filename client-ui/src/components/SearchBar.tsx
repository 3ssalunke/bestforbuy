import { useState } from "react";

type TSearchBarProps = {
  onSearch: (query: string) => void;
};

export default function SearchBar({ onSearch }: TSearchBarProps) {
  const [query, setQuery] = useState("");

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for best products..."
        className="border px-4 py-2 rounded w-full"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Find Products
      </button>
    </form>
  );
}
