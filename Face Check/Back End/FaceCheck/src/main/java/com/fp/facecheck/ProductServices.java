package com.fp.facecheck;

import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;

import java.util.List;

// a service is just a middle layer where functions for accessing the repo are, generally for each table/entity
@Service
public class ProductServices {
    private final ProductRepository productRepository;

    public ProductServices(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public List<Product> findProducts(Double minPrice, Double maxPrice, List<String> brands) {
        Specification<Product> specification =
                Specification.where(ProductSpecification.hasPriceBetween(minPrice, maxPrice)
                        .and(ProductSpecification.hasBrand(brands)));

        return productRepository.findAll(specification);
    }

    public List<String> findDistinctProductBrands() {
        return productRepository.findDistinctBrands();
    }
}
