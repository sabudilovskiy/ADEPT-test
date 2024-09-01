#pragma once
#include <uopenapi/all.hpp>
#include <userver/decimal64/decimal64.hpp>
#include <userver/storages/postgres/io/chrono.hpp>
#include <userver/storages/postgres/io/type_mapping.hpp>
#include <api/decimal.hpp>
#include <api/datetime.hpp>

namespace api {

struct Coordinates {
  Decimal x;
  Decimal y;
};

struct NewObject {
  std::string name;
  std::string type_name;
  Coordinates coordinates;
  boost::uuids::uuid token_idempotency;
};

struct Object {
  boost::uuids::uuid object_id;
  std::string name;
  std::string type_name;
  Coordinates coordinates;
  Datetime created_at;
};

} // namespace api


namespace userver::storages::postgres::io
{
template <>
struct CppToUserPg<api::NewObject>
{
    static constexpr DBTypeName postgres_name = "objects.new_object_t_v1";
};

template <>
struct CppToUserPg<api::Coordinates>
{
    static constexpr DBTypeName postgres_name = "objects.coordinates_t";
};

}  // namespace userver::storages::postgres::io