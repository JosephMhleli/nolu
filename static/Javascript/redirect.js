
function redirectToProductPage(title, price, image_url, author, category) {
    // Construct the URL with query parameters using url_for
    var url = '/ProductPage';
    url += '?title=' + encodeURIComponent(title) +
           '&price=' + encodeURIComponent(price) +
           '&image_url=' + encodeURIComponent(image_url) +
           '&author=' + encodeURIComponent(author) +
           '&category=' + encodeURIComponent(category);

    // Redirect to the new page
    window.location.href = url;
}

