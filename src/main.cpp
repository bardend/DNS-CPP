#include <iostream>
#include "DnsServer.hpp"
using namespace std;

int main() {
    DnsServer server("0.0.0.0", 53);
    server.start();
    return 0;
}
