#pragma once
#include <api/datetime.hpp>
#include <api/decimal.hpp>
#include <uopenapi/all.hpp>
#include <userver/decimal64/decimal64.hpp>
#include <userver/storages/postgres/io/chrono.hpp>
#include <userver/storages/postgres/io/type_mapping.hpp>

namespace api {

struct Coordinates {
  Decimal x;
  Decimal y;
};

struct NewObject {
  std::string name;
  std::string type_name;
  Coordinates coordinates;
  Datetime created_at;
  boost::uuids::uuid token_idempotency;
};

struct Object {
  boost::uuids::uuid object_id;
  std::string name;
  std::string type_name;
  Coordinates coordinates;
  Datetime created_at;
};

struct ObjectWithDistance {
  Object object;
  double distance;
};

} // namespace api

namespace userver::storages::postgres::io {
template <> struct CppToUserPg<api::NewObject> {
  static constexpr DBTypeName postgres_name = "objects.new_object_t_v1";
};

template <> struct CppToUserPg<api::Object> {
  static constexpr DBTypeName postgres_name = "objects.object_t_v1";
};

template <> struct CppToUserPg<api::Coordinates> {
  static constexpr DBTypeName postgres_name = "objects.coordinates_t";
};

} // namespace userver::storages::postgres::io
