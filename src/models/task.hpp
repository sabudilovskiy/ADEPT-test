#pragma once
#include <boost/uuid/uuid.hpp>
#include <string>
#include <optional>
#include <uopenapi/enum/declare.hpp>
#include <uopenapi/reflective/requirements/requirements_field.hpp>
#include <uopenapi/reflective/requirements/string/string_requirements.hpp>

namespace models{
    UOPENAPI_DECLARE_ENUM(TaskStatus, int, completed, incomplete);

    struct Task{
        boost::uuids::uuid id;
        std::string text;
        std::optional<std::string> description;
        TaskStatus status;
        std::optional<std::string> due_date;
    };
}
REQUIREMENTS_CE_UOPENAPI(models::Task, due_date) = string_requirements<"date-time">{};
