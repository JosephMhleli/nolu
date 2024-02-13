
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
function addToWish(imageUrl, title, author, price, category) {
    const bookDetails = {
        image_url: imageUrl,
        title: title,
        author: author,
        price: price,
        category: category
    };

    fetch('/Favorites/post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookDetails),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            // Optionally, redirect to the Favorites page if the book was added successfully
            window.location.href = '/Favorites';
        }
    })
    .catch(error => {
        console.error('Error adding book to wishlist:', error);
        alert('Error adding book to wishlist. Please try again.');
    });
}


function bookreq(){
    var url = '/requestBook';
    //redirecting to the page window
    window.location.href = url;
}
function getToken() {
    const cookies = document.cookie.split('; ');
    const tokenCookie = cookies.find(row => row.startsWith('token='));

    if (tokenCookie) {
        return tokenCookie.split('=')[1];
    } else {
        // Token cookie not found
        return null;
    }
}

function addToCart(image_url, title, author, price) {
    // Assuming you have a function to retrieve the token, replace getToken() with that function.
//     var token = getToken();
//    console.log('token is ',token)
    // Check if variables are defined and have values
    if (image_url && title && author && price && token) {
        // Make an AJAX request to the server
        $.ajax({
            type: "POST",
            url: "/AddtoCart",
            // headers: {
            //     'Authorization': 'Bearer ' + token
            // },
            data: {
                image_url: image_url,
                title: title,
                author: author,
                price: price
            },
            success: function(response) {
                // Update the cart counter and handle any other UI updates
                updateCartCounter(response.cart_count);
            },
            error: function(error) {
                console.error("Error adding to cart:", error);
            }
        });
    } else {
        console.error("One or more variables are undefined or null.");
    }
}


function updateCartCounter(count) {
    // Update the cart counter in the UI
    // For example, assuming you have a cart counter element with id "cartCounter"
    $("#cartCounter").text(count);
}

$("#cartContainer").hover(
    function() {
        // Show cart contents on hover
        $("#cartContents").removeClass("hidden");
    },
    function() {
        // Hide cart contents when not hovering
        $("#cartContents").addClass("hidden");
    }
);

function proceedToCheckout() {
    
}
function getToken() {
    const cookies = document.cookie.split('; ');
    const tokenCookie = cookies.find(row => row.startsWith('token='));

    if (tokenCookie) {
        return tokenCookie.split('=')[1];
    } else {
        // Token cookie not found
        return null;
    }
}

