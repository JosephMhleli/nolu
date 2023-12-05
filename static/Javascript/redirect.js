
function redirectToProductPage(title, price, image_url, author, category,descri) {
    // Construct the URL with query parameters using url_for
    var url = '/ProductPage';
    url += '?title=' + encodeURIComponent(title) +
           '&price=' + encodeURIComponent(price) +
           '&image_url=' + encodeURIComponent(image_url) +
           '&author=' + encodeURIComponent(author) +           
           '&category=' + encodeURIComponent(category)+
           '&descri='+ encodeURIComponent(descri);

    // Redirect to the new page
    window.location.href = url;
}


function bookreq(){
    var url = '/requestBook';
    //redirecting to the page window
    window.location.href = url;
}

function addToCart(event, itemImg, itemName, itemAuthor, itemPrice) {
    const cartCountElement = document.getElementById('cartcount');
    const cartItemsElement = document.getElementById('cart-items');

    // Increment cart count (you should replace this with your actual logic)
    const currentCount = parseInt(cartCountElement.innerText, 10);
    cartCountElement.innerText = currentCount + 1;

    // Update cart dropdown content (you should replace this with your actual logic)
    let cartContent = cartItemsElement.innerHTML;
    if (cartContent === "Cart is empty") {
        cartContent = ''; // Clear the default message
    }

    // Generate a unique ID for each cart item
    const itemId = `cart-item-${currentCount}`;

    // Add the selected item to the cart with HTML markup
    cartContent += `
        <div id="${itemId}" class="cart-item">
            <img src="${itemImg}" alt="${itemName} image" class="cart-item-image">
            <div class="cart-item-details">
                <p class="cart-item-title">${itemName}</p>
                <p class="cart-item-author">Author: ${itemAuthor}</p>
                <p class="cart-item-price">Price: ${itemPrice}</p>
            </div>
            <button class="remove-item-btn" onclick="removeCartItem('${itemId}')">Remove</button>
        </div>`;

    cartItemsElement.innerHTML = cartContent;
}





function removeCartItem(itemId) {
    // Remove the cart item with the specified ID
    const cartItem = document.getElementById(itemId);
    if (cartItem) {
        cartItem.remove();
    }

    // Update the cart count (you should replace this with your actual logic)
    const cartCountElement = document.getElementById('cartcount');
    const currentCount = parseInt(cartCountElement.innerText, 10);
    cartCountElement.innerText = Math.max(0, currentCount - 1);
}