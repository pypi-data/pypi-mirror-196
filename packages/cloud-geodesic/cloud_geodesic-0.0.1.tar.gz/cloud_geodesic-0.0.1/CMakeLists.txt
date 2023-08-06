cmake_minimum_required(VERSION 3.10)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS " ${CMAKE_CXX_FLAGS_INIT} -Wall -fPIC")

find_package(Eigen3 REQUIRED)
ADD_DEFINITIONS(-DEIGEN_NO_DEBUG)
include_directories(${EIGEN3_INCLUDE_DIR})

add_subdirectory(matplotplusplus)

include_directories(src)

add_library(fmt src/fmt.cpp)
target_link_libraries(fmt PUBLIC matplot)

add_executable(example "example/main.cpp")
target_link_libraries(example PUBLIC fmt)

add_subdirectory(pybind11)
pybind11_add_module(_cloud_geodesic src/wrapper.cpp)
target_link_libraries(_cloud_geodesic PUBLIC fmt)

set(PIP_INSTALL ON)
if(PIP_INSTALL)
    install(TARGETS _cloud_geodesic DESTINATION .)
endif()
