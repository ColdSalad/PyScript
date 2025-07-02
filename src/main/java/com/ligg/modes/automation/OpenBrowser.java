                webLoginButton.click();
                Platform.runLater(() -> {
                    loginButton.setDisable(false);
                    loginButton.setText("登录");
                });