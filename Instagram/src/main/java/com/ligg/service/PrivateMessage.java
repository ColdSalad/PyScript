package com.ligg.service;

import org.openqa.selenium.WebDriver;

/**
 * @Author Ligg
 * @Time 2025/7/25
 * <p>
 * 私信接口
 **/
public interface PrivateMessage {

    /**
     * 发送私信
     */
    void sendPrivateMessage(
            WebDriver driver, String username, String msgText
    ) throws InterruptedException;

    /**
     * 关注
     */
    void follow(WebDriver driver);
}
