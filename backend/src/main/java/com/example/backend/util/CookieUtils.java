package com.example.backend.util;

import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Value;

@Component
public class CookieUtils {

    @Value("${auth.cookie.name}")
    private String cookieName;

    @Value("${auth.cookie.max-age}")
    private int cookieMaxAge;

    @Value("${auth.cookie.secure}")
    private boolean cookieSecure;

    @Value("${auth.cookie.http-only}")
    private boolean cookieHttpOnly;

    public String extractSessionId(HttpServletRequest request) {
        if (request.getCookies() == null) {
            return null;
        }
        for (Cookie cookie : request.getCookies()) {
            if (cookieName.equals(cookie.getName())) {
                return cookie.getValue();
            }
        }
        return null;
    }

    public void addSessionCookie(HttpServletResponse response, String sessionId) {
        Cookie cookie = new Cookie(cookieName, sessionId);
        cookie.setHttpOnly(cookieHttpOnly);
        cookie.setSecure(cookieSecure);
        cookie.setPath("/");
        cookie.setMaxAge(cookieMaxAge);
        response.addCookie(cookie);
    }

    public void clearSessionCookie(HttpServletResponse response) {
        Cookie cookie = new Cookie(cookieName, null);
        cookie.setHttpOnly(cookieHttpOnly);
        cookie.setSecure(cookieSecure);
        cookie.setPath("/");
        cookie.setMaxAge(0);
        response.addCookie(cookie);
    }
}
