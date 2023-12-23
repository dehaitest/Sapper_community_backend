// JavaScript to handle product data and search

// Initial products data
const allProducts = [
  {
    "ProductName": "Building Blocks Set",
    "ProductDescription": "A creative set of colorful building blocks to inspire imaginative play and problem-solving skills.",
    "ProductPrice": "$19.99"
  },
  {
    "ProductName": "Stuffed Teddy Bear",
    "ProductDescription": "A soft and cuddly teddy bear, perfect for snuggling and comforting children of all ages.",
    "ProductPrice": "$14.95"
  },
  {
    "ProductName": "Remote-Controlled Car",
    "ProductDescription": "An exciting remote-controlled car with high-speed capabilities, providing hours of fun for kids and adults alike.",
    "ProductPrice": "$29.99"
  },
  {
    "ProductName": "Art Supplies Kit",
    "ProductDescription": "A complete art supplies kit including paints, brushes, and canvases for young artists to unleash their creativity.",
    "ProductPrice": "$24.99"
  },
  {
    "ProductName": "Puzzle Game Set",
    "ProductDescription": "A collection of challenging and educational puzzles that promote cognitive development and problem-solving skills.",
    "ProductPrice": "$17.50"
  }
];

// Function to display products
function displayProducts(products) {
  const productList = document.getElementById('product-list');
  productList.innerHTML = '';
  products.forEach(product => {
    const card = document.createElement('div');
    card.classList.add('card', 'col', 's12');
    card.innerHTML = `
      <h5>${product.ProductName}</h5>
      <p>${product.ProductDescription}</p>
      <p><strong>${product.ProductPrice}</strong></p>
    `;
    productList.appendChild(card);
  });
}

// Event listener for user's search input
document.getElementById('search').addEventListener('input', () => {
  const searchTerm = document.getElementById('search').value.toLowerCase();
  const filteredProducts = allProducts.filter(product => {
    return product.ProductName.toLowerCase().includes(searchTerm) || product.ProductDescription.toLowerCase().includes(searchTerm);
  });
  displayProducts(filteredProducts);
});