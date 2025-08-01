package com.ligg.service;

import com.ligg.pojo.Data;
import javafx.scene.control.Button;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

/**
 * @Author Ligg
 * @Time 2025/8/1
 **/
public interface HomeEnableBrowse {

    /**
     * 点赞
     */
    void like(WebDriver driver, JavascriptExecutor js, Button loginButton) throws InterruptedException;

    /**
     * 评论
     */
    void comment(WebDriver driver, Button loginButton, Data data) throws InterruptedException;

    /**
     * 提交评论
     */
    boolean submitComment(WebDriver driver, int commentedCount, Data data);

    /**
     * 关闭评论弹窗
     */
    void closeCommentBox(JavascriptExecutor js);
}
