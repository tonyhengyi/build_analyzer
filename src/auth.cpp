#include "../include/auth.h"
#include <string>

bool AuthSystem::registerUser(const std::string& username, const std::string& password) {
    if (users.find(username) != users.end()) {
        return false; // 用户已存在
    }
    users[username] = password;
    return true;
}

bool AuthSystem::loginUser(const std::string& username, const std::string& password) {
    auto it = users.find(username);
    if (it != users.end() && it->second == password) {
        return true; // 验证成功
    }
    return false; // 验证失败
}
