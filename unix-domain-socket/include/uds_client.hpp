#ifndef H_UDS_CLIENT_HPP
#define H_UDS_CLIENT_HPP

#include "uds_definitions.hpp"

namespace toolbox::uds {

class UDSClient {
    public:
        UDSClient();
        bool Connect();
        void Send();

    private:
        bool m_is_running{false};
        sockaddr_un m_socket_address;
        int m_server_file_descriptor;
        char m_buffer[BUF_SIZE];
};

}

#endif // H_UDS_CLIENT_HPP