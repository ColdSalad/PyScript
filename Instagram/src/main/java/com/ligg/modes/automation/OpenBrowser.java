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
                Platform.runLater(() -> {
                    loginButton.setDisable(false);
                    loginButton.setText("登录");
                });

                Thread.sleep(5000);
                if (!driver.getCurrentUrl().equals("https://www.instagram.com/?next=%2F")) {
                    WebDriverWait wait = new WebDriverWait(driver, java.time.Duration.ofSeconds(10));
                    var homeButton = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("body > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div > div > div > div > div > div:nth-of-type(1) > div > span > div > a > div")));
                    homeButton.click();
                    //点赞
                    like(driver);
                }
            } catch (InterruptedException e) {
                log.error("网页加载超时");
            }
        }).start();
    }

    /**
     * 点赞方法 - 自动滚动页面并对多个帖子点赞
     */
    public void like(WebDriver driver) {
        log.info("开始自动点赞...");
        WebDriverWait wait = new WebDriverWait(driver, java.time.Duration.ofSeconds(10));
        JavascriptExecutor js = (JavascriptExecutor) driver;
        
        int likedCount = 0;
        int maxLikes = 10; // 最多点赞10个帖子
        int scrollAttempts = 0;
        int maxScrollAttempts = 20; // 最多滚动20次
        
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

}
