#include <uopenapi/components/schema/schema_http_distributor.hpp>
#include <uopenapi/components/schema/schema_storage.hpp>
#include <userver/clients/dns/component.hpp>
#include <userver/clients/http/component.hpp>
#include <userver/components/minimal_server_component_list.hpp>
#include <userver/server/handlers/ping.hpp>
#include <userver/server/handlers/tests_control.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/testsuite/testsuite_support.hpp>
#include <userver/utils/daemon_run.hpp>
#include <views/object/post/handler.hpp>
#include <models/pg_object_repository.hpp>

int main(int argc, char *argv[]) {
  auto component_list = userver::components::MinimalServerComponentList()
                            .Append<userver::server::handlers::Ping>()
                            .Append<userver::components::TestsuiteSupport>()
                            .Append<userver::components::HttpClient>()
                            .Append<userver::clients::dns::Component>()
                            .Append<userver::server::handlers::TestsControl>();
  component_list.Append<uopenapi::components::schema_storage>();
  component_list.Append<uopenapi::components::schema_http_distributor>();
  component_list.Append<userver::components::Postgres>("objects_db");
  component_list.Append<views::object_post::AddObjectHandler>();
  component_list.Append<models::pg_object_respository>("object_repository");

  return userver::utils::DaemonMain(argc, argv, component_list);
}