cmake_minimum_required(VERSION 3.10)
project(login_server)

set(CMAKE_CXX_STANDARD 17)

# 包含httplib头文件
include_directories(include)

add_executable(login_server
    src/main.cpp
    src/auth.cpp
    src/router.cpp
)