package com.example.backend.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;

@Document(collection = "legal_articles")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LegalArticle {
    @Id
    private String id;

    @Field("document_id")
    private ObjectId documentId;

    private Integer dieu;

    @Field("ten_dieu")
    private String tenDieu;

    @Field("title_goc")
    private String titleGoc;

    private ArticlePath path;

    private String content;

    @Field("created_at")
    private LocalDateTime createdAt;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ArticlePath {
        private String phan;
        private String chuong;
        private String muc;
        @Field("tieu_muc")
        private String tieuMuc;
    }
}
