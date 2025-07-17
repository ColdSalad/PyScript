package com.ligg.modes.util;

import com.google.gson.Gson;
import com.ligg.modes.automation.OpenBrowser;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;
import java.util.Set;

/**
 * @Author Ligg
 * @Time 2025/7/17
 **/
public final class CookieUtil {
    private static final Logger log = LoggerFactory.getLogger(OpenBrowser.class);


    /**
     * 获取指定名称和指定域名的Cookie
     *
     * @param driver     浏览器驱动
     * @param cookieName Cookie名称
     * @param domain     Cookie域
     * @return Cookie对象
     */
    public static String getCookieByNameAndDomain(WebDriver driver, String cookieName, String domain) {
        Set<Cookie> allCookies = driver.manage().getCookies();

        for (Cookie cookie : allCookies) {
            if (cookie.getName().equals(cookieName) && cookie.getDomain().equals(domain)) {
                return cookie.getValue();
            }
        }
        return null;
    }

    /**
     * 保存 Cookie到json文件
     */
    public static void saveCookieToJson(Map<String, String> cookies) {
        Gson gson = new Gson();
        try (FileWriter writer = new FileWriter("cookies.json")){
            writer.write(gson.toJson(cookies));
            log.info("Cookie 已成功保存至:" + new File("cookies.json").getAbsolutePath());
        } catch (IOException e) {
            log.error("保存Cookie失败", e);
        }
    }


    /**
     * 根据Cookie名称和domain获取Value
     *
     * @param driver 浏览器驱动
     * @param cookieName Cookie名称
     * @param domain Cookie域
     * @return Cookie值
     */
    public static String getCookieValueByNameAndDomain(WebDriver driver, String cookieName, String domain) {
        Cookie cookie = driver.manage().getCookieNamed(cookieName);
        return cookie != null && cookie.getDomain().equals(domain) ? cookie.getValue() : null;
    }

}
