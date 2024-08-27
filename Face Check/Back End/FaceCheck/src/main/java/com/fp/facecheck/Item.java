package com.fp.facecheck;

import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import jakarta.persistence.*;

@Entity
@Table(name="Items")
@JsonPropertyOrder({"id", "itemName", "price", "rating","numReviews","href", "imageUrl", "website"})
public class Item {
    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private int id;
    @Column
    private String itemName;
    @Column
    private double price;
    @Column
    private double rating;
    @Column
    private int numReviews;
    @Column
    private String href;
    @Column
    private String imageUrl;
    @Column
    private String website;

    public Item(String itemName, double price, double rating, int numReviews, String href, String imageUrl, String website) {
        this.itemName = itemName;
        this.price = price;
        this.rating = rating;
        this.numReviews = numReviews;
        this.href = href;
        this.imageUrl = imageUrl;
        this.website = website;
    }

    public Item() {

    }

    @Override
    public String toString() {
        return String.format(
                "Item[id=%d, name='%s', price=£%f, rating=%f, reviews=%d, website=%s]\n image_data=%s\n references=%s",
                id, itemName, price, rating, numReviews, website, imageUrl, href
        );
    }

    public String getName() {
        return itemName;
    }

    public void setName(String name) {
        this.itemName = name;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    public double getRating() {
        return rating;
    }

    public void setRating(int rating) {
        this.rating = rating;
    }

    public int getNumReviews() {
        return numReviews;
    }

    public void setNumReviews(int numReviews) {
        this.numReviews = numReviews;
    }

    public String getReferenceLink() {
        return href;
    }

    public void setReferenceLink(String referenceLink) {
        this.href = referenceLink;
    }

    public String getWebsite() {
        return website;
    }

    public void setWebsite(String website) {
        this.website = website;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
}
