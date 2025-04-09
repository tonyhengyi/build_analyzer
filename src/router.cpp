#include "../include/router.h"
#include <string>

void setup_routes(httplib::Server& server, AuthSystem& authSystem) {
    // 服务静态文件 (HTML, CSS, JS)
    server.set_mount_point("/", "./static");

    // 注册接口
    server.Post("/api/register", [&](const httplib::Request& req, httplib::Response& res) {
        auto username = req.get_param_value("username");
        auto password = req.get_param_value("password");
        
        if (authSystem.registerUser(username, password)) {
            res.set_content("{\"success\": true, \"message\": \"Registration successful\"}", "application/json");
        } else {
            res.set_content("{\"success\": false, \"message\": \"Username already exists\"}", "application/json");
        }
    });
    
    // 登录接口
    server.Post("/api/login", [&](const httplib::Request& req, httplib::Response& res) {
        auto username = req.get_param_value("username");
        auto password = req.get_param_value("password");
        
        if (authSystem.loginUser(username, password)) {
            res.set_content("{\"success\": true, \"message\": \"Login successful\"}", "application/json");
        } else {
            res.set_content("{\"success\": false, \"message\": \"Invalid username or password\"}", "application/json");
        }
    });
}