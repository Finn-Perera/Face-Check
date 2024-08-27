function addItem() {
    const itemList = document.getElementById('items');
    const newItem = document.createElement('i');
    newItem.textContent = 'an item';
    newItem.classList.add('item')
    itemList.appendChild(newItem);
}

const itemsButton = document.getElementById('items-button');
itemsButton.addEventListener('click', () => {
    itemsContainer = document.getElementById('items-section');
    computedStyle = window.getComputedStyle(itemsContainer);

    if (computedStyle.contentVisibility === 'hidden') {
        itemsContainer.style.contentVisibility = 'auto';
    } else {
        itemsContainer.style.contentVisibility = 'hidden';
    }
});

// document.addEventListener('DOMContentLoaded', function() {
//     const button = document.getElementById('addItemButton');
//     button.addEventListener('click', addItem);
// });

document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8080/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(items => {
            console.log(items);
            if (!items.status === 'success') { // theres no status in my json this useless.
                throw new Error('Error getting data')
            }
            //console.log(data.name)
            console.log(items[0])
            if (Array.isArray(items)) {
                console.log('this works');
            }

            const listOfItemsDoc = document.getElementById('items')
            items.forEach(element => {
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
            });
        })
        .catch(error => console.error('Error fetching items: ', error));

});