let currentActive = null;

function collapseActive() {
    currentActive.querySelector('.extra-info').style.display = 'none';
    currentActive.classList.remove('active');
    currentActive = null;
}

document.addEventListener('DOMContentLoaded', function() {
    fetchProducts(null, null);
});

document.getElementById("price-filter-button").addEventListener('click', () => {
    const minPrice = document.getElementById("minPrice").value;
    const maxPrice = document.getElementById("maxPrice").value;

    if (isNaN(minPrice) || (minPrice < 0)) {
        return
    }

    if (isNaN(maxPrice) || (maxPrice < 0)) {
        return;
    }

    fetchProducts(minPrice, maxPrice)
})

// maybe display with 'greatest value' aka largest difference between low cost and average

function fetchProducts(minPrice, maxPrice) {
    const baseURL = 'http://localhost:8080/products';
    const params = new URLSearchParams();
    
    if (minPrice != null && !isNaN(minPrice)) {
        params.append('min_price', minPrice);
    }
    if (maxPrice != null && !isNaN(maxPrice)) {
        params.append('max_price', maxPrice);
    }

    const fetchProdString = params.toString() ? `${baseURL}?${params.toString()}` : baseURL;

    fetch(fetchProdString)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        //console.log(response)
        return response.json();
    })
    .then(products => {
        createProducts(products)

        attachEventListeners();
    })
    .catch(error => console.error('Error fetching items: ', error));
}

function createProducts(products) {
    const listOfItemsDoc = document.getElementById('items')
    listOfItemsDoc.innerHTML = ''; // clears items

    products.forEach(element => {
    // Building the item html
    var product = document.createElement('div');

    // Setting css class and attributes
    product.classList.add('item');
    product.setAttribute('product_id', element.productId) // good/bad idea?

    // Name Element
    nameOfProd = document.createElement('h4');
    nameOfProd.classList.add('line-clamped');
    nameOfProd.classList.add('product-name');
    nameOfProd.textContent = element.productName;

    // Lowest Cost Element
    lowestCostOfProd = document.createElement('a'); // make linkable?
    lowestCostOfProd.classList.add('product-lowest-cost');
    lowestCostOfProd.textContent = `£${parseFloat(element.lowestCost).toFixed(2)}`;

    // Image Element
    imgOfProd = document.createElement('img');
    imgOfProd.src = element.productImage;
    imgOfProd.classList.add('item-image');
    imgOfProd.alt = "Description"; // change this, could be prod name
    imgOfProd.draggable = false;

    // Image Wrapper
    imageWrapper = document.createElement('div');
    imageWrapper.classList.add('item-image-wrapper');
    imageWrapper.appendChild(imgOfProd);

    // Data Wrapper containing name, image, low cost
    itemDataWrapper = document.createElement('div');
    itemDataWrapper.classList.add('item-data-wrapper');
    itemDataWrapper.appendChild(imageWrapper);
    itemDataWrapper.appendChild(nameOfProd);
    itemDataWrapper.appendChild(lowestCostOfProd);
    // add lowest cost item
    
    // Deprecated??
    itemWrapper = document.createElement('div');
    itemWrapper.classList.add('item-wrapper');

    // Pop-out information displaying product options
    extraInfo = document.createElement('div');
    extraInfo.classList.add('extra-info');
    extraInfo.style.display = 'none';

    // Options Wrapper holds product's options
    optionsWrapper = document.createElement('div');
    optionsWrapper.classList.add('options-wrapper');
    extraInfo.appendChild(optionsWrapper);
    
    // Bring wrappers and elements together
    product.appendChild(itemDataWrapper);
    product.appendChild(extraInfo);

    // Add to item display panel
    listOfItemsDoc.appendChild(product);
    });
}

// whenever you call you should check that the element doesnt already have the info
function fetchExtraInfo(prodId, optionsWrapperElement) {
    fetch(`http://localhost:8080/products/${prodId}/options`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(options => {
        options.forEach(option => {
            optionElement = document.createElement('div');
            optionElement.classList.add('option-element');

            optionWebsite = document.createElement('p');
            optionPriceWrap = document.createElement('a'); // maybe wrap this in a div,discount colors?
            optionRating = document.createElement('div');
            
            price = option.price;
            price = parseFloat(price).toFixed(2)
            optionPriceWrap.textContent = `£${price}`;
            optionPriceWrap.classList.add('no-style-link');
            optionPriceWrap.classList.add('price-wrap');

            rating = option.rating;
            numReviews = option.numReviews;
            optionRating.textContent = `${rating} Stars out of 5, ${numReviews} reviews`
            optionWebsite.textContent = option.website;
            
            // add in last updated?
            hrefLink = option.href;
            optionPriceWrap.href = hrefLink;
            optionPriceWrap.target = '_blank';

            
            optionElement.appendChild(optionWebsite);
            optionElement.appendChild(optionRating);
            optionElement.appendChild(optionPriceWrap);
            optionsWrapperElement.appendChild(optionElement);
        })
    })
    .catch(error => console.error('Error fetching extra information: ', error));
}

function attachEventListeners() {
    // likely can be done on creation?
    document.querySelectorAll(".item").forEach(product => {
        product.addEventListener('click', function(event) {
            event.stopPropagation()
            this.classList.toggle('active');
            const extraInfo = this.querySelector('.extra-info');
            const isActive = this.classList.contains('active');
    
            if (extraInfo.style.display === 'block') {
                extraInfo.style.display = 'none';
            } else {
                extraInfo.style.display = 'block';
            }

            if (currentActive && currentActive != this) {
                collapseActive();
            }
            
            currentActive = this.classList.contains('active') ? this : null;
            
            // could cause problems?
            this.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
            
            const optionWrap = extraInfo.querySelector('.options-wrapper');
    
            if (!optionWrap.classList.contains("loaded")) {
                fetchExtraInfo(this.getAttribute("product_id"), optionWrap);
                optionWrap.classList.add('loaded');
            }
        });
    });

    document.addEventListener('click', function() {
        if (currentActive) {
            collapseActive();
        }
    })
}

