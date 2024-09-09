package com.fp.facecheck;

import jakarta.persistence.*;

import java.sql.Timestamp;

@Entity
@Table(name = "product_options")
public class ProductOption {

    @Id
    @GeneratedValue
    private int optionId;
    @ManyToOne
    @JoinColumn(name = "product_id")
    private Product product;
    private double price;
    private double rating;
    private int numReviews;
    private String href;
    private String website;
    private Timestamp lastUpdated;

    public ProductOption() {
    }

    public ProductOption(Product product, double price, double rating, int numReviews, String href, String website, Timestamp lastUpdated) {
        this.product = product;
        this.price = price;
        this.rating = rating;
        this.numReviews = numReviews;
        this.href = href;
        this.website = website;
        this.lastUpdated = lastUpdated;
    }

    @Override
    public String toString() {
        return "ProductOption{" +
                "optionId=" + optionId +
                ", product=" + product +
                ", price=" + price +
                ", rating=" + rating +
                ", numReviews=" + numReviews +
                ", href='" + href + '\'' +
                ", website='" + website + '\'' +
                ", lastUpdated=" + lastUpdated +
                '}';
    }

    public int getOptionId() {
        return optionId;
    }

    public void setOptionId(int optionId) {
        this.optionId = optionId;
    }

    public Product getProduct() {
        return product;
    }

    public void setProduct(Product product) {
        this.product = product;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public double getRating() {
        return rating;
    }

    public void setRating(double rating) {
        this.rating = rating;
    }

    public int getNumReviews() {
        return numReviews;
    }

    public void setNumReviews(int numReviews) {
        this.numReviews = numReviews;
    }

    public String getHref() {
        return href;
    }

    public void setHref(String href) {
        this.href = href;
    }

    public String getWebsite() {
        return website;
    }

    public void setWebsite(String website) {
        this.website = website;
    }

    public Timestamp getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(Timestamp lastUpdated) {
        this.lastUpdated = lastUpdated;
    }
}
