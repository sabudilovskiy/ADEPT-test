#pragma once
#include <api/group.hpp>
#include <api/object.hpp>
#include <unordered_map>

namespace models {
struct basic_object_respository {

  template <typename E, typename T = api::Object>
  using Grouped = std::unordered_map<E, std::vector<T>>;
  using DistanceGrouped = Grouped<api::DistanceType, api::ObjectWithDistance>;

  virtual api::Object add_object(const api::NewObject &new_object) = 0;

  virtual Grouped<api::TimeFrameType>
  group_by_time(const api::Datetime &now) const = 0;

  virtual Grouped<std::string> group_by_type(std::size_t N) const = 0;

  virtual Grouped<std::string> group_by_name() const = 0;

  virtual DistanceGrouped
  group_by_distance(const api::Coordinates &coordinates) const = 0;

  virtual std::vector<api::Object> get_all() const = 0;
};
} // namespace models
