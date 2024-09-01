#pragma once
#include <api/object.hpp>
#include <models/basic_object_repository.hpp>
#include <uopenapi/components/openapi_handler.hpp>
#include <userver/formats/parse/boost_uuid.hpp>
#include <userver/formats/serialize/boost_uuid.hpp>

namespace views::object_post {
struct request {
  api::NewObject body;
};
struct ok_response {
  api::Object body;
};
using response200 = uopenapi::http::response<ok_response, 200>;

using base = uopenapi::components::openapi_handler<request, response200>;
using response = base::response;
struct AddObjectHandler : base {
  static constexpr std::string_view kName = "add_object_handler";

  AddObjectHandler(const userver::components::ComponentConfig &cfg,
                   const userver::components::ComponentContext &ctx);

  response handle(request req) const override;

private:
  models::basic_object_respository &repository_;
};
} // namespace views::object_post
