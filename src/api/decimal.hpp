#pragma once

#include <uopenapi/reflective/schema/appender.hpp>
#include <userver/decimal64/decimal64.hpp>

namespace api {
using Decimal = userver::decimal64::Decimal<8>;
}

namespace uopenapi::reflective {
template <> struct schema_appender<api::Decimal, none_requirements> {

  static constexpr std::string_view kNameType = "Decimal";

  static void place_ref_to_type(userver::formats::yaml::ValueBuilder &place) {
    std::string result = "#/components/schemas/";
    result += kNameType;
    if (!place.IsObject()) {
      place = userver::formats::yaml::Type::kObject;
    }
    place["$ref"] = result;
  }
  static void
  place_definition(userver::formats::yaml::ValueBuilder &type_node) {
    if (type_node.IsObject()) {
      return;
    }
    type_node = userver::formats::common::Type::kObject;
    type_node["type"] = "string";
    type_node["description"] = "Decimal number like 0.52131231";
  }

  static void append(schema_view schema, none_requirements) {
    if (!schema.is_root()) {
      place_ref_to_type(schema.cur_place);
    }
    std::string name_type{kNameType};
    auto type_node = schema.root["components"]["schemas"][name_type];
    place_definition(type_node);
  }
};
} // namespace uopenapi::reflective
