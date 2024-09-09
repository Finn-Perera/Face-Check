package com.fp.facecheck;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@RestController
public class FaceCheckResource {

    private final ProductRepository prodRepo;

    public FaceCheckResource(ProductRepository prodRepo) {
        this.prodRepo = prodRepo;
    }

    /**
     * Gathers all products
     *
     * @return List of products
     */
    @GetMapping(value = "/products", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<Product>> getProducts() {
        try {
            List<Product> productsToReturn = prodRepo.findAll();
            return productsToReturn.isEmpty() ?
                    ResponseEntity.notFound().build() :
                    ResponseEntity.ok(productsToReturn);
        } catch (Exception e) {
            System.out.println("Internal Server Error: " + e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Gathers all product options for a specified product
     *
     * @param id product id
     * @return List of product options
     */
    @GetMapping(value = "products/{id}/options", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<ProductOption>> getProductOptions(@PathVariable Long id) {
        try {
            Optional<Product> productOptional = prodRepo.findById(id);
            if (productOptional.isEmpty()) {
                return ResponseEntity.notFound().build();
            }

            List<ProductOption> optionsToReturn = productOptional.get().getOptions();
            if (optionsToReturn.isEmpty()) {
                return ResponseEntity.notFound().build();
            } else {
                return ResponseEntity.ok(optionsToReturn);
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
