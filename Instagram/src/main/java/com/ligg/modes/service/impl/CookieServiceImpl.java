package com.ligg.modes.service.impl;

import com.ligg.modes.service.CookieService;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Set;

/**
 * @Author Ligg
 * @Time 2025/7/28
 **/
public class CookieServiceImpl implements CookieService {

    private static final Logger log = LoggerFactory.getLogger(CookieServiceImpl.class);

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
    public void addCookies(WebDriver driver, Set<Cookie> cookies) {
        try {
            for (Cookie cookie : cookies) {
                driver.manage().addCookie(cookie);
                log.info("已添加 cookie: {} = {}", cookie.getName(), cookie.getValue());
            }
            log.info("批量添加 cookies 完成，共添加 {} 个", cookies.size());
        } catch (Exception e) {
            log.error("批量添加 cookies 失败: {}", e.getMessage());
        }
    }

    @Override
    public Set<Cookie> getAllCookies(WebDriver driver) {
        try {
            Set<Cookie> cookies = driver.manage().getCookies();
            log.info("获取到 {} 个 cookies", cookies.size());
            return cookies;
        } catch (Exception e) {
            log.error("获取 cookies 失败: {}", e.getMessage());
            return null;
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

    @Override
    public void addInstagramCookies(WebDriver driver) {
        try {
            // 直接添加Instagram cookies
            addCookie(driver, "datr", "SMBcaGd5pEN9TBbgTHpG5Zx6", ".instagram.com", "/");
            addCookie(driver, "ig_did", "9708FC04-B966-418F-AED7-5BA6E6E365F7", ".instagram.com", "/");
            addCookie(driver, "mid", "aFzASAALAAGXyzxb-4jLQyPiW8HD", ".instagram.com", "/");
            addCookie(driver, "ps_l", "1", ".instagram.com", "/");
            addCookie(driver, "ps_n", "1", ".instagram.com", "/");
            addCookie(driver, "ig_nrcb", "1", ".instagram.com", "/");
            addCookie(driver, "ig_lang", "zh-cn", ".instagram.com", "/");
            addCookie(driver, "csrftoken", "Xj5bMVMlT1ms39r99ExFxHIsDBKEYyKh", ".instagram.com", "/");
            addCookie(driver, "ds_user_id", "76340853733", ".instagram.com", "/");
            addCookie(driver, "sessionid", "76340853733%3A4Eu5FObeaV8V6f%3A25%3AAYfXRDonBAp8yY8iKpwGVG7QDgeKGJC_9v4H6JMN8g", ".instagram.com", "/");
            addCookie(driver, "rur", "EAG\\05476340853733\\0541785206563:01fe109f4c61b74b36f2caf50257917c8b49accbbca2b744961a229190dbdaad21fd8a91", ".instagram.com", "/");
            addCookie(driver, "wd", "823x767", ".instagram.com", "/");

            log.info("Instagram cookies 添加完成");
        } catch (Exception e) {
            log.error("添加 Instagram cookies 失败: {}", e.getMessage());
        }
    }

    @Override
    public void addInstagramCookies(WebDriver driver, String sessionId, String csrfToken, String mid, String igDid) {
        try {
            // sessionid cookie（最重要的登录状态 cookie）
            if (sessionId != null && !sessionId.isEmpty()) {
                addCookie(driver, "sessionid", sessionId, ".instagram.com", "/");
            }

            // csrftoken cookie
            if (csrfToken != null && !csrfToken.isEmpty()) {
                addCookie(driver, "csrftoken", csrfToken, ".instagram.com", "/");
            }

            // mid cookie
            if (mid != null && !mid.isEmpty()) {
                addCookie(driver, "mid", mid, ".instagram.com", "/");
            }

            // ig_did cookie
            if (igDid != null && !igDid.isEmpty()) {
                addCookie(driver, "ig_did", igDid, ".instagram.com", "/");
            }

            log.info("Instagram cookies 添加完成");
        } catch (Exception e) {
            log.error("添加 Instagram cookies 失败: {}", e.getMessage());
        }
    }
}
