#include "handler.hpp"

namespace views::object_post {

response AddObjectHandler::handle(request req) const {
    response200 resp;
    resp->body = repository_.add_object(req.body);
    return resp;
}
AddObjectHandler::AddObjectHandler(
    const userver::components::ComponentConfig &cfg,
    const userver::components::ComponentContext &ctx)
    : base(cfg, ctx), repository_(ctx.FindComponent<models::basic_object_respository>("object_repository")) {
      
    }
} // namespace views::object_post