#ifndef AUTH_H
#define AUTH_H

#include <string>
#include <unordered_map>

class AuthSystem {
public:
    bool registerUser(const std::string& username, const std::string& password);
    bool loginUser(const std::string& username, const std::string& password);
    
private:
    std::unordered_map<std::string, std::string> users; // username -> password
};

#endif // AUTH_H