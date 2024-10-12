package com.fp.facecheck;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;

import java.util.List;

@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int productId;
    private String productName;
    private String productImage;
    private Double lowestCost;
    private String productBrand;
    @JsonIgnore
    @OneToMany(mappedBy = "product", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<ProductOption> options;

    public Product() {
    }

    public Product(int productId, String productName, String productImage, double lowestCost, String productBrand) {
        this.productId = productId;
        this.productName = productName;
        this.productImage = productImage;
        this.lowestCost = lowestCost;
        this.productBrand = productBrand;
    }

    @Override
    public String toString() {
        return "Product{" +
                "productId=" + productId +
                ", productName='" + productName + '\'' +
                ", productImage='" + productImage + '\'' +
                ", lowestCost=" + lowestCost +
                ", productBrand='" + productBrand + '\'' +
                ", options=" + options +
                '}';
    }

    public List<ProductOption> getOptions() {
        return options;
    }

    public int getProductId() {
        return productId;
    }

    public void setProductId(int productId) {
        this.productId = productId;
    }

    public String getProductName() {
        return productName;
    }

    public void setProductName(String productName) {
        this.productName = productName;
    }

    public String getProductImage() {
        return productImage;
    }

    public void setProductImage(String productImage) {
        this.productImage = productImage;
    }

    public Double getLowestCost() {
        return lowestCost;
    }

    public void setLowestCost(Double lowestCost) {
        this.lowestCost = lowestCost;
    }

    public String getProductBrand() {
        return productBrand;
    }

    public void setProductBrand(String productBrand) {
        this.productBrand = productBrand;
    }
}
