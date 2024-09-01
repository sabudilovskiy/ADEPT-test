#pragma once
#include <api/object.hpp>

namespace models {
struct basic_object_respository {
  virtual api::Object add_object(const api::NewObject& new_object) = 0;
};
} // namespace models
