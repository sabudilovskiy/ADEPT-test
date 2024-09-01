#pragma once
#include "handler_fwd.hpp"
#include "io.hpp"
#include <uopenapi/all.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/storages/postgres/postgres.hpp>
#include <userver/formats/parse/boost_uuid.hpp>
#include <userver/formats/serialize/boost_uuid.hpp>

namespace views::login{
    using base = uopenapi::components::openapi_handler<Request,Response200,Response400 >;
    struct handler : base{
        static constexpr std::string_view kName = "login_handler";
        handler(const userver::components::ComponentConfig& cfg,
                const userver::components::ComponentContext& ctx) : base(cfg, ctx),
                todo_db(ctx.FindComponent<userver::components::Postgres>("todo_db").GetCluster()){}
        response handle(views::login::Request req) const override;
    private:
        userver::storages::postgres::ClusterPtr todo_db;
    };
}
