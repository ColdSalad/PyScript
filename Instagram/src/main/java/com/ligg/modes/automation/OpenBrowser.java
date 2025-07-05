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
     * 点赞方法
     */
    public void like(WebDriver driver) {
        // 等待页面加载
        log.info("开始点赞...");
        WebDriverWait wait = new WebDriverWait(driver, java.time.Duration.ofSeconds(10));
        var likeButton  = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("html > body > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > section > main > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div:nth-of-type(1) > div > article:nth-of-type(1) > div > div:nth-of-type(3) > div > div > section:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1) > div > div")));
        likeButton.click();
        likeButton.click();
        log.info("点赞结束");
    }

}
