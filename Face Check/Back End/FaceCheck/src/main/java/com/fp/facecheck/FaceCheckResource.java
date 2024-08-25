package com.fp.facecheck;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class FaceCheckResource {

    private final FaceCheckRepository repo;

    public FaceCheckResource(FaceCheckRepository repo) {
        this.repo = repo;
    }

    @GetMapping(value = "/", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<Item>> getItems() {

        try {

            List<Item> itemsToReturn = repo.findAll();
            return itemsToReturn.isEmpty() ?
                    ResponseEntity.notFound().build() :
                    ResponseEntity.ok(itemsToReturn);
        } catch (Exception e) {
            System.out.println("Internal Server Error: " + e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
