#include "handler.hpp"

namespace views::group::name {

response GroupNameHandler::handle(request) const {
  auto groupped = repository_.group_by_name();
  response200 resp;
  auto &groups = resp->body.groups;
  groups.reserve(groupped.size());
  for (auto &[key, value] : groupped) {
    groups.emplace_back(Group{key, std::move(value)});
  }
  return resp;
}

GroupNameHandler::GroupNameHandler(
    const userver::components::ComponentConfig &cfg,
    const userver::components::ComponentContext &ctx)
    : base(cfg, ctx),
      repository_(ctx.FindComponent<models::basic_object_respository>(
          "object_repository")) {}
} // namespace views::group::name
