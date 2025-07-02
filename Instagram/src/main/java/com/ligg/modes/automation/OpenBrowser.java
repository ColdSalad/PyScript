package com.ligg.modes.automation;

import javafx.application.Platform;
import javafx.scene.control.Button;
import org.openqa.selenium.By;
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
                WebElement usernameInput = driver.findElement(By.cssSelector("#loginForm > div.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(1) > div > label > input"));
                WebElement passwordInput = driver.findElement(By.cssSelector("#loginForm > div.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(2) > div > label > input"));
                usernameInput.sendKeys(username);
                passwordInput.sendKeys(password);

                //点击登录按钮
                WebElement webLoginButton = driver.findElement(By.cssSelector("#loginForm > div.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1xmf6yo.x1e56ztr.x11hdunq.x11gldyt.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > button"));
                webLoginButton.click();
                Platform.runLater(() -> {
                    loginButton.setDisable(false);
                    loginButton.setText("登录");
                });

                Thread.sleep(5000);
                if(!driver.getCurrentUrl().equals("https://www.instagram.com/?next=%2F")){
                    driver.get("https://www.instagram.com/?next=%2F");
                }
            } catch (InterruptedException e) {
                log.error("网页加载超时");
            }
        }).start();
    }

    /**
     * 点赞方法
     */
    public void like() {
        try {
            // 打开目标网址
            driver.get("https://www.instagram.com/?next=%2F");
            // 等待页面加载
            Thread.sleep(5000);
            log.info("成功打开目标网址");
        } catch (InterruptedException e) {
            log.error("点赞过程中发生异常：{}", e.getMessage());
        }
    }

}
