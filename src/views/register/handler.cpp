#include "handler.hpp"

namespace views::Register{
    void Append(userver::components::ComponentList& componentList){
        componentList.Append<handler>();
    }
}
