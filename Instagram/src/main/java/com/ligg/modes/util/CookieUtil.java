package com.ligg.modes.util;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.ligg.modes.automation.OpenBrowser;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Type;
import java.util.HashMap;
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

    /**
     * 从JSON文件读取Cookie
     *
     * @param filePath JSON文件路径，如果为null则使用默认路径"cookies.json"
     * @return Cookie映射表，如果读取失败返回空Map
     */
    public static Map<String, String> loadCookieFromJson(String filePath) {
        if (filePath == null) {
            filePath = "cookies.json";
        }
        
        File file = new File(filePath);
        if (!file.exists()) {
            log.warn("Cookie文件不存在: {}", file.getAbsolutePath());
            return new HashMap<>();
        }
        
        Gson gson = new Gson();
        try (FileReader reader = new FileReader(file)) {
            Type type = new TypeToken<Map<String, String>>(){}.getType();
            Map<String, String> cookies = gson.fromJson(reader, type);
            log.info("成功从文件读取Cookie: {}", file.getAbsolutePath());
            return cookies != null ? cookies : new HashMap<>();
        } catch (IOException e) {
            log.error("读取Cookie文件失败: {}", e.getMessage());
            return new HashMap<>();
        }
    }

    /**
     * 从默认JSON文件读取Cookie
     *
     * @return Cookie映射表
     */
    public static Map<String, String> loadCookieFromJson() {
        return loadCookieFromJson(null);
    }

    /**
     * 将Cookie映射表应用到WebDriver
     *
     * @param driver WebDriver实例
     * @param cookies Cookie映射表
     */
    public static void applyCookiesToDriver(WebDriver driver, Map<String, String> cookies) {
        if (cookies == null || cookies.isEmpty()) {
            log.warn("Cookie映射表为空，跳过应用");
            return;
        }
        
        for (Map.Entry<String, String> entry : cookies.entrySet()) {
            String name = entry.getKey();
            String value = entry.getValue();
            if (name != null && value != null) {
                try {
                    driver.manage().addCookie(new Cookie(name, value));
                    log.debug("成功添加Cookie: {} = {}", name, value);
                } catch (Exception e) {
                    log.warn("添加Cookie失败: {} = {}, 错误: {}", name, value, e.getMessage());
                }
            }
        }
        log.info("成功应用{}个Cookie到浏览器", cookies.size());
    }

}
