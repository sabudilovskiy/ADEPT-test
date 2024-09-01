#pragma once
#include "handler_fwd.hpp"
#include "io.hpp"
#include <uopenapi/all.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/storages/postgres/postgres.hpp>
#include <codegen/sql.hpp>
#include <helpers/auth.hpp>
#include <userver/formats/parse/boost_uuid.hpp>
#include <userver/formats/serialize/boost_uuid.hpp>

namespace views::Register{
    using base = uopenapi::components::openapi_handler<Request,Response200,Response400 >;
    struct handler : base{
        static constexpr std::string_view kName = "register_handler";
        handler(const userver::components::ComponentConfig& cfg,
                const userver::components::ComponentContext& ctx) : base(cfg, ctx),
                todo_db(ctx.FindComponent<userver::components::Postgres>("todo_db").GetCluster()){}
        response handle(views::Register::Request req) const override{
            userver::storages::postgres::TimePointTz end_ts(userver::utils::datetime::Now() + std::chrono::hours(1));
            auto token = helpers::RegisterUser(
                    todo_db,
                    req.body.login,
                    req.body.password,
                    end_ts);
            if (token){
                Response200 response200;
                response200().body.token = *token;
                return response200;
            }
            else {
                Response400 resp400;
                resp400().body.message = "Username is busy. Use another";
                resp400().body.error_code = models::ErrorCode::username_busy;
                return resp400;
            }
        }
    private:
        userver::storages::postgres::ClusterPtr todo_db;
    };
}
