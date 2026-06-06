package com.example.backend.mapper;

import com.example.backend.dto.response.UserResponse;
import com.example.backend.entity.User;

public class UserMapper {

    public static UserResponse toDto(User user) {
        if (user == null) return null;

        return UserResponse.builder()
                .id(user.getId())
                .email(user.getEmail())
                .role(user.getRole())
                .build();
    }
}
