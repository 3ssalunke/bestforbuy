export type TProduct = {
  name: string;
  price: number;
  features: string[];
  image_url: string;
  product_url: string;
  user_rating: number;
};

type TProductCardProps = {
  product: TProduct;
};

export default function ProductCard({ product }: TProductCardProps) {
  return (
    <div className="border rounded shadow p-4 w-full max-w-sm">
      <img
        src={product.image_url}
        alt={product.name}
        className="w-full h-40 object-cover mb-4 rounded"
      />
      <h2 className="text-xl font-semibold mb-2">{product.name}</h2>
      <p className="text-gray-700 mb-2">RS. {product.price}</p>
      <p className="text-sm text-gray-600">{product.features.join(", ")}</p>
      <p>⭐ {product.user_rating}</p>
    </div>
  );
}
