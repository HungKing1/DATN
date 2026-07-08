package com.example.backend.controller;

import com.example.backend.dto.ai.DeleteLawResponse;
import com.example.backend.dto.ai.LawCreateResponse;
import com.example.backend.dto.ai.LawInfo;
import com.example.backend.dto.response.ApiResponse;
import com.example.backend.service.AiServerClient;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/v1/admin")
@RequiredArgsConstructor
public class AdminController {

    private final AiServerClient aiServerClient;

    @GetMapping("/laws")
    public ApiResponse<List<LawInfo>> listLaws() {
        log.debug("Admin listing all laws from Weaviate");
        List<LawInfo> laws = aiServerClient.listLaws();
        return ApiResponse.success(laws);
    }

    @PostMapping("/laws")
    public ApiResponse<LawCreateResponse> createLaw(@RequestBody Map<String, String> body) {
        String soKyHieu = body.get("so_ky_hieu");
        if (soKyHieu == null || soKyHieu.trim().isEmpty()) {
            throw new IllegalArgumentException("so_ky_hieu is required in the request body");
        }
        log.info("Admin ingesting Law from MongoDB: {}", soKyHieu);
        LawCreateResponse response = aiServerClient.ingestFromMongodb(soKyHieu);
        return ApiResponse.success(response);
    }

    @PostMapping("/laws/reload")
    public ApiResponse<LawCreateResponse> reloadLaw(
            @RequestParam String soKyHieu,
            @RequestBody Map<String, String> body) {
        String soKyHieuBody = body.get("so_ky_hieu");
        if (soKyHieuBody == null || soKyHieuBody.trim().isEmpty()) {
            soKyHieuBody = soKyHieu;
        }
        log.info("Admin reloading Law so_ky_hieu={} from MongoDB", soKyHieu);
        LawCreateResponse response = aiServerClient.reloadLaw(soKyHieu, soKyHieuBody);
        return ApiResponse.success(response);
    }

    @DeleteMapping("/laws")
    public ApiResponse<DeleteLawResponse> deleteLaw(@RequestParam String soKyHieu) {
        log.info("Admin cascade-deleting Law so_ky_hieu={}", soKyHieu);
        DeleteLawResponse response = aiServerClient.deleteLaw(soKyHieu);
        return ApiResponse.success(response);
    }

    @GetMapping("/ai-health")
    public ApiResponse<Map<String, Object>> aiServerHealth() {
        Map<String, Object> healthStatus = aiServerClient.checkHealth();
        return ApiResponse.success(healthStatus);
    }
}
