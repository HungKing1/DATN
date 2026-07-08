package com.example.backend.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;

@Configuration
public class WebClientConfig {

        @Value("${ai-server.base-url}")
        private String aiServerBaseUrl;

        @Value("${ai-server.timeout:30000}")
        private int quickTimeout;

        @Value("${ai-server.agent-timeout:300000}")
        private int agentTimeout;

        private ExchangeStrategies exchangeStrategies() {
                return ExchangeStrategies.builder()
                                .codecs(configurer -> configurer
                                                .defaultCodecs()
                                                .maxInMemorySize(16 * 1024 * 1024))
                                .build();
        }

        @Bean
        public WebClient aiServerWebClient() {
                HttpClient httpClient = HttpClient.create()
                                .responseTimeout(Duration.ofMillis(quickTimeout));

                return WebClient.builder()
                                .baseUrl(aiServerBaseUrl)
                                .clientConnector(new ReactorClientHttpConnector(httpClient))
                                .exchangeStrategies(exchangeStrategies())
                                .defaultHeader("Content-Type", "application/json")
                                .build();
        }

        @Bean
        public WebClient aiServerAgentWebClient() {
                HttpClient httpClient = HttpClient.create()
                                .responseTimeout(Duration.ofMillis(agentTimeout));

                return WebClient.builder()
                                .baseUrl(aiServerBaseUrl)
                                .clientConnector(new ReactorClientHttpConnector(httpClient))
                                .exchangeStrategies(exchangeStrategies())
                                .defaultHeader("Content-Type", "application/json")
                                .build();
        }
}
