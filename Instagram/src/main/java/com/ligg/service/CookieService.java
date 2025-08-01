package com.ligg.service;

import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;

import java.util.Set;

/**
 * @Author Ligg
 * @Time 2025/7/28
 **/
public interface CookieService {

    /**
     * 添加单个 cookie
     */
    void addCookie(WebDriver driver, String name, String value, String domain, String path);


    /**
     * 删除所有 cookies
     */
    void deleteAllCookies(WebDriver driver);



    /**
     * 获取特定的 cookie 值
     */
    String getCookieValue(WebDriver driver, String cookieName);

    /**
     * 保存 cookies 到 JSON 文件
     */
    void saveCookiesToJson(WebDriver driver);

    /**
     * 从 JSON 文件加载 cookies
     */
    void loadCookiesFromJson(WebDriver driver);
}
