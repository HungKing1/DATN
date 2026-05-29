package com.example.backend.repository;

import com.example.backend.entity.LegalArticle;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LegalArticleRepository extends MongoRepository<LegalArticle, String> {
    List<LegalArticle> findByDocumentIdOrderByDieuAsc(ObjectId documentId);
    List<LegalArticle> findByIdIn(List<String> ids);
}
