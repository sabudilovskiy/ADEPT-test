#include "handler.hpp"

namespace views::group::time {

response GroupByTimeHandler::handle(request) const {
  api::Datetime now(userver::utils::datetime::Now());
  auto groupped = repository_.group_by_time(now);
  response200 resp;
  auto &frames = resp->body.frames;
  frames.reserve(groupped.size());
  for (auto &[key, objs] : groupped) {
    frames.emplace_back(key, std::move(objs));
  }
  return resp;
}

GroupByTimeHandler::GroupByTimeHandler(
    const userver::components::ComponentConfig &cfg,
    const userver::components::ComponentContext &ctx)
    : base(cfg, ctx),
      repository_(ctx.FindComponent<models::basic_object_respository>(
          "object_repository")) {}
} // namespace views::group::time
