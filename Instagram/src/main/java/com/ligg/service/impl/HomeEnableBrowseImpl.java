package com.ligg.service.impl;

import com.ligg.pojo.Data;
import com.ligg.service.HomeEnableBrowse;
import com.ligg.util.ClickableParent;
import javafx.scene.control.Button;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.Random;

/**
 * @Author Ligg
 * @Time 2025/8/1
 **/
public class HomeEnableBrowseImpl implements HomeEnableBrowse {

    private static final Logger log = LoggerFactory.getLogger(HomeEnableBrowseImpl.class);

    /**
     * 点赞
     */
    @Override
    public void like(WebDriver driver, JavascriptExecutor js, Button loginButton) throws InterruptedException {
        WebElement likeButtons = driver.findElement(By.cssSelector("section  section  span >  .x1ypdohk  > div >div > span"));

        // 检查元素是否可见且可点击
        if (likeButtons.isDisplayed()) {
            // 滚动到元素位置
            js.executeScript("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", likeButtons);
            Thread.sleep(1000); // 等待滚动完成

            // 查找可点击的父元素
            WebElement clickableParent = ClickableParent.findClickableParent(likeButtons, js);

            if (clickableParent != null) {
                // 使用JavaScript点击，避免元素被遮挡的问题
                js.executeScript("arguments[0].click();", clickableParent);
                Thread.sleep(2000);
            }
        }
    }

    /**
     * 评论方法
     */
    @Override
    public void comment(WebDriver driver, Button loginButton, Data data) throws InterruptedException {

        JavascriptExecutor js = (JavascriptExecutor) driver;
        int commentedCount = 0; // 已评论的帖子数

        WebElement commentButtons = driver.findElement(By.xpath("//section//section/div/span[2]/div/div"));

        WebElement clickableParent = ClickableParent.findClickableParent(commentButtons, js);


        js.executeScript("arguments[0].click();", clickableParent);
        Thread.sleep(2000); // 等待弹窗加载

        // 点击弹窗中的评论按钮
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
            // 等待弹窗出现
            // 在弹窗中查找评论图标
            WebElement commentIconInPopup = driver.findElement(By.cssSelector("div[role='dialog'] div[tabindex='-1'] section:nth-of-type(1) > span:nth-of-type(2) > div >div"));
            WebElement clickableCommentButton = ClickableParent.findClickableParent(commentIconInPopup, js);
            if (clickableCommentButton != null) {
                js.executeScript("arguments[0].click();", clickableCommentButton);
                Thread.sleep(1000); // 等待输入框出现
            }
        } catch (Exception e) {
            log.info("在弹窗中未找到或无法点击评论图标，将直接尝试输入评论。");
            // 即使找不到图标，也继续尝试，因为UI可能已经允许直接输入
        }
        submitComment(driver, commentedCount, data);
        Thread.sleep(3000);
        closeCommentBox(js);
        log.info("评论完成，共评论{}个帖子", commentedCount);
    }


    /**
     * 提交评论
     */
    @Override
    public boolean submitComment(WebDriver driver, int commentedCount, Data data) {
        String[] comments = data.getSendData().getLeaveText().split("\\n\\n\\n");

        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
            Thread.sleep(2000);
            WebElement commentInput = wait.until(ExpectedConditions.elementToBeClickable(
                    By.cssSelector("div[role='dialog'] form textarea")
            ));
            String commentText = comments[new Random().nextInt(comments.length)];
            Thread.sleep(2000);
            // 先清空再输入（防止残留内容）
            commentInput.click();
            Thread.sleep(300);
            WebElement commentInput2 = wait.until(ExpectedConditions.elementToBeClickable(
                    By.cssSelector("div[role='dialog'] form textarea")
            ));
            commentInput2.sendKeys(commentText);
            Thread.sleep(1000);

            //发送评论
            String postSelector = "div[role='dialog'] form .x13fj5qh > div";
            WebElement sendButton = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(postSelector)));

            sendButton.click();
            log.info("成功评论第{}个帖子: {}", commentedCount + 1, commentText);
            Thread.sleep(3000);
            return true;

        } catch (Exception e) {
            log.warn("评论输入框操作失败: {}", e.getMessage());
            return false;
        }
    }

    /**
     * 关闭评论弹窗
     */
    @Override
    public void closeCommentBox(JavascriptExecutor js) {
        //关闭弹窗
        String closeButtonSelector = "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.xo2ifbc.x10l6tqk.x1eu8d0j.x1vjfegm > div > div";
        js.executeScript("document.querySelector('" + closeButtonSelector + "').click();");
        log.info("关闭评论弹窗");
    }
}
