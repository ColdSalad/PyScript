package com.ligg.service.impl;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ligg.service.CookieService;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * @Author Ligg
 * @Time 2025/7/28
 **/
public class CookieServiceImpl implements CookieService {

    private static final Logger log = LoggerFactory.getLogger(CookieServiceImpl.class);
    private static final String COOKIE_FILE_PATH = "instagram_cookies.json";
    private static final Gson gson = new GsonBuilder().setPrettyPrinting().create();

    @Override
    public void addCookie(WebDriver driver, String name, String value, String domain, String path) {
        try {
            Cookie cookie = new Cookie.Builder(name, value)
                    .domain(domain)
                    .path(path)
                    .build();
            driver.manage().addCookie(cookie);
            log.info("已添加 cookie: {} = {}", name, value);
        } catch (Exception e) {
            log.error("添加 cookie 失败: {}", e.getMessage());
        }
    }




    @Override
    public void deleteAllCookies(WebDriver driver) {
        try {
            driver.manage().deleteAllCookies();
            log.info("已删除所有 cookies");
        } catch (Exception e) {
            log.error("删除 cookies 失败: {}", e.getMessage());
        }
    }

    /**
     * 获取特定的 cookie 值
     * @param driver WebDriver实例
     * @param cookieName cookie名称
     * @return cookie值，如果不存在返回null
     */
    public String getCookieValue(WebDriver driver, String cookieName) {
        try {
            Cookie cookie = driver.manage().getCookieNamed(cookieName);
            if (cookie != null) {
                log.info("获取到 cookie: {} = {}", cookieName, cookie.getValue());
                return cookie.getValue();
            } else {
                log.warn("未找到 cookie: {}", cookieName);
                return null;
            }
        } catch (Exception e) {
            log.error("获取 cookie 失败: {}", e.getMessage());
            return null;
        }
    }

    /**
     * 保存 cookies 到 JSON 文件
     * @param driver WebDriver实例
     */
    public void saveCookiesToJson(WebDriver driver) {
        try {
            Set<Cookie> cookies = driver.manage().getCookies();
            Map<String, String> cookieMap = new HashMap<>();

            for (Cookie cookie : cookies) {
                cookieMap.put(cookie.getName(), cookie.getValue());
            }

            // 保存到 JSON 文件
            try (FileWriter writer = new FileWriter(COOKIE_FILE_PATH)) {
                gson.toJson(cookieMap, writer);
                log.info("Cookies 已保存到文件: {}", COOKIE_FILE_PATH);
            } catch (IOException e) {
                log.error("保存 cookies 到文件失败: {}", e.getMessage());
            }
        } catch (Exception e) {
            log.error("获取 cookies 失败: {}", e.getMessage());
        }
    }

    /**
     * 从 JSON 文件加载 cookies
     * @param driver WebDriver实例
     */
    public void loadCookiesFromJson(WebDriver driver) {
        try {
            if (!Files.exists(Paths.get(COOKIE_FILE_PATH))) {
                log.warn("Cookie 文件不存在: {}", COOKIE_FILE_PATH);
                return;
            }

            String jsonContent = new String(Files.readAllBytes(Paths.get(COOKIE_FILE_PATH)));
            Map<String, String> cookieMap = gson.fromJson(jsonContent, Map.class);

            for (Map.Entry<String, String> entry : cookieMap.entrySet()) {
                addCookie(driver, entry.getKey(), entry.getValue(), ".instagram.com", "/");
            }

            log.info("从文件加载了 {} 个 cookies", cookieMap.size());
        } catch (Exception e) {
            log.error("从文件加载 cookies 失败: {}", e.getMessage());
        }
    }
}
