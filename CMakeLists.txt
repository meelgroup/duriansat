cmake_minimum_required(VERSION 2.6 FATAL_ERROR)

project(maplesat)

#--------------------------------------------------------------------------------------------------
# Configurable options:

option(STATIC_BINARIES "Link binaries statically." ON)
option(USE_SORELEASE   "Use SORELEASE in shared library filename." ON)


include(CheckCXXCompilerFlag)
macro(add_cxx_flag_if_supported flagname)
  check_cxx_compiler_flag("${flagname}" HAVE_FLAG_${flagname})

  if(HAVE_FLAG_${flagname})
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${flagname}" )
  endif()
endmacro()

add_cxx_flag_if_supported("-Wall")
add_cxx_flag_if_supported("-Wextra")
add_cxx_flag_if_supported("-Wunused")
add_cxx_flag_if_supported("-Wsign-compare")
if (NOT CMAKE_BUILD_TYPE STREQUAL "Release")
    add_cxx_flag_if_supported("-fno-omit-frame-pointer")
endif()
add_cxx_flag_if_supported("-Wtype-limits")
add_cxx_flag_if_supported("-Wuninitialized")
add_cxx_flag_if_supported("-Wno-deprecated")
add_cxx_flag_if_supported("-Wstrict-aliasing")
add_cxx_flag_if_supported("-Wpointer-arith")
add_cxx_flag_if_supported("-Wheader-guard")
add_cxx_flag_if_supported("-Wpointer-arith")
add_cxx_flag_if_supported("-Wformat-nonliteral")
add_cxx_flag_if_supported("-Winit-self")
add_cxx_flag_if_supported("-Wparentheses")
add_cxx_flag_if_supported("-Wunreachable-code")
add_cxx_flag_if_supported("-ggdb3")

#--------------------------------------------------------------------------------------------------
# Dependencies:

find_package(ZLIB)
include_directories(${ZLIB_INCLUDE_DIR})
include_directories(${maplesat_SOURCE_DIR})

#--------------------------------------------------------------------------------------------------
# Compile flags:

add_definitions(-D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS)

#--------------------------------------------------------------------------------------------------
# Build Targets:

set(MAPLESAT_LIB_SOURCES
    utils/Options.cc
    utils/System.cc
    core/Solver.cc
    simp/SimpSolver.cc)

set(CMAKE_CXX_FLAGS "-O3")

# Get the current working branch
execute_process(
  COMMAND git rev-parse --abbrev-ref HEAD
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  OUTPUT_VARIABLE GIT_BRANCH
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Get the latest abbreviated commit hash of the working branch
execute_process(
  COMMAND git log -1 --format=%h
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  OUTPUT_VARIABLE GIT_COMMIT_HASH
  OUTPUT_STRIP_TRAILING_WHITESPACE
)


set(VERSION "${GIT_COMMIT_HASH}")


add_library(maplesat-lib-static STATIC ${MAPLESAT_LIB_SOURCES})
add_library(maplesat-lib-shared SHARED ${MAPLESAT_LIB_SOURCES})

target_link_libraries(maplesat-lib-shared ${ZLIB_LIBRARY})
target_link_libraries(maplesat-lib-static ${ZLIB_LIBRARY})

add_executable(maplesat_core core/Main.cc)
add_executable(maplesat_simp simp/Main.cc)

if(STATIC_BINARIES)
  target_link_libraries(maplesat_core maplesat-lib-static)
  target_link_libraries(maplesat_simp maplesat-lib-static)
else()
  target_link_libraries(maplesat_core maplesat-lib-shared)
  target_link_libraries(maplesat_simp mapleat-lib-shared)
endif()

set_target_properties(maplesat-lib-static PROPERTIES OUTPUT_NAME "maplesat")
set_target_properties(maplesat-lib-shared
  PROPERTIES
    OUTPUT_NAME "maplesat"
    VERSION ${MAPLESAT_VERSION}
    SOVERSION ${MAPLESAT_SOVERSION})

set_target_properties(maplesat_simp       PROPERTIES OUTPUT_NAME "maplesat")

#--------------------------------------------------------------------------------------------------
# Installation targets:

install(TARGETS maplesat-lib-static maplesat-lib-shared maplesat_core maplesat_simp
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(DIRECTORY mtl utils core simp
        DESTINATION include/maplesat
        FILES_MATCHING PATTERN "*.h")
