package com.fp.facecheck;

import jakarta.persistence.criteria.Predicate;
import org.springframework.data.jpa.domain.Specification;

import java.util.List;


// a specification is a filter, using criteria to form a query on the db
public class ProductSpecification {
    private static final String PRODUCT_LOWEST_COST = "lowestCost";
    private static final String PRODUCT_BRAND_NAME = "productBrand";
    private static final String PRODUCT_NAME = "productName";
    private static final String PRODUCT_RATING = "overallRating";
    private static final String WILDCARD_CHAR = "%";

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

    public static Specification<Product> hasRatingAbove(Double rating) {
        return ((root, query, criteriaBuilder) -> {
            if (rating == null) {
                return null;
            }
            return criteriaBuilder.greaterThanOrEqualTo(root.get(PRODUCT_RATING), rating);
        });
    }

    public static Specification<Product> hasBrand(List<String> brands) {
        return ((root, query, criteriaBuilder) -> {
            if (brands == null || brands.isEmpty()) return criteriaBuilder.conjunction();
            return root.get(PRODUCT_BRAND_NAME).in(brands);
        });
    }

    public static Specification<Product> searchByText(String searchText) {
        return ((root, query, criteriaBuilder) -> {
            String searchPattern = WILDCARD_CHAR + searchText.toLowerCase() + WILDCARD_CHAR;

            Predicate namePredicate = criteriaBuilder.like(criteriaBuilder.lower(root.get(PRODUCT_NAME)), searchPattern);
            Predicate brandPredicate = criteriaBuilder.like(criteriaBuilder.lower(root.get(PRODUCT_BRAND_NAME)), searchPattern);

            return criteriaBuilder.or(namePredicate, brandPredicate);
        });
    }
}
