package com.ligg.service;

import org.openqa.selenium.WebDriver;

/**
 * @Author Ligg
 * @Time 2025/8/1
 **/
public interface CommonService {

    /**
     * 关注
     */
    void EnableLeave(WebDriver driver);

    /**
     * 点赞
     */
    void EnableLike(WebDriver driver,String url,String Count);

    /**
     * 评论
     */
    void comments(WebDriver driver,String url,String Count,String msgText);
}
