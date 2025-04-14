#!/bin/bash

# 编译服务端
cd server/build
cmake .. && make

# 启动主服务
echo "主服务运行在 http://localhost:8080"
./server