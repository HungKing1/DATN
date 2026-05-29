package com.example.backend.repository;

import com.example.backend.entity.LegalDocument;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface LegalDocumentRepository extends MongoRepository<LegalDocument, String> {
    Optional<LegalDocument> findBySoKyHieu(String soKyHieu);

    Page<LegalDocument> findByTrangThai(String trangThai, Pageable pageable);

    Page<LegalDocument> findByTenDayDuContainingIgnoreCaseOrSoKyHieuContainingIgnoreCase(
            String tenDayDu, String soKyHieu, Pageable pageable
    );
}
