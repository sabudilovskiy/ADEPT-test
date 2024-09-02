cmake_minimum_required(VERSION 3.20)
project(service)
set(CMAKE_CXX_STANDARD 20)

set(openapi-extension-userver_BUILD_UNIT_TESTS false)
set(openapi-extension-userver_BUILD_TEST_SERVICES false)
set(openapi-extension-userver_SETUP_ENV OFF)
set(USERVER_FEATURE_POSTGRESQL ON)

enable_testing()

include(FetchContent)
FetchContent_Declare(
        uopenapi
        GIT_REPOSITORY https://github.com/sabudilovskiy/userver-openapi-extension
        GIT_TAG "da3a00a1c6b49a9a83522e183cc2d856f69efb18"
)
FetchContent_MakeAvailable(uopenapi)

userver_setup_environment()

CreateTrivialPart(
        name "src"
        path "/src"
)

target_link_libraries(${src_module} PUBLIC openapi-extension-userver_library)

add_executable(service service/main.cpp)

target_link_libraries(service PUBLIC ${src_module})

include(UserverTestsuite)
userver_testsuite_add_simple()