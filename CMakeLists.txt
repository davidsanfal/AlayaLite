cmake_minimum_required(VERSION 3.15...3.31)

# Project definition
set(PROJECT_NAME AlayaLite)
project(${PROJECT_NAME} LANGUAGES CXX)

# Default build type
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE
      Release
      CACHE STRING "Build type" FORCE
  )
endif()

# Include utility functions
include(cmake/PrintSummary.cmake)
include(cmake/Codecov.cmake)

option(ENABLE_COVERAGE "Enable code coverage instrumentation" OFF)
option(BUILD_TESTING "Build tests" OFF)

# ============================================================================
# 1. C++ STANDARD AND COMPILER CONFIGURATION
# ============================================================================

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(MSVC)
  add_compile_options(/EHsc /utf-8 /O2)
else()
  add_compile_options(-Wall -Ofast)
endif()

# ============================================================================
# 1. Dependency Management (Auto Conan Setup)
# ============================================================================
# include(cmake/ConanSetup.cmake)
if(APPLE)
  set(OPENMP_LIBOMP_PATH "")
  if(EXISTS "/opt/homebrew/opt/libomp")
    set(OPENMP_LIBOMP_PATH "/opt/homebrew/opt/libomp")
  elseif(EXISTS "/usr/local/opt/libomp")
    set(OPENMP_LIBOMP_PATH "/usr/local/opt/libomp")
  endif()
  if(OPENMP_LIBOMP_PATH)
    find_library(OpenMP_LIBRARY omp PATHS "${OPENMP_LIBOMP_PATH}/lib" NO_DEFAULT_PATH)
    if(OpenMP_LIBRARY)
      set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp" CACHE STRING "OpenMP C++ flags (libomp on macOS)")
      set(OpenMP_CXX_LIBRARIES "${OpenMP_LIBRARY}" CACHE STRING "OpenMP C++ libraries")
      set(OpenMP_FOUND TRUE CACHE BOOL "OpenMP found via libomp")
    endif()
  endif()
  list(APPEND CMAKE_PREFIX_PATH ${OPENMP_LIBOMP_PATH})
endif()
find_package(concurrentqueue REQUIRED)
find_package(pybind11 REQUIRED)
find_package(spdlog REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(OpenMP REQUIRED)

set(THIRD_PARTY_LIBS spdlog::spdlog_header_only concurrentqueue::concurrentqueue Eigen3::Eigen OpenMP::OpenMP_CXX)

if(UNIX AND NOT APPLE)
  find_package(libcoro REQUIRED)
  list(APPEND THIRD_PARTY_LIBS libcoro::libcoro)
endif()

# ============================================================================
# PROJECT TARGETS
# ============================================================================
include_directories(${CMAKE_SOURCE_DIR}/include)

add_library(${PROJECT_NAME} INTERFACE)
target_include_directories(
  ${PROJECT_NAME} INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>
)
target_link_libraries(${PROJECT_NAME} INTERFACE ${THIRD_PARTY_LIBS})
target_compile_features(${PROJECT_NAME} INTERFACE cxx_std_20)

# ============================================================================
# SUBDIRECTORIES
# ============================================================================
if(BUILD_TESTING)
  include(CTest)
  find_package(GTest)
  set(GTEST_LIBS GTest::gtest GTest::gtest_main)
  add_subdirectory(tests)
endif()

add_subdirectory(python)
print_build_summary()
