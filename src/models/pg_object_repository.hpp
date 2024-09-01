#pragma once

#include <userver/components/component_list.hpp>
#include <models/basic_object_repository.hpp>
#include <userver/components/loggable_component_base.hpp>
#include <userver/storages/postgres/database_fwd.hpp>

namespace models {
struct pg_object_respository : basic_object_respository,
                               userver::components::LoggableComponentBase {
  api::Object add_object(const api::NewObject& new_object) override;
  pg_object_respository(const userver::components::ComponentConfig &cfg,
                        const userver::components::ComponentContext &ctx);
  
private:
  userver::storages::postgres::ClusterPtr ptr;
};

void AppendPgObjectRepository(userver::components::ComponentList &list);

} // namespace models
