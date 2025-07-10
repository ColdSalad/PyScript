module instagram.automation {
    requires javafx.controls;
    requires javafx.fxml;
    requires org.seleniumhq.selenium.api;
    requires org.seleniumhq.selenium.edge_driver;
    requires org.seleniumhq.selenium.chrome_driver;
    requires org.slf4j;
    requires dev.failsafe.core;
    requires org.junit.jupiter.api;
    requires org.seleniumhq.selenium.support;
    requires com.google.common;
    requires org.json;
    requires okhttp3;

    exports com.ligg.modes.ui;
}
