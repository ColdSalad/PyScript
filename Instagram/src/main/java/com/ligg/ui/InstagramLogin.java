package com.ligg.ui;

import com.ligg.automation.OpenBrowser;
import com.ligg.http_request.HttpRequest;
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
 * @Time 2025/7/2
 **/
public class InstagramLogin extends Application {
    private static final Logger log = LoggerFactory.getLogger(InstagramLogin.class);
    private WebDriver driver;
    private static final HttpRequest httpRequest = new HttpRequest();
    private static final CookieService cookieService = new CookieServiceImpl();

    @Override
    public void start(Stage stage) {
        //设置窗口标题
        stage.setTitle("后台登录验证");
        //设置icon
        stage.getIcons().add(new Image(Objects.requireNonNull(getClass().getResourceAsStream("/image/instagram_logo.jpg"))));
        //创建一个垂直盒子布局作为根容器
        VBox root = new VBox(20);
        root.setAlignment(Pos.CENTER);
        root.setPadding(new Insets(20, 20, 20, 20));

        //添加Logo
        Image logoImage = new Image(Objects.requireNonNull(getClass().getResourceAsStream("/image/instagram_logo.jpg")));
        ImageView logo = new ImageView(logoImage);
        logo.setFitHeight(80);
        logo.setFitWidth(80);
        logo.setPreserveRatio(true);

        //创建输入框
        TextField usernameField = new TextField();
        usernameField.setPromptText("请输入后台用户名");
        usernameField.setPrefWidth(200);

        PasswordField passwordField = new PasswordField();
        passwordField.setPromptText("请输入后台密码");
        passwordField.setPrefWidth(200);

        //创建登录按钮
        Button loginButton = new Button("后台登录");
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

            loginButton.setText("验证中...");
            loginButton.setDisable(true);

            String response = httpRequest.login(username, password);
            if (response == null || response.contains("ok") || response.contains("no")) {
                Platform.runLater(() -> {
                    Alert alert = new Alert(Alert.AlertType.WARNING);
                    alert.setTitle("提示");
                    alert.setHeaderText(response);
                    alert.showAndWait();
                });
                loginButton.setText("后台登录");
                loginButton.setDisable(false);
                return;
            }

            // 登录成功，关闭当前窗口并打开Instagram登录界面
            stage.close();
            try {
                driver = new ChromeDriver();
                driver.get("https://www.instagram.com/");
            } catch (Exception e) {
                driver = new EdgeDriver();
                driver.get("https://www.instagram.com/");
            }

            // 首先尝试从 JSON 文件加载 cookies
            cookieService.loadCookiesFromJson(driver);

            cookieService.getCookieValue(driver, "sessionid");
            driver.navigate().refresh(); // 刷新页面使 cookies 生效

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
            }catch (Exception e) {
                log.warn("未检测到登录表单，已通过 cookie 完成登录");
            }
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
