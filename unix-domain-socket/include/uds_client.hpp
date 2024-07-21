#ifndef H_UDS_CLIENT_HPP
#define H_UDS_CLIENT_HPP

#include "uds_definitions.hpp"
#include <cstdint>
#include <vector>

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
        std::vector<uint8_t> m_buffer;
};

}

#endif // H_UDS_CLIENT_HPP