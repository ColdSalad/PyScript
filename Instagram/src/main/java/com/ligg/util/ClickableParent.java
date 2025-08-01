package com.ligg.util;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;

/**
 * @Author Ligg
 * @Time 2025/8/1
 **/
public class ClickableParent {

    /**
     * 查找SVG元素的可点击父元素
     */
    public static WebElement findClickableParent(WebElement svgElement, JavascriptExecutor js) {
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
}
