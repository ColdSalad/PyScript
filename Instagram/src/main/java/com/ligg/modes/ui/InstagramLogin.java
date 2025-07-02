package com.ligg.modes.ui;

import com.ligg.modes.automation.OpenBrowser;
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

import java.util.Objects;


/**
 * @Author Ligg
 * @Time 2025/7/2
 **/
public class InstagramLogin extends Application {

    private static final OpenBrowser openBrowser = new OpenBrowser();
    @Override
    public void start(Stage stage) {
        //设置窗口标题
        stage.setTitle("InstagramLogin");

        //创建一个垂直盒子布局作为根容器
        VBox root = new VBox(20);
        root.setAlignment(Pos.CENTER);
        root.setPadding(new Insets(40, 40, 40, 40));

        //添加Logo
        Image logoImage = new Image(Objects.requireNonNull(getClass().getResourceAsStream("/image/instagram_logo.jpg")));
        ImageView logo = new ImageView(logoImage);
        logo.setFitHeight(80);
        logo.setFitWidth(180);
        logo.setPreserveRatio(true);

        //创建输入框
        TextField usernameField = new TextField();
        usernameField.setPromptText("请输入用户名");
        usernameField.setPrefWidth(300);

        PasswordField passwordField = new PasswordField();
        passwordField.setPromptText("请输入密码");
        passwordField.setPrefWidth(300);

        //创建登录按钮
        Button loginButton = new Button("登录");
        loginButton.setStyle("-fx-background-color: #3897f0; -fx-text-fill: white;");
        loginButton.setPrefWidth(300);
        loginButton.setFont(Font.font(16));

        //添加登录按钮点击事件
        loginButton.setOnAction(event -> {
            String username = usernameField.getText();
            String password = passwordField.getText();
            if ( username.isEmpty() && password.isEmpty()){
                //添加输入框为空提示
                Platform.runLater(() -> {
                    Alert alert = new Alert(Alert.AlertType.WARNING);
                    alert.setTitle("提示");
                    alert.setHeaderText("请输入用户名和密码");
                    alert.showAndWait();
                });
                return;
            }
            if(username.length() < 6 || password.length() < 6){
                Platform.runLater(() -> {
                    Alert alert = new Alert(Alert.AlertType.WARNING);
                    alert.setTitle("提示");
                    alert.setHeaderText("用户名和密码长度不能小于6位");
                    alert.showAndWait();
                });
                return;
            }
            loginButton.setDisable(true);
            loginButton.setText("登录中...");
            openBrowser.Login(username,password, loginButton);
            //添加一个登录按钮状态
        });

        //将所有元素添加到根容器
        root.getChildren().addAll(logo,usernameField,passwordField,loginButton);

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
