#ifndef H_UDS_DEFINITIONS_HPP
#define H_UDS_DEFINITIONS_HPP

#include <sys/un.h>
#include <sys/socket.h>
#include <string>

namespace toolbox::uds {

// tmp folder should not be used in production code
const std::string SV_SOCK_PATH = "/tmp/us_example";
const std::size_t BUF_SIZE = 100;

}

#endif // H_UDS_DEFINITIONS_HPP