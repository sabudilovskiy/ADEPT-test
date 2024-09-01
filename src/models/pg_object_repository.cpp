#include "pg_object_repository.hpp"
#include "codegen/sql.hpp"
#include <userver/storages/postgres/cluster.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/utils/datetime.hpp>

namespace models{
    pg_object_respository::pg_object_respository(
        const userver::components::ComponentConfig &cfg,
        const userver::components::ComponentContext &ctx)
        : userver::components::LoggableComponentBase(cfg, ctx) {
    ptr = ctx.FindComponent<userver::components::Postgres>("objects_db")
                .GetCluster();
    }

    api::Object pg_object_respository::add_object(const api::NewObject& new_object){
        auto result = ptr->Execute(userver::storages::postgres::ClusterHostType::kMaster, sql::add_object, new_object, userver::utils::datetime::Now());
        return result.AsSingleRow<api::Object>(userver::storages::postgres::kRowTag);
    }

    void AppendPgObjectRepository(userver::components::ComponentList &list) {
      list.Append<pg_object_respository>("object_repository");
    }
    } // namespace models