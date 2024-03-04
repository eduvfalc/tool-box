#include "uds_server.hpp"
#include "uds_helper.hpp"
#include <iostream>
#include <thread>
#include <unistd.h>
#include <chrono>
#include <fcntl.h>

using namespace toolbox::uds;

UDSServer::UDSServer() {
    m_server_file_descriptor = helper::Guard(socket(AF_UNIX, SOCK_STREAM, 0), "could not create server socket");
    if (remove(SV_SOCK_PATH) == -1 && errno != ENOENT) {
        helper::Error("could not remove socket");
    }
    auto flags = fcntl(m_server_file_descriptor, F_GETFL);
    if (-1  == flags) {
        helper::Error("could not read socket flags");
    }
    helper::Guard(fcntl(m_server_file_descriptor, F_SETFL, flags | O_NONBLOCK), "could not set socket as non-blocking");
    memset(&m_socket_address, 0, sizeof(sockaddr_un));
    m_socket_address.sun_family = AF_UNIX;
    strncpy(m_socket_address.sun_path, SV_SOCK_PATH, sizeof(m_socket_address.sun_path) - 1);
}

bool
UDSServer::Bind() {
    auto result = bind(m_server_file_descriptor, reinterpret_cast<sockaddr*>(&m_socket_address), sizeof(sockaddr_un));
    return result == -1 ? false : true;
}

bool
UDSServer::Listen() {
    auto result = listen(m_server_file_descriptor, BACKLOG);
    return result == -1 ? false : true;
}

void
UDSServer::Start() {
    m_is_running = true;
    m_server_thread = std::thread(&UDSServer::Run, this);
}

void
UDSServer::Run() {
    ssize_t num_read;
    while (true == m_is_running) {
        auto client_file_descriptor = accept(m_server_file_descriptor, NULL, NULL);
        if (-1 == client_file_descriptor) {
            if (errno == EWOULDBLOCK) {
                // put some delay otherwise CPU load will be high
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            else {
                helper::Error("unable to accept client request");
            }
        }
        else {
            while ((num_read = read(client_file_descriptor, m_buffer, BUF_SIZE)) > 0) {
                if (write(STDOUT_FILENO, m_buffer, num_read) != num_read) {
                    helper::Error("partial/failed write");
                }
            }
            if (-1 == num_read) {
                helper::Error("unable to read");
            }
            helper::Guard(close(client_file_descriptor), "unable to close connection");
        }
    }
}

void
UDSServer::Stop() {
    if (m_is_running) {
        m_is_running = false;
        if (m_server_thread.joinable()){
            m_server_thread.join();
        }
    }
}