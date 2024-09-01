#pragma once
#include <api/object.hpp>
#include <models/basic_object_repository.hpp>
#include <uopenapi/components/openapi_handler.hpp>
#include <userver/formats/parse/boost_uuid.hpp>
#include <userver/formats/serialize/boost_uuid.hpp>
#include <userver/formats/serialize/common_containers.hpp>

namespace views::group::type {
struct request {
  std::size_t N;
};

struct Group {
  std::string type;
  std::vector<api::Object> objects;
};

struct ok_response_body {
  std::vector<Group> groups;
};

struct ok_response {
  ok_response_body body;
};

using response200 = uopenapi::http::response<ok_response, 200>;

using base = uopenapi::components::openapi_handler<request, response200>;
using response = base::response;
struct GroupTypeHandler : base {
  static constexpr std::string_view kName = "group-type-handler";

  GroupTypeHandler(const userver::components::ComponentConfig &cfg,
                   const userver::components::ComponentContext &ctx);

  response handle(request req) const override;

private:
  models::basic_object_respository &repository_;
};
} // namespace views::group::type
