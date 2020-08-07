cmake_minimum_required(VERSION 2.6 FATAL_ERROR)

enable_language( CXX )

project(duriansat)
SET(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

find_program(CCACHE_FOUND ccache)
if(CCACHE_FOUND)
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
    set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK ccache)
    message(STATUS "Ok, CCache found!")
endif(CCACHE_FOUND)

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

add_compile_options("-O3")
add_compile_options("-g")


# -----------------------------------------------------------------------------
# Add GIT version

find_program (GIT_EXECUTABLE git)
if (GIT_EXECUTABLE)
  include(GetGitRevisionDescription)
  get_git_head_revision(GIT_REFSPEC GIT_SHA1)
  MESSAGE(STATUS "GIT hash found: ${GIT_SHA1}")
  add_definitions( -DVERSION="${GIT_SHA1}" )
else()
  set(GIT_SHA "GIT-hash-notfound")
endif()


#--------------------------------------------------------------------------------------------------
# Dependencies:

find_package(ZLIB)
include_directories(${ZLIB_INCLUDE_DIR})
include_directories(${duriansat_SOURCE_DIR})

#--------------------------------------------------------------------------------------------------
# Compile flags:

add_definitions(-D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS)

#--------------------------------------------------------------------------------------------------
# Build Targets:

set(DURIANSAT_LIB_SOURCES
    utils/Options.cc
    utils/System.cc
    utils/terminal.cc
    core/Solver.cc
    simp/SimpSolver.cc)

set(CMAKE_CXX_FLAGS "-O3")


add_library(duriansat-lib-static STATIC ${DURIANSAT_LIB_SOURCES})
add_library(duriansat-lib-shared SHARED ${DURIANSAT_LIB_SOURCES})

target_link_libraries(duriansat-lib-shared ${ZLIB_LIBRARY})
target_link_libraries(duriansat-lib-static ${ZLIB_LIBRARY})

add_executable(duriansat_simp simp/Main.cc)

if(STATIC_BINARIES)
  target_link_libraries(duriansat_simp duriansat-lib-static -static)
else()
  target_link_libraries(duriansat_simp duriansat-lib-shared)
endif()

set_target_properties(duriansat-lib-static PROPERTIES OUTPUT_NAME "duriansat")
set_target_properties(duriansat-lib-shared
  PROPERTIES
    OUTPUT_NAME "duriansat"
    VERSION ${DURIANSAT_VERSION}
    SOVERSION ${DURIANSAT_SOVERSION})

set_target_properties(duriansat_simp       PROPERTIES OUTPUT_NAME "duriansat")

#--------------------------------------------------------------------------------------------------
# Installation targets:

install(TARGETS duriansat-lib-static duriansat-lib-shared duriansat_simp
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(DIRECTORY mtl utils core simp
        DESTINATION include/duriansat
        FILES_MATCHING PATTERN "*.h")
