#ifndef H_UDS_HELPER_HPP
#define H_UDS_HELPER_HPP

#include <string>

namespace toolbox::uds::helper
{
int Guard(int value, const std::string& error_message);
void Error(const std::string& error_message);
}

#endif //UDS_HELPER_HPP