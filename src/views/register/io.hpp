#pragma once
#include <string>
#include <uopenapi/http/response.hpp>
#include <models/error_response.hpp>
#include <models/auth.hpp>
#include <boost/uuid/uuid.hpp>

namespace views::Register{

    struct ResponseBody{
        boost::uuids::uuid token;
    };

    struct Response{
        ResponseBody body;
    };

    using Request = models::auth::Request;

    using Response200 = uopenapi::http::response<Response, 200>;
    using Response400 = uopenapi::http::response<models::ErrorResponse, 400>;
}
