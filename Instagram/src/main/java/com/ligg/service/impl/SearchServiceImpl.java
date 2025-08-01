package com.ligg.service.impl;

import com.ligg.service.SearchService;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @Author Ligg
 * @Time 2025/8/1
 **/
public class SearchServiceImpl implements SearchService {

    private static final Logger log = LoggerFactory.getLogger(SearchServiceImpl.class);

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
    public void EnableLike(WebDriver driver,String url, String Count) {
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
}
