package com.ligg.service.impl;

import com.ligg.pojo.Data;
import com.ligg.service.HomeEnableBrowse;
import com.ligg.util.ClickableParent;
import javafx.application.Platform;
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
import java.util.List;
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
    public void like(WebDriver driver, int maxLikes, JavascriptExecutor js, Button loginButton) throws InterruptedException {
        for (int i = 0; i < maxLikes; i++) {
            List<WebElement> likeButtons = driver.findElements(By.cssSelector("svg[aria-label='赞']"));

            if (!likeButtons.isEmpty()) {
                for (WebElement svgElement : likeButtons) {
                    // 检查元素是否可见且可点击
                    if (svgElement.isDisplayed()) {
                        // 滚动到元素位置
                        js.executeScript("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", svgElement);
                        Thread.sleep(1000); // 等待滚动完成

                        // 查找可点击的父元素（通常是button）
                        WebElement clickableParent = ClickableParent.findClickableParent(svgElement, js);

                        if (clickableParent != null) {
                            // 使用JavaScript点击，避免元素被遮挡的问题
                            js.executeScript("arguments[0].click();", clickableParent);
                            log.info("成功点赞第{}个帖子", i);
                            Thread.sleep(2000);
                            break;
                        }
                    }
                }
            }

            // 如果还没达到目标数量，继续滚动页面
            log.info("滚动页面加载更多帖子...");
            js.executeScript("window.scrollBy(0, 800);"); // 向下滚动800像素
            Thread.sleep(3000); // 等待页面加载
        }

        log.info("点赞完成");
    }

    /**
     * 评论方法
     */
    @Override
    public void comment(WebDriver driver, Button loginButton, Data data) {
        log.info("开始自动评论...");
        Platform.runLater(() -> loginButton.setText("评论中..."));

        JavascriptExecutor js = (JavascriptExecutor) driver;
        int commentedCount = 0; // 已评论的帖子数
        int maxComments = Integer.parseInt(data.getSendData().getConfigDatas().getHome_HomeBrowseCount());

        try {
            while (commentedCount < maxComments) {
                List<WebElement> commentButtons = driver.findElements(By.cssSelector("svg[aria-label='评论']"));

                for (WebElement svgElement : commentButtons) {
                    if (commentOnPost(svgElement, driver, js, commentedCount, data)) {
                        commentedCount++;
                        if (commentedCount >= maxComments) {
                            break;
                        }
                    }
                }

                if (commentedCount < maxComments) {
                    log.info("滚动页面加载更多帖子...");
                    js.executeScript("window.scrollBy(0, 800);");
                    Thread.sleep(3000);
                }
            }

            log.info("评论完成，共评论{}个帖子", commentedCount);
            updateButtonState(loginButton, "完成");

        } catch (InterruptedException e) {
            log.error("评论过程中发生异常：{}", e.getMessage());
            updateButtonState(loginButton, "评论失败");
        }
    }

    /**
     * 评论单个帖子
     */
    @Override
    public boolean commentOnPost(WebElement svgElement, WebDriver driver, JavascriptExecutor js, int commentedCount, Data data) {
        try {
            if (!svgElement.isDisplayed()) {
                return false;
            }

            js.executeScript("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", svgElement);
            Thread.sleep(2000);

            WebElement clickableParent = ClickableParent.findClickableParent(svgElement, js);
            if (clickableParent == null) {
                return false;
            }

            js.executeScript("arguments[0].click();", clickableParent);
            Thread.sleep(2000); // 等待弹窗加载

            // 点击弹窗中的评论按钮
            try {
                WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
                // 等待弹窗出现
                WebElement commentModal = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("div[role='dialog']")));
                // 在弹窗中查找评论图标
                WebElement commentIconInPopup = commentModal.findElement(By.cssSelector("svg[aria-label='评论']"));
                WebElement clickableCommentButton = ClickableParent.findClickableParent(commentIconInPopup, js);
                if (clickableCommentButton != null) {
                    js.executeScript("arguments[0].click();", clickableCommentButton);
                    Thread.sleep(1000); // 等待输入框出现
                }
            } catch (Exception e) {
                log.warn("在弹窗中未找到或无法点击评论图标，将直接尝试输入评论。");
                // 即使找不到图标，也继续尝试，因为UI可能已经允许直接输入
            }
            boolean success = submitComment(driver, commentedCount, data);
            closeCommentBox(js);

            return success;
        } catch (Exception e) {
            log.warn("评论单个帖子时出现异常: {}", e.getMessage());
            return false;
        }
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
                    By.cssSelector("div[role='dialog'] textarea[placeholder*='添加评论']")
            ));
            String commentText = comments[new Random().nextInt(comments.length)];
            Thread.sleep(2000);
            // 先清空再输入（防止残留内容）
            commentInput.click();
            Thread.sleep(300);
            commentInput.sendKeys(commentText);
            Thread.sleep(1000);

            //发送评论
            String postSelector = "//div[@role='dialog']//div[text()='发布']";
            WebElement sendButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath(postSelector)));

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

    /**
     * 更新按钮状态
     */
    private void updateButtonState(Button button, String text) {
        Platform.runLater(() -> {
            button.setText(text);
            button.setDisable(false);
        });
    }
}
