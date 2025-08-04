package com.ligg.automation;

import com.ligg.http_request.HttpRequest;
import com.ligg.pojo.Data;
import com.ligg.pojo.ProfilePage;
import com.ligg.service.CookieService;
import com.ligg.service.HomeEnableBrowse;
import com.ligg.service.PrivateMessage;
import com.ligg.service.CommonService;
import com.ligg.service.impl.CookieServiceImpl;
import com.ligg.service.impl.HomeEnableBrowseImpl;
import com.ligg.service.impl.PrivateMessageImpl;
import com.ligg.service.impl.CommonServiceImpl;
import javafx.application.Platform;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
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

import java.time.Duration;
import java.util.List;
import java.util.Objects;
import java.util.Random;


/**
 * @Author Ligg
 * @Time 2025/7/2
 **/
public class OpenBrowser {

    private static final Logger log = LoggerFactory.getLogger(OpenBrowser.class);
    private WebDriver driver;
    private static final PrivateMessage privateMessage = new PrivateMessageImpl();
    private static final HttpRequest httpRequest = new HttpRequest();
    private static final CookieService cookieService = new CookieServiceImpl();
    private static final HomeEnableBrowse homeEnableBrowse = new HomeEnableBrowseImpl();
    private static final CommonService commonService = new CommonServiceImpl();
    private String adminUsername;
    private Data data = null;

    //打开浏览器
    public void Login(String username, String password, Button loginButton, String adminUsername) {
        this.adminUsername = adminUsername;
        //创建一个线程用于打开浏览器，避免GUI阻塞主线程
        new Thread(() -> {
            try {
                driver = new ChromeDriver();
                driver.get("https://www.instagram.com/");
            } catch (Exception e) {
                log.info("尝试启动Edge浏览器...");
                driver = new EdgeDriver();
                driver.get("https://www.instagram.com/");

            }

            try {
                Thread.sleep(2000);
                log.info("开始添加 Instagram cookies...");

                // 首先尝试从 JSON 文件加载 cookies
                cookieService.loadCookiesFromJson(driver);

                cookieService.getCookieValue(driver, "sessionid");

                driver.navigate().refresh(); // 刷新页面使 cookies 生效
                //TODO 如果无法进入首页说明Cookie过期，需要删除 instagram_cookies.json文件 重新获取
                Thread.sleep(3000);
            } catch (Exception e) {
                log.warn("添加 cookies 失败: {}", e.getMessage());
            }

            // 检查登录状态并处理登录逻辑
            try {
                Thread.sleep(5000);

                // 检查是否已经登录（通过检测登录表单是否存在）
                boolean needLogin;
                try {
                    // 尝试查找登录表单，如果找到说明需要登录
                    WebElement loginForm = driver.findElement(By.xpath("//*[@id=\"loginForm\"]"));
                    log.info("检测到登录表单，需要手动登录");
                    needLogin = true;
                    cookieService.deleteAllCookies(driver);
                    //选中账号、密码输入框
                    WebElement usernameInput = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[1]/div[1]/div/label/input"));
                    WebElement passwordInput = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[1]/div[2]/div/label/input"));
                    if (usernameInput.isDisplayed()) {
                        log.info("已找到用户名输入框，开始填入登录信息");
                        usernameInput.sendKeys(username);
                        passwordInput.sendKeys(password);
                        //点击登录按钮
                        WebElement webLoginButton = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[1]/div[3]/button"));
                        webLoginButton.click();
                        Thread.sleep(5000);

                        // 手动登录成功后，获取并保存 sessionid cookie
                        log.info("手动登录成功，开始获取 sessionid cookie...");
                        String sessionId = cookieService.getCookieValue(driver, "sessionid");
                        if (sessionId != null) {
                            log.info("成功获取 sessionid: {}", sessionId);
                            // 保存所有 cookies 到 JSON 文件
                            cookieService.saveCookiesToJson(driver);
                        } else {
                            log.warn("未能获取到 sessionid cookie");
                        }
                    }
                } catch (org.openqa.selenium.NoSuchElementException e) {
                    // 找不到登录表单，说明已经通过 cookie 登录
                    log.info("未检测到登录表单，已通过 cookie 完成登录");
                    needLogin = false;
                }

                // 根据登录状态决定后续操作
                if (needLogin) {
                    // 如果进行了手动登录，需要等待并导航到主页
                    Thread.sleep(5000);
                    String currentUrl = driver.getCurrentUrl();
                    log.info("登录后当前 URL: {}", currentUrl);

                    // 如果不在主页，尝试点击主页按钮
                    if (currentUrl != null && !currentUrl.equals("https://www.instagram.com/?next=%2F")) {
                        try {
                            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
                            var homeButton = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("body > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div > div > div > div > div > div:nth-of-type(1) > div > span > div > a > div")));
                            homeButton.click();
                            Thread.sleep(3000);
                        } catch (Exception e) {
                            log.warn("无法找到主页按钮，直接导航到主页");
                            driver.get("https://www.instagram.com/");
                            Thread.sleep(3000);
                        }
                    }
                } else {
                    // 如果通过 cookie 登录，直接等待页面稳定
                    Thread.sleep(3000);
                    log.info("Cookie 登录成功，页面已准备就绪");
                }

                //开始自动化操作
                log.info("开始执行自动化操作");
                operation(driver, loginButton);

            } catch (InterruptedException e) {
                log.error("网页加载超时: {}", e.getMessage());
            } catch (Exception e) {
                log.error("登录过程中发生异常: {}", e.getMessage());
            }
        }).start();
    }

    /**
     * 开始干活
     */
    public void operation(WebDriver driver, Button loginButton) {
        Data data = httpRequest.getData(adminUsername);
        this.data = data;
        updateButtonState(loginButton);
        new WebDriverWait(driver, Duration.ofSeconds(10));
        JavascriptExecutor js = (JavascriptExecutor) driver;

        Data.ConfigDatas configDatas = data.getSendData().getConfigDatas();


        //首页浏览
        if (Objects.equals(configDatas.getHome_IsEnableBrowse(), "true")) {
            int maxComments = Integer.parseInt(data.getSendData().getConfigDatas().getHome_HomeBrowseCount());
            try {
                for (int i = 0; i < maxComments; i++) {
                    //点赞
                    if (Objects.equals(configDatas.getHome_IsEnableLike(), "true")) {
                        log.info("开始自动点赞...");
                        homeEnableBrowse.like(driver, js, loginButton);
                    }
                    Thread.sleep(3000);
                    //评论
                    if (Objects.equals(configDatas.getHome_IsEnableLeave(), "true")) {
                        homeEnableBrowse.comment(driver, loginButton, data);
                    }

                    js.executeScript("window.scrollBy(0, 800);"); // 向下滚动800像素
                    Thread.sleep(3000);
                }
            } catch (Exception e) {
                log.error("浏览过程中发生异常：{}", e.getMessage());
            }

        }

        //互动
        if (Objects.equals(configDatas.getHuDong_IsHuDong(), "true")) {
            goToProfilePage(driver, js);
        }

        //关键词送欧式搜索
        if (Objects.equals(configDatas.getKey_IsEnableKey(), "true")) {
            search(driver);
        }

        //结束后弹窗通知是否关闭浏览器
        Platform.runLater(() -> {
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("操作完成");
            alert.setHeaderText("自动化操作已完成");
            alert.setContentText("是否需要关闭浏览器?");

            ButtonType closeBrowser = new ButtonType("关闭浏览器");
            ButtonType keepBrowser = new ButtonType("保持打开");

            alert.getButtonTypes().setAll(closeBrowser, keepBrowser);

            alert.showAndWait().ifPresent(buttonType -> {
                if (buttonType == closeBrowser) {
                    if (driver != null) {
                        driver.quit();
                    }
                } else {
                    updateButtonState(loginButton);
                }
            });
        });
    }


    /**
     * 进入个人首页
     */
    private void goToProfilePage(WebDriver driver, JavascriptExecutor js) {
        List<Data.UserInFIdList> userInFIdList = data.getUserInFIdList();

        Data.UserInFIdList userInFI = userInFIdList.get(0);
        Integer id = Integer.parseInt(userInFI.getId());
        Integer count = Integer.parseInt(this.data.getSendData().getConfigDatas().getHuDong_GetUserCount());
        ProfilePage profilePage = httpRequest.getProfilePage(count, id);

        if (profilePage != null) {
            //私信内容
            String[] MsgText = this.data.getSendData().getMsgText().split("\\n\\n\\n");
            //留言内容
            String[] LeaveText = this.data.getSendData().getLeaveText().split("\\n\\n\\n");
            for (ProfilePage.User user : profilePage.getUserList()) {
                try {
                    String userId = user.getUser_id();
                    String userName = user.getUser_name();
                    String userFullName = user.getUser_fullname();
                    String instagramId = user.getInstagram_id();
                    String instagraminfId = user.getInstagraminf_id();
                    String createdAt = user.getCreated_at();
                    int types = user.getTypes();
                    String instagramURL = "https://www.instagram.com/";
                    String msgText = MsgText[new Random().nextInt(MsgText.length)];//从MsgText数组中随机获取一条消息
                    String url = instagramURL + userName;
                    driver.get(url);

                    //追踪(关注)
                    if (Objects.equals(this.data.getSendData().getConfigDatas().getHuDong_IsEnableTracking(), "true")) {
                        commonService.EnableLeave(driver);
                        Thread.sleep(3000);
                        //结束后重新回到用户首页
                        driver.get(url);

                    }
                    //发送私信
                    if (Objects.equals(this.data.getSendData().getConfigDatas().getHuDong_IsEnableMsg(), "true")) {
                        privateMessage.sendPrivateMessage(driver, userName, msgText);
                        Thread.sleep(1000);
                        driver.get(url);
                    }
                    //点赞
                    if (Objects.equals(this.data.getSendData().getConfigDatas().getHuDong_IsEnableLike(), "true")) {
                        commonService.EnableLike(driver, url, this.data.getSendData().getConfigDatas().getHuDong_TrackingUserCount());
                        Thread.sleep(1000);
                        driver.get(url);
                    }

                    //留言(评论)
                    if (Objects.equals(this.data.getSendData().getConfigDatas().getHuDong_IsEnableLeave(), "true")) {
                        //随机获取一条留言内容
                        String text = LeaveText[new Random().nextInt(LeaveText.length)];
                        commonService.comments(driver, url, this.data.getSendData().getConfigDatas().getHuDong_TrackingUserCount(), text);
                        Thread.sleep(1000);
                        driver.get(url);
                    }
                    Thread.sleep(2000); //等待发送完成
                } catch (Exception e) {
                    log.warn("进入用户主页失败: {}", e.getMessage());
                }
            }
        }
    }

    /**
     * 关键字搜索
     */
    private void search(WebDriver driver) {

        String instagram = "https://www.instagram.com";
        driver.get(instagram + "/?next=%2F");
        String[] MsgText = this.data.getSendData().getMsgText().split("\\n\\n\\n");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        try {


            String[] keys = this.data.getSendData().getConfigDatas().getKeys().split("#");

            for (String key : keys) {
                //点击搜索按钮
                WebElement searchSvg = wait.until(ExpectedConditions.presenceOfElementLocated(
                        By.cssSelector("svg[aria-label='搜索']")
                ));
                searchSvg.click();

                Thread.sleep(2000);
                //搜索框中输入关键字
                WebElement searchInput = wait.until(ExpectedConditions.presenceOfElementLocated(
                        By.cssSelector("input[aria-label='搜索输入']")
                ));
                searchInput.sendKeys(key);
                log.info("已输入搜索关键字: {}", this.data.getSendData().getConfigDatas().getKeys());
                Thread.sleep(2000);

                //获取搜索条目集合
                List<WebElement> searchItems = wait.until(ExpectedConditions.presenceOfAllElementsLocatedBy(
                        By.cssSelector("div > div > div.x9f619.x1ja2u2z.x78zum5.x1n2onr6.x1iyjqo2.xs83m0k.xeuugli.x1qughib.x6s0dn4.x1a02dak.x1q0g3np.xdl72j9 > div > div > div > span")
                ));
                //创建一个String数组，用于存储搜索条目
                String[] searchItemTexts = new String[searchItems.size()];
                //遍历搜索条目集合，将每个条目的文本存储到String数组中
                for (int i = 0; i < searchItems.size(); i++) {
                    searchItemTexts[i] = searchItems.get(i).getText();
                }

                //遍历搜索条目，打开每个条目的页面
                for (String searchItemText : searchItemTexts) {
                    String url = instagram + "/" + searchItemText;
                    Thread.sleep(2000);
                    driver.get(url);
                    String msgText = MsgText[new Random().nextInt(MsgText.length)];

                    // 追踪(关注)
                    if (Objects.equals(this.data.getSendData().getConfigDatas().getKey_IsEnableTracking(), "true")) {
                        commonService.EnableLeave(driver);
                    }

                    // 点赞
                    if (Objects.equals(this.data.getSendData().getConfigDatas().getKey_IsEnableLike(), "true")) {
                        commonService.EnableLike(driver, url, this.data.getSendData().getConfigDatas().getKey_SearchCount());
                    }

                    // 发送私信
                    if (Objects.equals(this.data.getSendData().getConfigDatas().getKey_IsEnableLeave(), "true")) {
                        privateMessage.sendPrivateMessage(driver, searchItemText, msgText);
                        Thread.sleep(2000);
                    }
                    Thread.sleep(2000);
                }
                driver.get(instagram);
                Thread.sleep(2000);
            }

        } catch (Exception e) {
            log.warn("关键词操作失败: {}", e.getMessage());
        }
    }


    /**
     * 更新按钮状态
     */
    private void updateButtonState(Button button) {
        Platform.runLater(() -> {
            button.setText("完成");
            button.setDisable(false);
        });
    }
}
