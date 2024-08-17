package com.fp.facecheck;

public class Item {
    private String name;
    private int price;
    private int rating;
    private int numReviews;
    private String referenceLink;
    private String website;

    public Item(String name, int price, int rating, int numReviews, String referenceLink, String website) {
        this.name = name;
        this.price = price;
        this.rating = rating;
        this.numReviews = numReviews;
        this.referenceLink = referenceLink;
        this.website = website;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getPrice() {
        return price;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    public int getRating() {
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
        return referenceLink;
    }

    public void setReferenceLink(String referenceLink) {
        this.referenceLink = referenceLink;
    }

    public String getWebsite() {
        return website;
    }

    public void setWebsite(String website) {
        this.website = website;
    }
}
