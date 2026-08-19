function ProductGrid({ products, highlightedIds = [] }) {
  return (
    <div className="product-grid">
      {products.map((product) => (
        <div
          key={product.id}
          className={`product-card ${
            highlightedIds.includes(product.id) ? "highlighted" : ""
          }`}
        >
          <h3>{product.name}</h3>
          <p className="brand">{product.brand}</p>
          <p className="description">{product.description}</p>
          <div className="product-footer">
            <span className="price">${product.price.toFixed(2)}</span>
            <span className="category">{product.category}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ProductGrid;
