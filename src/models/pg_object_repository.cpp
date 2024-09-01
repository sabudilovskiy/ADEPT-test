#include "pg_object_repository.hpp"
#include "codegen/sql.hpp"
#include <codecvt>
#include <locale>
#include <ranges>
#include <regex>
#include <uopenapi/enum_helpers/all.hpp>
#include <userver/storages/postgres/cluster.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/storages/postgres/io/composite_types.hpp>
#include <userver/utils/datetime.hpp>
namespace models {

namespace {

template <typename E> using Grouped = basic_object_respository::Grouped<E>;

using DistanceGrouped = basic_object_respository::DistanceGrouped;

// TODO: поправить это говно
bool starts_with_cyrillic(const std::string &str, std::string &first_letter) {
  if (str.empty()) {
    return false;
  }
  std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
  std::wstring wstr = converter.from_bytes(str);

  if (!wstr.empty() && ((wstr[0] >= L'А' && wstr[0] <= L'я') ||
                        wstr[0] == L'Ё' || wstr[0] == L'ё')) {
    first_letter = converter.to_bytes(tolower(wstr[0]));
    return true;
  }
  return false;
}

double distance(const api::Coordinates &lhs, const api::Coordinates &rhs) {
  auto l_x = lhs.x.ToDoubleInexact();
  auto l_y = lhs.y.ToDoubleInexact();
  auto r_x = rhs.x.ToDoubleInexact();
  auto r_y = rhs.y.ToDoubleInexact();
  return sqrt((l_x - r_x) * (l_x - r_x) + (l_y - r_y) * (l_y - r_y));
}

api::DistanceType GetDistanceType(double dist) {
  if (dist < 100) {
    return api::DistanceType::hundred;
  }
  if (dist < 1000) {
    return api::DistanceType::thousand;
  }
  if (dist < 10000) {
    return api::DistanceType::ten_thousand;
  }
  return api::DistanceType::far;
}

} // namespace

pg_object_respository::pg_object_respository(
    const userver::components::ComponentConfig &cfg,
    const userver::components::ComponentContext &ctx)
    : userver::components::LoggableComponentBase(cfg, ctx) {
  ptr = ctx.FindComponent<userver::components::Postgres>("objects_db")
            .GetCluster();
}

api::Object
pg_object_respository::add_object(const api::NewObject &new_object) {
  auto result =
      ptr->Execute(userver::storages::postgres::ClusterHostType::kMaster,
                   sql::add_object, new_object);
  return result.AsSingleRow<api::Object>(userver::storages::postgres::kRowTag);
}

void AppendPgObjectRepository(userver::components::ComponentList &list) {
  list.Append<pg_object_respository>("object_repository");
}

Grouped<api::TimeFrameType>
pg_object_respository::group_by_time(const api::Datetime &now) const {
  auto pg_res =
      ptr->Execute(userver::storages::postgres::ClusterHostType::kMaster,
                   sql::group_by_time, now);

  Grouped<api::TimeFrameType> result;

  for (auto &row : pg_res) {
    auto [val, e] = row.As<std::tuple<api::Object, api::TimeFrameType>>(
        userver::storages::postgres::kRowTag);
    auto [it, _] = result.try_emplace(e);
    it->second.emplace_back(std::move(val));
  }

  return result;
}

Grouped<std::string> pg_object_respository::group_by_type(std::size_t N) const {
  auto objs = get_all();
  Grouped<std::string> result;
  for (auto &obj : objs) {
    auto [it, emplaced] =
        result.try_emplace(obj.type_name, std::vector<api::Object>{});
    it->second.emplace_back(std::move(obj));
  }

  auto comp_obj = [](const api::Object &l, const api::Object &r) {
    return l.name < r.name;
  };

  std::vector<api::Object> various;
  for (auto it = result.begin(); it != result.end();) {
    auto &[key, value] = *it;
    if (value.size() <= N) {
      std::move(value.begin(), value.end(), std::back_inserter(various));
      it = result.erase(it);
    } else {
      std::ranges::sort(value, comp_obj);
      it++;
    }
  }
  auto [it, emplaced] = result.try_emplace("разное", std::move(various));
  if (!emplaced) {
    it->second.reserve(it->second.size() + various.size());
    std::move(various.begin(), various.end(), std::back_inserter(it->second));
  }
  std::ranges::sort(it->second, comp_obj);
  return result;
}

std::vector<api::Object> pg_object_respository::get_all() const {
  auto pg_res = ptr->Execute(
      userver::storages::postgres::ClusterHostType::kMaster, sql::get_all);
  return pg_res.AsContainer<std::vector<api::Object>>(
      userver::storages::postgres::kRowTag);
}

Grouped<std::string> pg_object_respository::group_by_name() const {
  auto objs = get_all();
  Grouped<std::string> result;
  for (auto &obj : objs) {
    std::string first_letter;
    if (starts_with_cyrillic(obj.name, first_letter)) {
      auto [it, emplaced] =
          result.try_emplace(first_letter, std::vector<api::Object>{});
      it->second.emplace_back(std::move(obj));
    } else {
      auto [it, emplaced] = result.try_emplace("#", std::vector<api::Object>{});
      it->second.emplace_back(std::move(obj));
    }
  }
  for (auto &[_, value] : result) {
    std::ranges::sort(value, [](const api::Object &l, const api::Object &r) {
      return l.name < r.name;
    });
  }
  return result;
}

DistanceGrouped pg_object_respository::group_by_distance(
    const api::Coordinates &coordinates) const {
  auto objs = get_all();
  DistanceGrouped result;
  for (auto &obj : objs) {
    auto dist = distance(coordinates, obj.coordinates);
    auto [it, _] = result.try_emplace(GetDistanceType(dist));
    it->second.emplace_back(
        api::ObjectWithDistance{.object = std::move(obj), .distance = dist});
  }
  for (auto &[key, value] : result) {
    std::ranges::sort(value,
                      [](auto &l, auto &r) { return l.distance < r.distance; });
  }
  return result;
}
} // namespace models
