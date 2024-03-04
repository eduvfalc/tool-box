#include "uds_client.hpp"
#include <memory>
#include <iostream>

int main () {
    std::shared_ptr<toolbox::uds::UDSClient> client = std::make_shared<toolbox::uds::UDSClient>();
    if (!client->Connect()) std::cout << "unable to connect" << std::endl;
    client->Send();
    return 0;
}