#include "uds_helper.hpp"
#include <iostream>

namespace toolbox::uds::helper
{

int Guard(int value, const std::string& error_message) {
    if (-1 == value){
        Error(error_message);
    }
    return value;
}

void Error(const std::string& error_message) {
    std::cerr << error_message << std::endl;
    std::exit(EXIT_FAILURE);
}

}