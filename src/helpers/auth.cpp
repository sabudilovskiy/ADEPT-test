#include "auth.hpp"
#include <codegen/sql.hpp>
#include <userver/utils/datetime/date.hpp>

namespace helpers{
    std::optional<boost::uuids::uuid> GetToken(
            const userver::storages::postgres::ClusterPtr& cluster_ptr,
            std::string_view login,
            std::string_view password,
            userver::storages::postgres::TimePointTz now,
            userver::storages::postgres::TimePointTz end_ts){
        auto result = cluster_ptr->Execute(
                userver::storages::postgres::ClusterHostType::kMaster,
                sql::get_token,
                login,
                password,
                now,
                end_ts);
        return result.AsOptionalSingleRow<boost::uuids::uuid>();
    }

    std::optional<boost::uuids::uuid>
    RegisterUser(const userver::storages::postgres::ClusterPtr &cluster_ptr, std::string_view login,
                 std::string_view password, userver::storages::postgres::TimePointTz end_ts) {
        auto result = cluster_ptr->Execute(
                userver::storages::postgres::ClusterHostType::kMaster,
                sql::create_user,
                login,
                password,
                end_ts);
        return result.AsOptionalSingleRow<boost::uuids::uuid>();
    }
}
