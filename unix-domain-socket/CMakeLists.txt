cmake_minimum_required(VERSION 3.16)

set(PROJECT_NAME uds)
project(${PROJECT_NAME})

add_executable(${PROJECT_NAME}-server src/server_main.cpp src/uds_server.cpp src/uds_helper.cpp)
target_include_directories(${PROJECT_NAME}-server PUBLIC include)

add_executable(${PROJECT_NAME}-client src/client_main.cpp src/uds_client.cpp src/uds_helper.cpp)
target_include_directories(${PROJECT_NAME}-client PUBLIC include)