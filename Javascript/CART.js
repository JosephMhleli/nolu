function redirectToProductPage(title, author, imagePath,price) {
    // Redirect to the product page and pass book information as query parameters
    const queryString = `?title=${encodeURIComponent(title)}&author=${encodeURIComponent(author)}&image=${encodeURIComponent(imagePath)}&price=${encodeURIComponent(price)}`;
    window.location.href = "/Pages/ProductPage.html" + queryString;
}

  
  function addToCart(event) {
    event.stopPropagation(); // Prevents the click on the link from triggering the click on the bookimg div
    // Add your logic for adding to the cart here
  }
  