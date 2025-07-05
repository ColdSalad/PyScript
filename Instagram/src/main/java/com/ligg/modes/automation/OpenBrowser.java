package com.ligg.modes.automation;

import javafx.application.Platform;
import javafx.scene.control.Button;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;


/**
 * @Author Ligg
 * @Time 2025/7/2
 **/
public class OpenBrowser {

    private static final Logger log = LoggerFactory.getLogger(OpenBrowser.class);
    private WebDriver driver;


    //打开浏览器
    public void Login(String username, String password, Button loginButton) {
        //创建一个线程用于打开浏览器，避免GUI阻塞主线程
        new Thread(() -> {
            try {
                //默认启动Edge浏览器
                log.info("尝试启动Edge浏览器...");
                driver = new EdgeDriver();
            } catch (Exception e) {
                log.info("Edge启动失败，尝试启动Chrome浏览器...");
                driver = new ChromeDriver();
            }
            driver.get("https://www.instagram.com/");
            // 自动登录逻辑
            try {
                Thread.sleep(5000);
                //选中账号、密码输入框
                WebElement usernameInput = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[1]/div[1]/div/label/input"));
                WebElement passwordInput = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[1]/div[2]/div/label/input"));
                usernameInput.sendKeys(username);
                passwordInput.sendKeys(password);

                //点击登录按钮
                WebElement webLoginButton = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[1]/div[3]/button"));
                webLoginButton.click();


                Thread.sleep(5000);
                if (!driver.getCurrentUrl().equals("https://www.instagram.com/?next=%2F")) {
                    WebDriverWait wait = new WebDriverWait(driver, java.time.Duration.ofSeconds(10));
                    var homeButton = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("body > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div > div > div > div > div > div:nth-of-type(1) > div > span > div > a > div")));
                    homeButton.click();

                    //点赞
                    like(driver, loginButton);
                }
            } catch (InterruptedException e) {
                log.error("网页加载超时");
            }
        }).start();
    }

    /**
     * 点赞方法 - 自动滚动页面并对多个帖子点赞
     */
    public void like(WebDriver driver, Button loginButton) {
        log.info("开始自动点赞...");
        Platform.runLater(() -> {
            loginButton.setText("点赞中...");
        });
        new WebDriverWait(driver, java.time.Duration.ofSeconds(10));
        JavascriptExecutor js = (JavascriptExecutor) driver;

        int likedCount = 0; // 已点赞的帖子数
        int maxLikes = 3; // 最多点赞10个帖子
        int scrollAttempts = 0; // 滚动次数
        int maxScrollAttempts = 10; // 最多滚动20次

        try {
            while (likedCount < maxLikes && scrollAttempts < maxScrollAttempts) {
                // 查找所有未点赞的按钮（通过aria-label="赞"识别）
                List<WebElement> likeButtons = driver.findElements(By.cssSelector("svg[aria-label='赞']"));

                if (!likeButtons.isEmpty()) {
                    for (WebElement svgElement : likeButtons) {
                        try {
                            // 检查元素是否可见且可点击
                            if (svgElement.isDisplayed()) {
                                // 滚动到元素位置
                                js.executeScript("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", svgElement);
                                Thread.sleep(1000); // 等待滚动完成

                                // 查找可点击的父元素（通常是button）
                                WebElement clickableParent = findClickableParent(svgElement, js);

                                if (clickableParent != null) {
                                    // 使用JavaScript点击，避免元素被遮挡的问题
                                    js.executeScript("arguments[0].click();", clickableParent);
                                    likedCount++;
                                    log.info("成功点赞第{}个帖子", likedCount);
                                    Thread.sleep(2000); // 点赞后等待2秒

                                    if (likedCount >= maxLikes) {
                                        break;
                                    }
                                }
                            }
                        } catch (Exception e) {
                            log.warn("点赞单个帖子时出现异常: {}", e.getMessage());
                        }
                    }
                }

                // 如果还没达到目标数量，继续滚动页面
                if (likedCount < maxLikes) {
                    log.info("滚动页面加载更多帖子...");
                    js.executeScript("window.scrollBy(0, 800);"); // 向下滚动800像素
                    Thread.sleep(3000); // 等待页面加载
                    scrollAttempts++;
                }
            }

            log.info("点赞完成，共点赞{}个帖子", likedCount);
            /*
             开始评论
             */
            comment(driver, loginButton);
        } catch (InterruptedException e) {
            log.error("点赞过程中发生异常：{}", e.getMessage());
        }
    }

    /**
     * 查找SVG元素的可点击父元素
     */
    private WebElement findClickableParent(WebElement svgElement, JavascriptExecutor js) {
        String script = "var element = arguments[0];" +
                "while (element.parentNode) {" +
                "  element = element.parentNode;" +
                "  if (element.tagName.toLowerCase() === 'button' || element.hasAttribute('onclick') || element.getAttribute('role') === 'button') {" +
                "    return element;" +
                "  }" +
                "}" +
                "return null;";

        return (WebElement) js.executeScript(script, svgElement);
    }

    /**
     * 评论方法 - 自动滚动页面并对多个帖子进行评论
     */
    public void comment(WebDriver driver, Button loginButton) {
        log.info("开始自动评论...");
        Platform.runLater(() -> loginButton.setText("评论中..."));

        WebDriverWait wait = new WebDriverWait(driver, java.time.Duration.ofSeconds(10));
        JavascriptExecutor js = (JavascriptExecutor) driver;

        int commentedCount = 0;
        int maxComments = 5; // 最多评论5个帖子
        int scrollAttempts = 0;
        int maxScrollAttempts = 15; // 最多滚动15次

        // 预定义的评论内容
        String[] comments = {
            "很棒的分享！👍",
            "太有趣了！😊",
            "喜欢这个内容！❤️",
            "非常不错！✨",
            "很有意思！😄"
        };

        try {
            while (commentedCount < maxComments && scrollAttempts < maxScrollAttempts) {
                // 查找所有评论按钮（通过aria-label="评论"识别）
                List<WebElement> commentButtons = driver.findElements(By.cssSelector("svg[aria-label='评论']"));

                if (!commentButtons.isEmpty()) {
                    for (WebElement svgElement : commentButtons) {
                        try {
                            // 检查元素是否可见
                            if (svgElement.isDisplayed()) {
                                // 滚动到元素位置
                                js.executeScript("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", svgElement);
                                Thread.sleep(1000);

                                // 查找可点击的父元素
                                WebElement clickableParent = findClickableParent(svgElement, js);

                                if (clickableParent != null) {
                                    // 点击评论按钮
                                    js.executeScript("arguments[0].click();", clickableParent);
                                    Thread.sleep(2000); // 等待评论框加载

                                    try {
                                        // 评论弹窗中点击评论按钮
                                        WebElement commentSvg = wait.until(ExpectedConditions.elementToBeClickable(
                                                By.cssSelector("svg[aria-label='评论']")
                                        ));
                                        commentSvg.click();

                                        //找到评论输入框
                                        WebElement commentInput = wait.until(ExpectedConditions.elementToBeClickable(
                                            By.cssSelector("textarea[aria-label='添加评论...'], textarea[placeholder='添加评论...']")
                                        ));

                                        // 输入评论内容
                                        String commentText = comments[commentedCount % comments.length];
                                        commentInput.clear();
                                        commentInput.sendKeys(commentText);
                                        Thread.sleep(1000);

                                        // 查找并点击发布按钮
                                        try {
                                            WebElement postButton = driver.findElement(By.xpath("//button[contains(text(),'发布') or contains(text(),'Post')]"));
                                            if (postButton.isEnabled()) {
                                                postButton.click();
                                                commentedCount++;
                                                log.info("成功评论第{}个帖子: {}", commentedCount, commentText);
                                                Thread.sleep(3000); // 评论后等待3秒
                                            }
                                        } catch (Exception e) {
                                            log.warn("未找到发布按钮，尝试按Enter键发布评论");
                                            commentInput.sendKeys("\n"); // 按Enter键发布
                                            commentedCount++;
                                            log.info("成功评论第{}个帖子: {}", commentedCount, commentText);
                                            Thread.sleep(3000);
                                        }

                                        // 尝试关闭评论弹窗
                                        try {
                                            WebElement closeButton = driver.findElement(By.cssSelector("svg[aria-label='关闭'], button[aria-label='关闭']"));
                                            js.executeScript("arguments[0].click();", closeButton);
                                            Thread.sleep(1000);
                                        } catch (Exception e) {
                                            log.debug("未找到关闭按钮，可能评论框已自动关闭");
                                            // 按ESC键尝试关闭
                                            js.executeScript("document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}));");
                                        }

                                        if (commentedCount >= maxComments) {
                                            break;
                                        }

                                    } catch (Exception e) {
                                        log.warn("评论输入框操作失败: {}", e.getMessage());
                                        // 尝试关闭可能打开的弹窗
                                        try {
                                            js.executeScript("document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}));");
                                        } catch (Exception ignored) {}
                                    }
                                }
                            }
                        } catch (Exception e) {
                            log.warn("评论单个帖子时出现异常: {}", e.getMessage());
                        }
                    }
                }

                // 如果还没达到目标数量，继续滚动页面
                if (commentedCount < maxComments) {
                    log.info("滚动页面加载更多帖子...");
                    js.executeScript("window.scrollBy(0, 800);");
                    Thread.sleep(3000);
                    scrollAttempts++;
                }
            }

            log.info("评论完成，共评论{}个帖子", commentedCount);
            Platform.runLater(() -> {
                loginButton.setText("完成");
                loginButton.setDisable(false);
            });

        } catch (InterruptedException e) {
            log.error("评论过程中发生异常：{}", e.getMessage());
            Platform.runLater(() -> {
                loginButton.setText("评论失败");
                loginButton.setDisable(false);
            });
        }
    }

}
