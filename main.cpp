#include <iostream>
#include "DnsServer.hpp"
using namespace std;

int main() {
    DnsServer server("127.0.0.1", 1053);
    server.start();
    return 0;
}


