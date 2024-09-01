#pragma once

#include <models/basic_object_repository.hpp>
#include <userver/components/component_list.hpp>
#include <userver/components/loggable_component_base.hpp>
#include <userver/storages/postgres/database_fwd.hpp>

namespace models {
struct pg_object_respository : basic_object_respository,
                               userver::components::LoggableComponentBase {

  api::Object add_object(const api::NewObject &new_object) override;

  pg_object_respository(const userver::components::ComponentConfig &cfg,
                        const userver::components::ComponentContext &ctx);

  Grouped<api::TimeFrameType>
  group_by_time(const api::Datetime &now) const override;

  std::vector<api::Object> get_all() const override;

  Grouped<std::string> group_by_type(std::size_t N) const override;

  Grouped<std::string> group_by_name() const override;

  DistanceGrouped
  group_by_distance(const api::Coordinates &coordinates) const override;

private:
  userver::storages::postgres::ClusterPtr ptr;
};

void AppendPgObjectRepository(userver::components::ComponentList &list);

} // namespace models
