#include "uds_client.hpp"
#include "uds_helper.hpp"
#include <fcntl.h>
#include <unistd.h>

using namespace toolbox::uds;

UDSClient::UDSClient() {
    m_server_file_descriptor = helper::Guard(socket(AF_UNIX, SOCK_STREAM, 0), "could not create client socket");
    memset(&m_socket_address, 0, sizeof(sockaddr_un));
    m_socket_address.sun_family = AF_UNIX;
    strncpy(m_socket_address.sun_path, SV_SOCK_PATH, sizeof(m_socket_address.sun_path) - 1);
}

bool
UDSClient::Connect() {
    auto result = connect(m_server_file_descriptor, reinterpret_cast<sockaddr*>(&m_socket_address), sizeof(sockaddr_un));
    return result == -1 ? false : true;
}

void
UDSClient::Start() {
    ssize_t num_read;
    while ((num_read = read(STDIN_FILENO, m_buffer, BUF_SIZE)) > 0)
        if (write(m_server_file_descriptor, m_buffer, num_read) != num_read)
            helper::Error("partial/failed write");
}