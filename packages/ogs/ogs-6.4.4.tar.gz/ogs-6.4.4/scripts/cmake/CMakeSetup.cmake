# Disallow in-source builds as the git project cluttered with generated files
# probably confuses people. source/build* is still allowed!
if("${PROJECT_SOURCE_DIR}" STREQUAL "${PROJECT_BINARY_DIR}")
    message(
        FATAL_ERROR
            "In-source builds are not allowed!\n"
            "Make sure to remove CMakeCache.txt and CMakeFiles/ "
            "from the source directory!"
    )
endif()

# Set additional CMake modules path
CPMAddPackage(
    NAME cmake-modules
    GITHUB_REPOSITORY bilke/cmake-modules
    GIT_TAG d98828f54f6974717798e63195cfbf08fe2daad0
    DOWNLOAD_ONLY YES
)
# To be replaced later. See
# https://gitlab.kitware.com/cmake/cmake/-/issues/22831
CPMAddPackage(
    NAME findmkl_cmake
    GITHUB_REPOSITORY bilke/findmkl_cmake
    GIT_TAG ee49c4f973f66bb7bfd644658d14e43459f557fa
    DOWNLOAD_ONLY YES
)
CPMAddPackage(
    # TODO: VERSION 0.0.7 when
    # https://github.com/cpm-cmake/CPMLicenses.cmake/pull/6 is merged
    NAME CPMLicenses.cmake
    GITHUB_REPOSITORY bilke/CPMLicenses.cmake
    GIT_TAG 71b1512d81e6294a15aafd78df431ce2dd64a805
)
set(CMAKE_MODULE_PATH
    ${CMAKE_MODULE_PATH}
    "${PROJECT_SOURCE_DIR}/scripts/cmake"
    "${PROJECT_SOURCE_DIR}/scripts/cmake/jedbrown"
    "${PROJECT_SOURCE_DIR}/scripts/cmake/vector-of-bool"
    "${findmkl_cmake_SOURCE_DIR}/cmake"
    "${cmake-modules_SOURCE_DIR}"
)

list(
    APPEND
    CMAKE_PREFIX_PATH
    $ENV{HOMEBREW_ROOT} # Homebrew package manager on Mac OS
    $ENV{CMAKE_LIBRARY_SEARCH_PATH} # Environment variable, Windows
    ${CMAKE_LIBRARY_SEARCH_PATH}
) # CMake option, Windows

# Load additional modules
include(GNUInstallDirs)
include(ProcessorCount)
ProcessorCount(NUM_PROCESSORS)
set(NUM_PROCESSORS ${NUM_PROCESSORS} CACHE STRING "Processor count")

# Check if this project is included in another
if(NOT PROJECT_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    set(_IS_SUBPROJECT ON CACHE INTERNAL "" FORCE)
    set(OGS_BUILD_CLI OFF CACHE BOOL "" FORCE)
endif()

if((NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
   OR (NOT CMAKE_BUILD_TYPE AND MSVC AND OGS_USE_CONAN)
)
    message(STATUS "Setting build type to 'Debug' as none was specified.")
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the type of build." FORCE)
    set_property(
        CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel"
                                        "RelWithDebInfo"
    )
endif()

# Get the hostname
site_name(HOSTNAME)

if(BUILD_SHARED_LIBS OR OGS_BUILD_PYTHON_MODULE)
    # When static libraries are used in some shared libraries it is required
    # that also the static libraries have position independent code.
    set(CMAKE_POSITION_INDEPENDENT_CODE TRUE)

    # Enable Windows DLL support.
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()
