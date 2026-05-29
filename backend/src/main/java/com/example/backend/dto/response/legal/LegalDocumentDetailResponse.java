package com.example.backend.dto.response.legal;

import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
public class LegalDocumentDetailResponse {
    private String id;
    private String soKyHieu;
    private String tenDayDu;
    private String loaiVanBan;
    private String coQuanBanHanh;
    private String khoaQuocHoi;
    private String kyHop;
    private String ngayThongQua;
    private String chucDanhNguoiKy;
    private String tenNguoiKy;
    private String quocHieu;
    private String tieuNgu;
    private List<String> canCuBanHanh;

    private List<TocGroup> toc;
    private List<ArticleItem> articles;

    @Data
    @Builder
    public static class TocGroup {
        private String phan;
        private String chuong;
        private String muc;
        private List<TocEntry> items;
    }

    @Data
    @Builder
    public static class TocEntry {
        private String id;
        private Integer dieu;
        private String tenDieu;
        private String anchor;
    }

    @Data
    @Builder
    public static class ArticleItem {
        private String id;
        private Integer dieu;
        private String tenDieu;
        private String titleGoc;
        private String phan;
        private String chuong;
        private String muc;
        private String tieuMuc;
        private String content;
    }
}
