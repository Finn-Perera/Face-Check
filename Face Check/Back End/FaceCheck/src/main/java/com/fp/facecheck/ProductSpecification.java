package com.fp.facecheck;

import org.springframework.data.jpa.domain.Specification;

import java.util.List;

// a specification is a filter, using criteria to form a query on the db
public class ProductSpecification {
    private static final String PRODUCT_LOWEST_COST = "lowestCost";
    private static final String PRODUCT_BRAND_NAME = "productBrand";

    public static Specification<Product> hasPriceBetween(Double minPrice, Double maxPrice) {
        return ((root, query, criteriaBuilder) -> {
            if (minPrice == null && maxPrice == null) {
                return criteriaBuilder.conjunction();
            } else if (maxPrice == null) {
                return criteriaBuilder.greaterThanOrEqualTo(root.get(PRODUCT_LOWEST_COST), minPrice);
            } else if (minPrice == null) {
                return criteriaBuilder.lessThanOrEqualTo(root.get(PRODUCT_LOWEST_COST), maxPrice);
            } else {
                return criteriaBuilder.between(root.get(PRODUCT_LOWEST_COST), minPrice, maxPrice);
            }
        });
    }

    public static Specification<Product> hasBrand(List<String> brands) {
        return (root, query, criteriaBuilder) -> {
            if (brands == null || brands.isEmpty()) return criteriaBuilder.conjunction();
            return root.get(PRODUCT_BRAND_NAME).in(brands);
        };
    }
}
