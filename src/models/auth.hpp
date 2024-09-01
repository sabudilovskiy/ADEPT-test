#pragma once
#include <string>
#include <boost/uuid/uuid.hpp>

namespace models::auth{
    struct RequestBody{
        std::string login;
        std::string password;
    };
    struct Request{
        RequestBody body;
    };
    struct ResponseBody{
        boost::uuids::uuid token;
    };
    struct Response{
        ResponseBody body;
    };
}
