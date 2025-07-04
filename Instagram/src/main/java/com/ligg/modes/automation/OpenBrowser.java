package com.ligg.modes.automation;

import javafx.application.Platform;
import javafx.scene.control.Button;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
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
                    driver.get("https://www.instagram.com/?next=%2F");
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
        try {
            // 等待页面加载
            Thread.sleep(3000);
            log.info("开始点赞...");

            // 使用JavaScript查找最近的可点击父按钮区域并点击
            WebElement svgElement = driver.findElement(By.cssSelector("svg[aria-label='赞']"));
            JavascriptExecutor jsExecutor = (JavascriptExecutor) driver;

            // 查找最近的可点击父元素(button 或具有onclick属性的元素)
            String script = "var element = arguments[0];" +
                    "while (element.parentNode) {" +
                    "  element = element.parentNode;" +
                    "  if (element.tagName.toLowerCase() === 'button' || element.hasAttribute('onclick')) {" +
                    "    return element;" +
                    "  }" +
                    "}" +
                    "return null;";

            WebElement clickableParent = (WebElement) jsExecutor.executeScript(script, svgElement);

            if (clickableParent != null) {
                jsExecutor.executeScript("arguments[0].click();", clickableParent);
                log.info("成功点击点赞按钮");
            } else {
                log.warn("未找到可点击的父元素");
            }

        } catch (InterruptedException e) {
            log.error("点赞过程中发生异常：{}", e.getMessage());
        }
    }

}
