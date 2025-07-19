package com.ligg.modes.automation;

import com.ligg.modes.http_request.HttpRequest;
import com.ligg.modes.pojo.Data;
import com.ligg.modes.pojo.ProfilePage;
import javafx.application.Platform;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import org.jetbrains.annotations.NotNull;
import org.openqa.selenium.*;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.*;


/**
 * @Author Ligg
 * @Time 2025/7/2
 **/
public class OpenBrowser {

    private static final Logger log = LoggerFactory.getLogger(OpenBrowser.class);
    private WebDriver driver;

    private static final HttpRequest httpRequest = new HttpRequest();
    private String adminUsername;

    private Data data = null;

    //打开浏览器
    public void Login(String username, String password, Button loginButton, String adminUsername) {
        this.adminUsername = adminUsername;
        //创建一个线程用于打开浏览器，避免GUI阻塞主线程
        new Thread(() -> {
            try {
                log.info("尝试启动Chrome浏览器...");
                EdgeOptions edgeOptions = new EdgeOptions();
                edgeOptions.addArguments("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36");
                driver = new EdgeDriver(edgeOptions);

            } catch (Exception e) {
                //默认启动Edge浏览器
                log.info("Chrome启动失败，尝试启动Edge浏览器...");
                ChromeOptions chromeOptions = new ChromeOptions();
                chromeOptions.addArguments("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36");
                driver = new ChromeDriver(chromeOptions);

            }
            driver.get("https://www.instagram.com/?next=%2F");
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

                WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
                try {
                    // 尝试查找错误消息，如果找到说明登录失败
                    WebElement error = wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[normalize-space()='很抱歉，密码有误，请检查密码。']")));
                    if (error.isDisplayed()) {
                        Platform.runLater(() -> {
                            Alert alert = new Alert(Alert.AlertType.WARNING);
                            alert.setTitle("提示");
                            alert.setHeaderText(error.getText());
                            alert.showAndWait();
                        });
                        Platform.runLater(() -> {
                            loginButton.setText("重新登录");
                            loginButton.setDisable(false);
                        });
                        return;
                    }
                } catch (org.openqa.selenium.TimeoutException e) {
                    // 没有找到错误消息，说明登录成功，继续执行
                    log.info("登录成功，未发现错误消息");
                }
//                    //获取登录后的Cookie
//                    String datrCookie = CookieUtil.getCookieByNameAndDomain(driver, "datr", "www.instagram.com");
//                    String ig_didCookie = CookieUtil.getCookieByNameAndDomain(driver, "ig_did", "www.instagram.com");
//                    String midCookie = CookieUtil.getCookieByNameAndDomain(driver, "mid", ".instagram.com");
//                    String ps_lCookie = CookieUtil.getCookieByNameAndDomain(driver, "ps_l", "www.instagram.com");
//                    String ps_nCookie = CookieUtil.getCookieByNameAndDomain(driver, "ps_n", "www.instagram.com");
//                    String ig_nrcbCookie = CookieUtil.getCookieByNameAndDomain(driver, "ig_nrcb", "www.instagram.com");
//                    String csrftokenCookie = CookieUtil.getCookieByNameAndDomain(driver, "csrftoken", ".instagram.com");
//                    String dprCookie = CookieUtil.getCookieByNameAndDomain(driver, "dpr", "www.instagram.com");
//                    String localeCookie = CookieUtil.getCookieByNameAndDomain(driver, "locale", "www.instagram.com");
//                    String ig_langCookie = CookieUtil.getCookieByNameAndDomain(driver, "ig_lang", "www.instagram.com");
//                    String sessionidCookie = CookieUtil.getCookieByNameAndDomain(driver, "sessionid", "www.instagram.com");
//                    String ds_user_idCookie = CookieUtil.getCookieByNameAndDomain(driver, "ds_user_id", ".instagram.com");
//                    String wdCookie = CookieUtil.getCookieByNameAndDomain(driver, "wd", "www.instagram.com");
//                    String rurCookie = CookieUtil.getCookieByNameAndDomain(driver, "rur", "www.instagram.com");
//
//                    Thread.sleep(3000);
//                    HashMap<String, String> cookieMap = new HashMap<>();
//                    cookieMap.put("datr", datrCookie);
//                    cookieMap.put("ig_did", ig_didCookie);
//                    cookieMap.put("mid", midCookie);
//                    cookieMap.put("ps_l", ps_lCookie);
//                    cookieMap.put("ps_n", ps_nCookie);
//                    cookieMap.put("ig_nrcb", ig_nrcbCookie);
//                    cookieMap.put("csrftoken", csrftokenCookie);
//                    cookieMap.put("dpr", dprCookie);
//                    cookieMap.put("locale", localeCookie);
//                    cookieMap.put("ig_lang", ig_langCookie);
//                    cookieMap.put("sessionid", sessionidCookie);
//                    cookieMap.put("ds_user_id", ds_user_idCookie);
//                    cookieMap.put("wd", wdCookie);
//                    cookieMap.put("rur", rurCookie);

//                    保存Cookie
//                    CookieUtil.saveCookieToJson(cookieMap);
                Thread.sleep(5000);
                var homeButton = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("body > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div > div > div > div > div > div:nth-of-type(1) > div > span > div > a > div")));
                homeButton.click();
                //点赞
                like(driver, loginButton);
            } catch (InterruptedException e) {
                log.error("网页加载超时");
            }
        }).start();
    }

    /**
     * 点赞方法 - 自动滚动页面并对多个帖子点赞
     */
    public void like(WebDriver driver, Button loginButton) {
        Data data = httpRequest.getData(adminUsername);
        this.data = data;
        log.info("开始自动点赞...");
        Platform.runLater(() -> loginButton.setText("点赞中..."));
        new WebDriverWait(driver, Duration.ofSeconds(10));
        JavascriptExecutor js = (JavascriptExecutor) driver;

        Data.ConfigDatas configDatas = data.getSendData().getConfigDatas();
        String Home_IsEnableLike = configDatas.getHome_IsEnableLike();
        int likedCount = 0; // 已点赞的帖子数
//        int maxLikes = Integer.parseInt(configDatas.getHome_HomeBrowseCount()); // 最多点赞10个帖子
        int maxLikes = 1;
        int scrollAttempts = 0; // 滚动次数
        int maxScrollAttempts = 10; // 最多滚动次
        String HuDong_IsEnableMsg = configDatas.getHuDong_IsEnableMsg(); //是否私信
        String Home_IsEnableLeave = configDatas.getHome_IsEnableLeave(); //是评论
        //点赞
        if (Objects.equals(Home_IsEnableLike, "true")) {
            try {
                while (likedCount < maxLikes && scrollAttempts < maxScrollAttempts) {
                    // 查找所有未点赞的按钮（通过aria-label="赞"识别）
                    List<WebElement> likeButtons = driver.findElements(By.cssSelector("svg[aria-label='赞'],svg[aria-label='Like']"));

                    if (!likeButtons.isEmpty()) {
                        for (WebElement svgElement : likeButtons) {
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
                                    break;
                                }
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
        if (Objects.equals(Home_IsEnableLeave, "true")) {
            //评论
            comment(driver, loginButton);
        }

        //私信
        if (Objects.equals(HuDong_IsEnableMsg, "true")) {
            goToProfilePage(driver, js);
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
     * 评论方法
     */
    public void comment(WebDriver driver, Button loginButton) {
        log.info("开始自动评论...");
        Platform.runLater(() -> loginButton.setText("评论中..."));
        Data.ConfigDatas configDatas = data.getSendData().getConfigDatas();
        JavascriptExecutor js = (JavascriptExecutor) driver;
        int commentedCount = 0; // 已评论的帖子数
        int maxComments = Integer.parseInt(configDatas.getHome_HomeBrowseCount()); // 最多评论5个帖子
        int scrollAttempts = 0; // 滚动次数
        int maxScrollAttempts = 15; // 最多滚动15次
        long currentScrollPosition = 0; // 记录当前滚动位置

        try {
            while (commentedCount < maxComments && scrollAttempts < maxScrollAttempts) {
                // 获取当前页面的滚动位置
                currentScrollPosition = ((Number) js.executeScript("return window.pageYOffset;")).longValue();

                List<WebElement> commentButtons = driver.findElements(By.cssSelector("svg[aria-label='评论'],svg[aria-label='Comment']"));
                boolean foundValidPost = false;

                for (WebElement svgElement : commentButtons) {
                    // 检查元素是否在当前可视区域内或稍微下方
                    Number elementTopNum = (Number) js.executeScript("return arguments[0].getBoundingClientRect().top;", svgElement);
                    if (elementTopNum != null) {
                        double elementTop = elementTopNum.doubleValue();
                        if (elementTop >= -100 && elementTop <= 1000) { // 在可视区域内或稍微下方
                            if (commentOnPost(svgElement, driver, js, commentedCount, currentScrollPosition)) {
                                commentedCount++;
                                foundValidPost = true;
                                if (commentedCount >= maxComments) {
                                    break;
                                }
                            }
                        }
                    }
                }

                // 如果还没达到目标数量，继续滚动页面
                if (commentedCount < maxComments) {
                    log.info("滚动页面加载更多帖子...");
                    // 确保页面向下滚动
                    js.executeScript("window.scrollTo(0, " + (currentScrollPosition + 700) + ");");
                    Thread.sleep(3000);
                    scrollAttempts++;
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
    private boolean commentOnPost(WebElement svgElement, WebDriver driver, JavascriptExecutor js, int commentedCount, long currentScrollPosition) {
        try {
            if (!svgElement.isDisplayed()) {
                return false;
            }

            // 不使用scrollIntoView，避免页面跳转，只确保元素可见
            Number elementTopNum = (Number) js.executeScript("return arguments[0].getBoundingClientRect().top;", svgElement);
            if (elementTopNum != null) {
                double elementTop = elementTopNum.doubleValue();
                if (elementTop < 0 || elementTop > 800) {
                    // 如果元素不在合适的可视区域，轻微调整滚动位置
                    js.executeScript("window.scrollTo(0, " + (currentScrollPosition + (long) elementTop - 400) + ");");
                }
            }
            Thread.sleep(1000);

            WebElement clickableParent = findClickableParent(svgElement, js);
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
                WebElement commentIconInPopup = commentModal.findElement(By.cssSelector("svg[aria-label='评论'],svg[aria-label='Comment']"));
                WebElement clickableCommentButton = findClickableParent(commentIconInPopup, js);
                if (clickableCommentButton != null) {
                    js.executeScript("arguments[0].click();", clickableCommentButton);
                    Thread.sleep(1000); // 等待输入框出现
                }
            } catch (Exception e) {
                log.warn("在弹窗中未找到或无法点击评论图标，将直接尝试输入评论。");
                // 即使找不到图标，也继续尝试，因为UI可能已经允许直接输入
            }

            // 检测是否限制评论
            try {
                WebElement restrictedComment = driver.findElement(By.xpath("//span[normalize-space()='这篇帖子限制评论了。']"));
                if (restrictedComment != null && restrictedComment.isDisplayed()) {
                    log.warn("检测到帖子限制评论，跳过该帖子");
                    // 记录关闭评论框前的滚动位置
                    long scrollPositionBeforeClose = ((Number) js.executeScript("return window.pageYOffset;")).longValue();
                    closeCommentBox(js);
                    // 恢复滚动位置，确保页面不跳转
                    js.executeScript("window.scrollTo(0, " + scrollPositionBeforeClose + ");");
                    Thread.sleep(500); // 等待页面稳定
                    return false;
                }
            } catch (NoSuchElementException e) {
                // 没有找到限制评论的提示，继续正常流程
            }
            boolean success = submitComment(driver, js, commentedCount);
            // 记录关闭评论框前的滚动位置
            long scrollPositionBeforeClose = ((Number) js.executeScript("return window.pageYOffset;")).longValue();
            closeCommentBox(js);
            // 恢复滚动位置，确保页面不跳转
            js.executeScript("window.scrollTo(0, " + scrollPositionBeforeClose + ");");
            Thread.sleep(500); // 等待页面稳定

            return success;
        } catch (Exception e) {
            log.warn("评论单个帖子时出现异常: {}", e.getMessage());
            return false;
        }
    }

    /**
     * 提交评论
     */
    private boolean submitComment(WebDriver driver, JavascriptExecutor js, int commentedCount) {
        String[] comments = this.data.getSendData().getLeaveText().split("\\n\\n\\n");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        try {
            String commentInputSelector = "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x1qjc9v5.xjbqb8w.xjwep3j.x1t39747.x1wcsgtt.x1pczhz8.xr1yuqi.x11t971q.x4ii5y1.xvc5jky.x15h9jz8.x47corl.xh8yej3.xir0mxb.x1juhsu6 > div > article > div > div.x1qjc9v5.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x5wqa0o.xln7xf2.xk390pu.xdj266r.x14z9mp.xat24cr.x1lziwak.x65f84u.x1vq45kp.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x11njtxf > div > div > div.x78zum5.xdt5ytf.x1q2y9iw.x1n2onr6.xh8yej3.x9f619.x1iyjqo2.x13lttk3.x1t7ytsu.xpilrb4.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1b5io7h > section.x5ur3kl.x13fuv20.x178xt8z.x1roi4f4.x2lah0s.xvs91rp.xl56j7k.x17ydfre.x1n2onr6.x10b6aqq.x1yrsyyn.x1hrcb2b.xv54qhq > div > form > div > textarea";
            WebElement commentInput = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(commentInputSelector)));
            String commentText = comments[commentedCount % comments.length];
            //输入评论
            commentInput.sendKeys(commentText);
            Thread.sleep(1000);

            //发送评论
            String postSelector = "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x1qjc9v5.xjbqb8w.xjwep3j.x1t39747.x1wcsgtt.x1pczhz8.xr1yuqi.x11t971q.x4ii5y1.xvc5jky.x15h9jz8.x47corl.xh8yej3.xir0mxb.x1juhsu6 > div > article > div > div.x1qjc9v5.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x5wqa0o.xln7xf2.xk390pu.xdj266r.x14z9mp.xat24cr.x1lziwak.x65f84u.x1vq45kp.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x11njtxf > div > div > div.x78zum5.xdt5ytf.x1q2y9iw.x1n2onr6.xh8yej3.x9f619.x1iyjqo2.x13lttk3.x1t7ytsu.xpilrb4.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1b5io7h > section.x5ur3kl.x13fuv20.x178xt8z.x1roi4f4.x2lah0s.xvs91rp.xl56j7k.x17ydfre.x1n2onr6.x10b6aqq.x1yrsyyn.x1hrcb2b.xv54qhq > div > form > div > div.x13fj5qh > div";
            js.executeScript("document.querySelector('" + postSelector + "').click();");
            log.info("成功评论第{}个帖子: {}", commentedCount + 1, commentText);
            Thread.sleep(3000);
            return true;

        } catch (Exception e) {
            log.warn("评论输入框操作失败: {}", e.getMessage());
            return false;
        }
    }

    /**
     * 进入个人首页
     */
    private void goToProfilePage(WebDriver driver, JavascriptExecutor js) {
        Data.ConfigDatas configDatas = data.getSendData().getConfigDatas();

        List<Data.UserInFIdList> userInFIdList = data.getUserInFIdList();
        // 从UserInFIdList数组中获取第一个元素的Id和Count
        if (userInFIdList != null && !userInFIdList.isEmpty()) {
            Data.UserInFIdList firstItem = userInFIdList.get(0);
            Integer id = Integer.valueOf(firstItem.getId()); //成员分类
            Integer Count = Integer.valueOf(firstItem.getCount()); //帖子数量
            
            ProfilePage profilePage = httpRequest.getProfilePage(Count, id);
            processProfilePage(profilePage, driver, js);
        } else {
            log.warn("UserInFIdList为空，无法获取用户列表");
        }
    }
    
    /**
     * 处理ProfilePage数据
     */
    private void processProfilePage(ProfilePage profilePage, WebDriver driver, JavascriptExecutor js) {
        if (profilePage != null) {
            String[] MsgText = this.data.getSendData().getMsgText().split("\\n\\n\\n");
            for (ProfilePage.User user : profilePage.getUserList()) {
                try {
                    String userId = user.getUser_id();
                    String userName = user.getUser_name();
                    String userFullName = user.getUser_fullname();
                    String instagramId = user.getInstagram_id();
                    String instagraminfId = user.getInstagraminf_id();
                    String createdAt = user.getCreated_at();
                    int types = user.getTypes();

                    driver.get("https://www.instagram.com/" + userName);
                    log.info("进入用户主页: {}", userName);
                    //打开弹窗点击私信按钮
                    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
                    // 更多按钮
                    String moreSelector = "svg[aria-label='选项'],svg[aria-label='Options']";
                    WebElement more = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(moreSelector)));
                    more.click();

                    Thread.sleep(1000);
                    String messageSelector = "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > button:nth-child(6)";
                    WebElement message = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(messageSelector)));
                    message.click();

                    //检查是否有消息通知弹窗
                    try {
                        WebElement messageNotify = wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath("//h2[normalize-space()='打开通知']")));
                        if (messageNotify != null && messageNotify.isDisplayed()) {
                            WebElement closeButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[normalize-space()='以后再说']")));
                            closeButton.click();
                            log.info("检测到消息通知弹窗，已关闭");
                        }
                    } catch (org.openqa.selenium.TimeoutException e) {
                        // 没有找到消息通知弹窗，继续正常流程
                        log.debug("未检测到消息通知弹窗，继续正常流程");
                    }
                    WebElement messageP = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("body > div > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x9f619.x1f5funs.xvbhtw8.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.xvc5jky.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa > section > main > section > div > div > div > div.xjp7ctv > div > div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k > div > div.html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x9f619.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1iyjqo2.x2lwn1j.xeuugli.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.xcrg951.x6prxxf.x6ikm8r.x10wlt62.x1n2onr6.xh8yej3 > div > div.x78zum5.xdt5ytf.x1iyjqo2.x193iq5w.x2lwn1j.x1n2onr6 > div:nth-child(2) > div > div > div > div > div.html-div.xat24cr.xexx8yu.xyri2b.x1c1uobl.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1xmf6yo.x13fj5qh.x2fvf9.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.xs9asl8 > div > div.xzsf02u.x1a2a7pz.x1n2onr6.x14wi4xw.x1iyjqo2.x1gh3ibb.xisnujt.xeuugli.x1odjw0f.notranslate > p")));
                    //从MsgText数组中随机获取一条数据
                    String msgText = MsgText[new Random().nextInt(MsgText.length)];
                    messageP.sendKeys(msgText);

                    //点击发送按钮
                    WebElement sendButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//div[@role='button'][@tabindex='0' and normalize-space()='Send']")));
                    sendButton.click();
                } catch (Exception e) {
                    log.warn("进入用户主页失败: {}", e.getMessage());
                }
            }
        } else {
            log.warn("获取ProfilePage失败，无法进行私信操作");
        }
    }

    /**
     * 关闭评论弹窗
     */
    private void closeCommentBox(@NotNull JavascriptExecutor js) {
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
