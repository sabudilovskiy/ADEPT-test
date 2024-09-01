#pragma once

#include <uopenapi/reflective/schema/appender.hpp>
#include <userver/storages/postgres/io/chrono.hpp>

namespace api{
    using Datetime = userver::storages::postgres::TimePointTz;
}

namespace uopenapi::reflective{
  template <>
  struct schema_appender<api::Datetime, none_requirements>{

    static constexpr std::string_view kNameType = "Datetime";

    static void place_ref_to_type(userver::formats::yaml::ValueBuilder& place){
      std::string result = "#/components/schemas/";
      result += kNameType;
      if (!place.IsObject()) {
          place = userver::formats::yaml::Type::kObject;
      }
      place["$ref"] = result;
    }
    static void place_definition(userver::formats::yaml::ValueBuilder& type_node) {
        if (type_node.IsObject()) {
            return;
        }
        type_node = userver::formats::common::Type::kObject;
        type_node["type"] = "string";
        type_node["format"] = "datetime";
      }

    static void append(schema_view schema, none_requirements){
       if (!schema.is_root()) {
            place_ref_to_type(schema.cur_place);
        }
        std::string name_type{kNameType};
        auto type_node = schema.root["components"]["schemas"][name_type];
        place_definition(type_node);
    }
  };
}