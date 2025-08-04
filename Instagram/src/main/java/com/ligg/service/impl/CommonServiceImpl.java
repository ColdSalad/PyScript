package com.ligg.service.impl;

import com.ligg.service.CommonService;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @Author Ligg
 * @Time 2025/8/1
 **/
public class CommonServiceImpl implements CommonService {

    private static final Logger log = LoggerFactory.getLogger(CommonServiceImpl.class);

    @Override
    public void EnableLeave(WebDriver driver) {
        try {
            WebElement focusButton = driver.findElement(By.cssSelector("div > button > div > div"));
            Thread.sleep(3000);
            focusButton.click();
        } catch (InterruptedException e) {
            log.info("可能已经关注，直接跳过");
        }
    }

    /**
     * 点赞
     */
    @Override
    public void EnableLike(WebDriver driver, String url, String Count) {
        int maxLikes = Integer.parseInt(Count);
        try {
            //打开弹窗
            for (int i = 1; i <= maxLikes; i++) {
                Thread.sleep(4000);
                String xpath = "//div[@class='x1n2onr6']/div/div/div/div[1]/div[" + i + "]/a";
                if (i > 3) {
                    xpath = "//div[@class='x1n2onr6']/div/div/div/div[" + 1 + 1 + "]/div[" + i + "]/a";
                }
                WebElement element = driver.findElement(By.xpath(xpath));
                Thread.sleep(3000);
                element.click();
                Thread.sleep(3000);
                WebElement likeButton = driver.findElement(By.xpath("//div[@role='dialog']//div/section[1]/span[1]"));
                likeButton.click();//点一次可能出现无法现在成功的问题
                likeButton.click();
                Thread.sleep(1000);
                driver.get(url);
            }

        } catch (Exception e) {
            log.error(e.getMessage());
            log.info("可能没有发布帖子", e);
        }
    }

    /**
     * 评论
     */
    @Override
    public void comments(WebDriver driver, String url, String Count, String msgText) {
        int max = Integer.parseInt(Count);
        try {
            //打开弹窗
            for (int i = 1; i <= max; i++) {
                Thread.sleep(4000);
                String xpath = "//div[@class='x1n2onr6']/div/div/div/div[1]/div[" + i + "]/a";
                if (i > 3) {
                    xpath = "//div[@class='x1n2onr6']/div/div/div/div[" + 1 + 1 + "]/div[" + i + "]/a";
                }
                WebElement element = driver.findElement(By.xpath(xpath));
                Thread.sleep(3000);
                element.click();
                Thread.sleep(3000);

                try {
                    //点击评论图标
                    WebElement likeButton = driver.findElement(By.xpath("//div[@role='dialog']//div/section[1]/span[2]"));
                    likeButton.click();//点一次可能出现无法现在成功的问题
                    likeButton.click();
                    Thread.sleep(1000);
                } catch (Exception e) {
                    log.info("不用管直接跳过");
                }

                //获取评论框
                WebElement commentBox = driver.findElement(By.xpath("//div[@role='dialog']//section[3]//form//textarea"));
                commentBox.clear();//清空
                Thread.sleep(1000);
                //输入内容
                commentBox.sendKeys(msgText);
                Thread.sleep(1000);

                //发送内容
                WebElement sendButton = driver.findElement(By.xpath("//div[@role='dialog']//section[3]//form/div/div[2]"));
                sendButton.click();
                Thread.sleep(3000);
                driver.get(url);
            }

        } catch (Exception e) {
            log.error(e.getMessage());
            log.info("可能没有发布帖子", e);
        }
    }
}
