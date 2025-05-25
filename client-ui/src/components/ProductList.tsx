import ProductCard, { type TProduct } from "./ProductCard";

type TProductListProps = {
  products: TProduct[];
};

export default function ProductList({ products }: TProductListProps) {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">
        These are the top {products.length} AI suggested products
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {products.map((product, index) => (
          <ProductCard key={index} product={product} />
        ))}
      </div>
    </div>
  );
}
