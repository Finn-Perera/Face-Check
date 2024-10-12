package com.fp.facecheck;

import com.fp.facecheck.dtos.BrandCountDTO;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long>, JpaSpecificationExecutor<Product> {
    @Query("SELECT new com.fp.facecheck.dtos.BrandCountDTO(p.productBrand, count(*)) FROM Product p GROUP BY p.productBrand")
    List<BrandCountDTO> findDistinctBrands();
}
