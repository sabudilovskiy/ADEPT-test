#pragma once
#include <boost/uuid/uuid.hpp>
#include <optional>
#include <string_view>
#include <userver/storages/postgres/cluster.hpp>
#include <chrono>
#include <userver/utils/datetime.hpp>

namespace helpers{
    std::optional<boost::uuids::uuid> GetToken(
            const userver::storages::postgres::ClusterPtr& cluster_ptr,
            std::string_view login,
            std::string_view password,
            userver::storages::postgres::TimePointTz now,
            userver::storages::postgres::TimePointTz end_ts);

    std::optional<boost::uuids::uuid> RegisterUser(
            const userver::storages::postgres::ClusterPtr& cluster_ptr,
            std::string_view login,
            std::string_view password,
            userver::storages::postgres::TimePointTz end_ts);
}
