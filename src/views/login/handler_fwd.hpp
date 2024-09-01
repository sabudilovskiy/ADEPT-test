#pragma once
#include <userver/components/component_list.hpp>

namespace views::login{
    struct handler;
    void Append(userver::components::ComponentList& componentList);
}
