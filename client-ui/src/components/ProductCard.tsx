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
    <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-4 w-full max-w-sm">
      <img
        src={product.image_url}
        alt={product.name}
        className="w-full h-48 object-cover rounded-xl mb-4"
      />
      <h2 className="text-lg font-bold text-gray-800 mb-1">{product.name}</h2>
      <p className="text-primary text-lg font-semibold mb-1">
        ₹ {product.price}
      </p>

      <ul className="text-sm text-gray-600 list-disc pl-5 max-h-28 overflow-y-auto mb-2 custom-scrollbar">
        {product.features.map((feature, index) => (
          <li key={index}>{feature}</li>
        ))}
      </ul>

      <p className="text-yellow-500 text-sm font-medium mb-3">
        ⭐ {product.user_rating}
      </p>

      <a
        href={product.product_url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block bg-blue-600 text-white text-sm font-semibold px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
      >
        Buy Now
      </a>
    </div>
  );
}
