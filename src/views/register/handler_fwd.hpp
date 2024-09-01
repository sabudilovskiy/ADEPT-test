#pragma once
#include <userver/components/component_list.hpp>

namespace views::Register{
    struct handler;
    void Append(userver::components::ComponentList& componentList);
}
