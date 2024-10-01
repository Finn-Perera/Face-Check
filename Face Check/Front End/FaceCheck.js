let currentActive = null;


document.addEventListener('DOMContentLoaded', function() {
    createProducts();
});

function collapseActive() {
    currentActive.querySelector('.extra-info').style.display = 'none';
    currentActive.classList.remove('active');
    currentActive = null;
}
// maybe display with 'greatest value' aka largest difference between low cost and average

function createProducts() {
    fetch('http://localhost:8080/products')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        //console.log(response)
        return response.json();
    })
    .then(products => {
        console.log(products);

        console.log(products[0])

        const listOfItemsDoc = document.getElementById('items')
        products.forEach(element => {
            
            var product = document.createElement('div');
            product.classList.add('item');
            product.setAttribute('product_id', element.productId)

            nameOfProd = document.createElement('h4');
            nameOfProd.classList.add('line-clamped');
            nameOfProd.classList.add('product-name');
            nameOfProd.textContent = element.productName;

            imgOfProd = document.createElement('img');
            imgOfProd.src = element.productImage;
            imgOfProd.classList.add('item-image');
            imgOfProd.alt = "Description"; // change this

            itemDataWrapper = document.createElement('div');
            itemDataWrapper.classList.add('item-data-wrapper');
            
            imageWrapper = document.createElement('div');
            imageWrapper.classList.add('item-image-wrapper');
            
            itemWrapper = document.createElement('div');
            itemWrapper.classList.add('item-wrapper');


            //product.classList.add('active')
            extraInfo = document.createElement('div');
            extraInfo.classList.add('extra-info');
            extraInfo.style.display = 'none';

            optionsWrapper = document.createElement('div');
            optionsWrapper.classList.add('options-wrapper');
            extraInfo.appendChild(optionsWrapper);
            
            imageWrapper.appendChild(imgOfProd);
            itemDataWrapper.appendChild(imageWrapper);
            itemDataWrapper.appendChild(nameOfProd);
            
            product.appendChild(itemDataWrapper);
            product.appendChild(extraInfo);
            listOfItemsDoc.appendChild(product);
        });

        attachEventListeners();
        /*items.forEach(element => {
            var item = document.createElement('div');
            item.classList.add('item');
            
            nameOfProd = document.createElement('h4');
            nameOfProd.textContent = element.name;
            
            
            imageOfProd = document.createElement('img');
            imageOfProd.src = element.imageUrl;
            imageOfProd.classList.add('item-image');
            imageOfProd.alt="Description";

            imageWrapper = document.createElement('a');
            imageWrapper.classList.add('item-image-wrapper');
            imageWrapper.appendChild(imageOfProd);
            
            cost = document.createElement('h5');
            cost.textContent = "£" + element.price.toFixed(2); // rudimentary, only uk?

            review = document.createElement('div');
            review.classList.add('review');
            // these shouldnt be div but not sure what it should be yet
            reviewRating = document.createElement('div'); 
            reviewNum = document.createElement('div')
            reviewRating.textContent = element.rating + "★";
            reviewNum.textContent = element.numReviews + " Reviews";
            review.appendChild(reviewRating);
            review.appendChild(reviewNum);

            //refLink = document.createElement('a');
            imageWrapper.href = element.referenceLink;
            imageWrapper.target = '_blank';
            imageWrapper.rel = 'noopener noreferrer';
            //refLink.textContent = element.referenceLink;

            websiteOrigin = document.createElement('h6');
            websiteOrigin.textContent = element.website;
            
            item.appendChild(nameOfProd);
            item.appendChild(imageWrapper);
            item.appendChild(cost);
            item.appendChild(review);
            //item.appendChild(refLink);
            item.appendChild(websiteOrigin);

            listOfItemsDoc.appendChild(item);
        });*/
    })
    .catch(error => console.error('Error fetching items: ', error));
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
            console.log(option);
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

