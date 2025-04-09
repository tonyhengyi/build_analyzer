#include "httplib.h"
#include <random>

std::string generate_noise(int length) {
    static const char alphanum[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    std::string noise;
    for (int i = 0; i < length; ++i) {
        noise += alphanum[rand() % (sizeof(alphanum) - 1)];
    }
    return noise;
}

int main() {
    httplib::Server svr;

    // 旧版安全头设置方式
    auto set_secure_headers = [](httplib::Response &res) {
        res.set_header("Content-Security-Policy", "default-src 'self'; script-src 'none'");
        res.set_header("X-Content-Type-Options", "nosniff");
        res.set_header("X-Frame-Options", "DENY");
    };

    // 登录页面
    svr.Get("/", [&](const httplib::Request &req, httplib::Response &res) {
        std::string html = R"(
            <!DOCTYPE html>
            <html>
            <head>
                <title>Secure Login</title>
                <style>
                    body { font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; }
                    .login-box { background: white; max-width: 400px; margin: 50px auto; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                    input { width: 100%; padding: 10px; margin: 8px 0; box-sizing: border-box; }
                    button { background: #4CAF50; color: white; padding: 10px; border: none; width: 100%; }
                </style>
                <!-- )" + generate_noise(32) + R"( -->
            </head>
            <body>
                <div class="login-box">
                    <h2>Login</h2>
                    <form action="/login" method="post">
                        <input type="text" name="username" placeholder="Username" required>
                        <input type="password" name="password" placeholder="Password" required>
                        <button type="submit">Sign In</button>
                    </form>
                </div>
                <!-- )" + generate_noise(128) + R"( -->
            </body>
            </html>
        )";
        
        set_secure_headers(res);
        res.set_content(html, "text/html");
    });

    // 登录处理
    svr.Post("/login", [&](const httplib::Request &req, httplib::Response &res) {
        auto username = req.get_param_value("username");
        auto password = req.get_param_value("password");
        
        set_secure_headers(res);
        if (!username.empty() && !password.empty()) {
            res.set_content("Login successful for user: " + username, "text/plain");
        } else {
            res.set_content("Invalid credentials", "text/plain");
        }
    });

    std::cout << "Server running at http://localhost:8080\n";
    svr.listen("0.0.0.0", 8080);
}