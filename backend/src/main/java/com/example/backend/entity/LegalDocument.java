package com.example.backend.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Document(collection = "legal_documents")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LegalDocument {
    @Id
    private String id;

    @Field("so_ky_hieu")
    private String soKyHieu;

    @Field("ten_day_du")
    private String tenDayDu;

    @Field("loai_van_ban")
    private String loaiVanBan;

    @Field("co_quan_ban_hanh")
    private String coQuanBanHanh;

    @Field("khoa_quoc_hoi")
    private String khoaQuocHoi;

    @Field("ky_hop")
    private String kyHop;

    @Field("ngay_thong_qua")
    private LocalDate ngayThongQua;

    @Field("ngay_hieu_luc")
    private LocalDate ngayHieuLuc;

    @Field("chuc_danh_nguoi_ky")
    private String chucDanhNguoiKy;

    @Field("ten_nguoi_ky")
    private String tenNguoiKy;

    @Field("quoc_hieu")
    private String quocHieu;

    @Field("tieu_ngu")
    private String tieuNgu;

    @Field("can_cu_ban_hanh")
    private List<String> canCuBanHanh;

    @Field("tong_so_dieu")
    private Integer tongSoDieu;

    private List<String> body;

    @Field("trang_thai")
    private String trangThai;

    @Field("created_at")
    private LocalDateTime createdAt;

    @Field("updated_at")
    private LocalDateTime updatedAt;
}
