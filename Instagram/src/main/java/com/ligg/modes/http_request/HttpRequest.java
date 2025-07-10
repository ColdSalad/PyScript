package com.ligg.modes.http_request;

import com.ligg.modes.automation.OpenBrowser;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @Author Ligg
 * @Time 2025/7/10
 **/
public class HttpRequest {

    private static final Logger log = LoggerFactory.getLogger(OpenBrowser.class);

    /**
     * 发送登录请求
     */
    public String login(String Account, String PassWord) {
        OkHttpClient client = new OkHttpClient();

        String url = String.format("http://aj.ry188.vip/api/Login.aspx?Account=%s&PassWord=%s", Account, PassWord);
        Request request = new Request.Builder()
                .url(url)
                .build();
        try (Response response = client.newCall(request).execute()){
            if (response.body() != null) {
                return response.body().string();
            }
        } catch (Exception e) {
            log.error("发送登录请求失败");
        };
        return null;
    }
}
