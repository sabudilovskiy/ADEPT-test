#include "handler.hpp"

#include <helpers/auth.hpp>

namespace views::login{
    void Append(userver::components::ComponentList& componentList){
        componentList.Append<handler>();
    }

    handler::response handler::handle(views::login::Request req) const {
        userver::storages::postgres::TimePointTz now(userver::utils::datetime::Now());
        userver::storages::postgres::TimePointTz end_ts(userver::utils::datetime::Now() + std::chrono::hours(1));
        auto token = helpers::GetToken(
                todo_db,
                req.body.login,
                req.body.password,
                now,
                end_ts);
        if (!token){
            Response400 resp400;
            resp400().body.message = "Invalid login or password";
            resp400().body.error_code = models::ErrorCode::invalid_credentials;
            return resp400;
        }
        Response200 response200;
        response200().body.token = *token;
        return response200;
    }
}
