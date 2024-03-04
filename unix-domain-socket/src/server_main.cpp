#include "uds_server.hpp"
#include <memory>
#include <thread>
#include <chrono>
#include <iostream>

int main () {
    std::shared_ptr<toolbox::uds::UDSServer> server = std::make_shared<toolbox::uds::UDSServer>();
    if (!server->Bind()) std::cout << "unable to bind" << std::endl;
    if (!server->Listen()) std::cout << "unable to listen" << std::endl;
    server->Start();
    std::this_thread::sleep_for(std::chrono::seconds(5));
    server->Stop();
    return 0;
}