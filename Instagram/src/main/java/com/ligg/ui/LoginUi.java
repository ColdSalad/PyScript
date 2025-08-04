package com.ligg.ui;

import com.ligg.automation.OpenBrowser;
import com.ligg.pojo.AdminLogin;
import com.ligg.service.CookieService;
import com.ligg.service.impl.CookieServiceImpl;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Stage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.Objects;


/**
 * @Author Ligg
 * @Time 2025/7/10
 **/
public class LoginUi extends Application {
    private static WebDriver driver;
    private static final Logger log = LoggerFactory.getLogger(LoginUi.class);
    private static final CookieService cookieService = new CookieServiceImpl();
    private static final OpenBrowser openBrowser = new OpenBrowser();

    @Override
    public void start(Stage stage) {
        createInstagramLoginUI(stage);
    }

    /**
     * 创建Instagram登录界面
     */
    public static void createInstagramLoginUI(Stage stage) {
        //设置窗口标题
        stage.setTitle("Instagram 登录");
        //设置icon
        stage.getIcons().add(new Image(Objects.requireNonNull(LoginUi.class.getResourceAsStream("/image/instagram_logo.jpg"))));
        //创建一个垂直盒子布局作为根容器
        VBox root = new VBox(20);
        root.setAlignment(Pos.CENTER);
        root.setPadding(new Insets(20, 20, 20, 20));

        //添加Logo
        Image logoImage = new Image(Objects.requireNonNull(LoginUi.class.getResourceAsStream("/image/instagram_logo.jpg")));
        ImageView logo = new ImageView(logoImage);
        logo.setFitHeight(80);
        logo.setFitWidth(80);
        logo.setPreserveRatio(true);

        //创建输入框
        TextField usernameField = new TextField();
        usernameField.setPromptText("请输入Instagram用户名");
        usernameField.setPrefWidth(200);

        PasswordField passwordField = new PasswordField();
        passwordField.setPromptText("请输入Instagram密码");
        passwordField.setPrefWidth(200);

        //创建登录按钮
        Button loginButton = new Button("登录");
        loginButton.setStyle("-fx-background-color: #3897f0; -fx-text-fill: white;");
        loginButton.setPrefWidth(300);
        loginButton.setFont(Font.font(16));

        //添加登录按钮点击事件
        loginButton.setOnAction(event -> {
            String username = usernameField.getText();
            String password = passwordField.getText();

            if (username.isEmpty() || password.isEmpty()) {
                Platform.runLater(() -> {
                    Alert alert = new Alert(Alert.AlertType.WARNING);
                    alert.setTitle("提示");
                    alert.setHeaderText("请输入用户名和密码");
                    alert.showAndWait();
                });
                return;
            }

            try {
                driver = new ChromeDriver();
                driver.get("https://www.instagram.com/");
            } catch (Exception e) {
                log.info("尝试启动Edge浏览器...");
                driver = new EdgeDriver();
                driver.get("https://www.instagram.com/");

            }

            // 检查登录状态并处理登录逻辑
            try {
                Thread.sleep(5000);

                // 检查是否已经登录（通过检测登录表单是否存在）
                boolean needLogin;
                try {
                    // 尝试查找登录表单，如果找到说明需要登录
                    WebElement loginForm = driver.findElement(By.xpath("//*[@id=\"loginForm\"]"));
                    needLogin = true;

                    cookieService.deleteAllCookies(driver);
                    //选中账号、密码输入框
                    WebElement usernameInput = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[1]/div[1]/div/label/input"));
                    WebElement passwordInput = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[1]/div[2]/div/label/input"));
                    if (usernameInput.isDisplayed()) {
                        log.info("已找到用户名输入框，开始填入登录信息");
                        usernameInput.sendKeys();
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
                openBrowser.operation(driver, loginButton);

            } catch (InterruptedException e) {
                log.error("网页加载超时: {}", e.getMessage());
            } catch (Exception e) {
                log.error("登录过程中发生异常: {}", e.getMessage());
            }
            loginButton.setText("正在启动...");
            loginButton.setDisable(true);

        });

        //将所有元素添加到根容器
        root.getChildren().addAll(logo, usernameField, passwordField, loginButton);

        //创建容器设置样式
        Scene scene = new Scene(root, 400, 500);
        scene.setFill(Color.web("#fafafa"));

        //设置场景并显示
        stage.setScene(scene);
        stage.show();

    }

    public static void main(String[] args) {
        launch(args);
    }
}
