import ProductCard, { type TProduct } from "./ProductCard";

type TProductListProps = {
  products: TProduct[];
};

export default function ProductList({ products }: TProductListProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {products.map((product, index) => (
        <ProductCard key={index} product={product} />
      ))}
    </div>
  );
}
