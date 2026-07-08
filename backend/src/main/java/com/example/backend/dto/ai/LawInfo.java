package com.example.backend.dto.ai;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LawInfo {

    @JsonProperty("so_ky_hieu")
    private String soKyHieu;

    @JsonProperty("ten_day_du")
    private String tenDayDu;

    @JsonProperty("loai_van_ban")
    private String loaiVanBan;

    @JsonProperty("chunk_count")
    private int chunkCount;
}
