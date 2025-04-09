#ifndef ROUTER_H
#define ROUTER_H

#include <httplib.h>
#include "auth.h"

void setup_routes(httplib::Server& server, AuthSystem& authSystem);

#endif // ROUTER_H