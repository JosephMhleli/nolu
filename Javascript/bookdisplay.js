const urlParams = new URLSearchParams(window.location.search);
        const title = urlParams.get('title');
        const author = urlParams.get('author');
        const imagePath = urlParams.get('image');
        const price = urlParams.get('price');

        // Use the book information as needed
        console.log('Title:', title);
        console.log('Author:', author);
        console.log('Image path:', imagePath);
        console.log('Price:', price);

        // Update your page content dynamically with the retrieved information
        const titleElement = document.getElementById('bookTitle');
        const authorElement = document.getElementById('bookAuthor');
        const imageElement = document.getElementById('bookImage');
        const priceElement = document.getElementById('bookPrice');

        if (titleElement) {
            titleElement.textContent = title;
        }

        if (authorElement) {
            authorElement.textContent = author;
        }

        if (imageElement) {
            imageElement.src = imagePath;
        }
        if (authorElement) {
            priceElement.textContent = price;
        }
        