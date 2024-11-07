let currentActive = null;
let brandsList = [];

function collapseActive() {
    currentActive.querySelector('.extra-info').style.display = 'none';
    currentActive.classList.remove('active');
    currentActive = null;
}

document.addEventListener('DOMContentLoaded', function() {
    ratingsOnOpen()
    fetchProducts(null, null, null, null, null);
    fetchBrands();
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

    fetchProducts(minPrice, maxPrice, gatherChecked(), null, gatherRadioChecked())
});

// maybe display with 'greatest value' aka largest difference between low cost and average
function gatherChecked() {
    const checked = document.querySelectorAll('input[name="brand"]:checked');
    const selected = Array.from(checked).map(checked => checked.value);

    if (selected === undefined || selected.length == 0) {
        return null;
    }

    return selected;   
}

function gatherRadioChecked() {
    const checked = document.querySelector('input[name="radio-rating"]:checked');
    if (checked === undefined || checked === null) {
        return null;
    }
    value = parseFloat(checked.value);
    return value;
}

function searchProducts() {
    let input = document.getElementById('searchInput').value.toLowerCase();
    fetchProducts(null, null, null, input, null);
}

function createURL(minPrice, maxPrice, brands, search, rating) {
    let baseURL = 'http://localhost:8080/products';
    const params = new URLSearchParams();
    
    // If search is not null, then force search only
    // May change later
    if (search != null) {
        params.append('value', search);
        baseURL += '/search';
    } else {
        if (brands != null && brands !== undefined && brands.length !== 0) {
            for (let b of brands) {
                params.append('brand', b);
            }
        }
        if (minPrice != null && !isNaN(minPrice)) {
            params.append('min_price', minPrice);
        }
        if (maxPrice != null && !isNaN(maxPrice)) {
            params.append('max_price', maxPrice);
        }
        if (rating != null && !isNaN(rating) && rating >= 0) {
            params.append('rating', rating);
        }
    }

    return params.toString() ? `${baseURL}?${params.toString()}` : baseURL;
}

function ratingsOnOpen() {
    // this is weird, it seems to get them in reverse order?
    ratingWrappers = document.querySelectorAll('.rating-radio-wrapper');
    generateRating(0, 'red', ratingWrappers[5]);
    generateRating(1, 'red', ratingWrappers[4]);
    generateRating(2, 'red', ratingWrappers[3]);
    generateRating(3, 'yellow', ratingWrappers[2]);
    generateRating(4, 'green', ratingWrappers[1]);
    generateRating(5, 'green', ratingWrappers[0]);
}

function generateRating(filledStars, filledColor = 'red', wrapper) {
    const totalStars = 5;
    for (let i = 0; i < totalStars; i++) {
        const ratingDiv = document.createElement('span');
        ratingDiv.classList.add(i < filledStars ? 'filled-rating' : 'empty-rating');
        if (i < filledStars) {
            ratingDiv.classList.add(filledColor);
        }

        wrapper.appendChild(ratingDiv);
    }
    const plus = document.createElement('span');
    plus.textContent="+";
    wrapper.appendChild(plus);
  }

function fetchProducts(minPrice, maxPrice, brands, search, rating) {
    const fetchProdString = createURL(minPrice, maxPrice, brands, search, rating);
    fetch(fetchProdString)
    .then(response => {
        if (response.status === 204) {
            // No Content Response
            return []
        }
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
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

    if (products.length === 0) {
        const noProductsMessage = document.createElement('div');
        noProductsMessage.textContent = 'No products found.';
        noProductsMessage.classList.add('no-products-message');
        listOfItemsDoc.appendChild(noProductsMessage);
        return;
    }    

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

function fetchBrands() {
    fetch(`http://localhost:8080/brands`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(brands => {
        const checklistWrapper = document.querySelector(".checkbox-wrapper");
        brands.forEach(brand => {
            brandsList.push(brand);
        });
        brands.sort((a, b) => b.count - a.count);
        createBrandChecklist(brands, checklistWrapper);
    }).catch(error => console.error('Error fetching brands: ', error));
}

function createBrandChecklist(brandList, checklistWrapper) {
    let count = 0;
    while (count <= 10) {
        b = brandList[count];
        brandName = b.productBrand;
        brandCount = b.count;

        if (brandName === "") {
            brandName = "Others"; // find a way to put this at the bottom
        }
        inputElement = document.createElement('input');
        inputElement.type = "checkbox";
        inputElement.id =`${brandName}Checkbox`;
        inputElement.value = `${brandName}`;
        inputElement.name = "brand";

        labelElement = document.createElement('label');
        labelElement.htmlFor = `${brandName}Checkbox`;
        labelElement.textContent = `${brandName} (${brandCount})`;

        checklistWrapper.appendChild(inputElement);
        checklistWrapper.appendChild(labelElement);
        checklistWrapper.appendChild(document.createElement('br'));
        
        count += 1;
    }
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
