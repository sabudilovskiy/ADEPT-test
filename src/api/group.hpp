#pragma once
#include <uopenapi/all.hpp>
#include <userver/storages/postgres/io/enum_types.hpp>
#include <userver/storages/postgres/io/user_types.hpp>

namespace api {
UOPENAPI_DECLARE_ENUM(DistanceType, int, hundred, thousand, ten_thousand, far);
UOPENAPI_DECLARE_ENUM(TimeFrameType, int, later, tomorrow, today, week, month,
                      year, earlier);

} // namespace api

namespace userver::storages::postgres::io {
template <>
struct CppToUserPg<api::TimeFrameType> : EnumMappingBase<api::TimeFrameType> {
  static constexpr userver::storages::postgres::DBTypeName postgres_name =
      "objects.time_frame_e";
  static constexpr userver::utils::TrivialBiMap enumerators =
      uopenapi::enum_helpers::create_enumerator_func<api::TimeFrameType>();
};
} // namespace userver::storages::postgres::io
