#pragma once
#include "userver/fs/blocking/write.hpp"
#include <uopenapi/components/schema/schema_storage.hpp>
#include <userver/components/component_context.hpp>

namespace components {
struct SchemaFileDistributor
    : public userver::components::LoggableComponentBase {
  static constexpr std::string_view kName = "schema-file-distributor";
  SchemaFileDistributor(const userver::components::ComponentConfig &cfg,
                        const userver::components::ComponentContext &ctx)
      : userver::components::LoggableComponentBase(cfg, ctx),
        schema_storage_(
            ctx.FindComponent<uopenapi::components::schema_storage>()) {}

  void OnAllComponentsLoaded() override {
    auto schema = schema_storage_.get_schema().v;
    std::string str = ToString(schema.ExtractValue());
    userver::fs::blocking::RewriteFileContents("api.yaml", str);
  }

private:
  uopenapi::components::schema_storage &schema_storage_;
};
} // namespace components
