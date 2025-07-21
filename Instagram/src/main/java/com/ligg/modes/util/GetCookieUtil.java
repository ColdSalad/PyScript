package com.ligg.modes.util;

import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;

import java.util.Set;

/**
 * @Author Ligg
 * @Time 2025/7/17
 **/
public final class GetCookieUtil {

    /**
     * 获取指定名称和指定域名的Cookie
     *
     * @param driver     浏览器驱动
     * @param cookieName Cookie名称
     * @param domain     Cookie域
     * @return  Cookie对象
     */
    public static Cookie getCookieByNameAndDomain(WebDriver driver, String cookieName, String domain) {
        Set<Cookie> allCookies = driver.manage().getCookies();

        for (Cookie cookie : allCookies) {
            if (cookie.getName().equals(cookieName) && cookie.getDomain().equals(domain)) {
                return cookie;
            }
        }
        return null;
    }
}
