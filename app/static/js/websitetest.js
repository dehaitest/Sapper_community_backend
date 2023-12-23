// Product Data
let allProducts = [
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
  
  // Display All Products
  function displayAllProducts() {
    let productsContainer = document.querySelector('.products-container');
    productsContainer.innerHTML = '';
    allProducts.forEach(product => {
      let productCard = document.createElement('div');
      productCard.classList.add('product-card');
      productCard.innerHTML = `
        <img src="" alt="Product Image">
        <h3>${product.ProductName}</h3>
        <p>${product.ProductPrice}</p>
        <p>${product.ProductDescription}</p>
      `;
      productsContainer.appendChild(productCard);
    });
  }
  
  // Search Products
  function searchProducts() {
    let searchInput = document.getElementById('search').value.toLowerCase();
    let filteredProducts = allProducts.filter(product => {
      return product.ProductName.toLowerCase().includes(searchInput) || product.ProductDescription.toLowerCase().includes(searchInput);
    });
    displayFilteredProducts(filteredProducts);
  }
  
  // Display Filtered Products
  function displayFilteredProducts(filteredProducts) {
    let productsContainer = document.querySelector('.products-container');
    productsContainer.innerHTML = '';
    filteredProducts.forEach(product => {
      let productCard = document.createElement('div');
      productCard.classList.add('product-card');
      productCard.innerHTML = `
        <img src="" alt="Product Image">
        <h3>${product.ProductName}</h3>
        <p>${product.ProductPrice}</p>
        <p>${product.ProductDescription}</p>
      `;
      productsContainer.appendChild(productCard);
    });
  }
  
  // Initial Load
  window.onload = function() {
    displayAllProducts();
  };