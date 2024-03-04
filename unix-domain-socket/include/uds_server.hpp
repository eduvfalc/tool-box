#ifndef H_UDS_SERVER_HPP
#define H_UDS_SERVER_HPP

#include "uds_definitions.hpp"
#include <atomic>
#include <thread>
#include <string>

#define BACKLOG 5

namespace toolbox::uds {

class UDSServer {
    public:
        UDSServer();
        bool Bind();
        bool Listen();
        void Start();
        void Stop();

    private:
        std::atomic<bool> m_is_running{false};
        sockaddr_un m_socket_address;
        int m_server_file_descriptor;
        char m_buffer[BUF_SIZE];
        std::thread m_server_thread;
        
        void Run();
};

} // namespace toolbox::uds

#endif // H_UDS_SERVER_HPP