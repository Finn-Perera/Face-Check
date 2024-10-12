package com.fp.facecheck.dtos;

public class BrandCountDTO {
    private String productBrand;
    private Long count;

    public BrandCountDTO(String productBrand, Long count) {
        this.productBrand = productBrand;
        this.count = count;
    }

    public String getProductBrand() {
        return productBrand;
    }

    public void setProductBrand(String productBrand) {
        this.productBrand = productBrand;
    }

    public Long getCount() {
        return count;
    }

    public void setCount(Long count) {
        this.count = count;
    }
}
