#include "handler.hpp"

namespace views::group::type {

response GroupTypeHandler::handle(request req) const {
  auto groupped = repository_.group_by_type(req.N);
  response200 resp;
  auto &groups = resp->body.groups;
  groups.reserve(groupped.size());
  for (auto &[key, value] : groupped) {
    groups.emplace_back(Group{key, std::move(value)});
  }
  return resp;
}

GroupTypeHandler::GroupTypeHandler(
    const userver::components::ComponentConfig &cfg,
    const userver::components::ComponentContext &ctx)
    : base(cfg, ctx),
      repository_(ctx.FindComponent<models::basic_object_respository>(
          "object_repository")) {}
} // namespace views::group::type
