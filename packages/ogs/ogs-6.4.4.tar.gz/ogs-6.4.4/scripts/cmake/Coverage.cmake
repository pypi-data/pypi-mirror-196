find_program(FASTCOV_PATH NAMES fastcov fastcov.py)
if(NOT FASTCOV_PATH AND NOT OGS_USE_PIP)
    message(
        FATAL_ERROR "Code coverage requires either fastcov or OGS_USE_PIP=ON."
    )
endif()

# cmake-lint: disable=E1126

# https://github.com/linux-test-project/lcov/pull/125
if(APPLE)
    set(GENHTML_PATH ${PROJECT_BINARY_DIR}/bin/genhtml)
    file(
        DOWNLOAD
        https://raw.githubusercontent.com/linux-test-project/lcov/41d8655951d6898511f98be2a2dbcfbe662f0b17/bin/genhtml
        ${GENHTML_PATH}
    )
    file(
        DOWNLOAD
        https://raw.githubusercontent.com/linux-test-project/lcov/41d8655951d6898511f98be2a2dbcfbe662f0b17/bin/get_version.sh
        ${PROJECT_BINARY_DIR}/bin/get_version.sh
    )
    file(
        CHMOD
        ${GENHTML_PATH}
        ${PROJECT_BINARY_DIR}/bin/get_version.sh
        FILE_PERMISSIONS
        OWNER_READ
        OWNER_WRITE
        OWNER_EXECUTE
    )
endif()

include(CodeCoverage)
append_coverage_compiler_flags()
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Og")

# cmake-lint: disable=C0103
if(NOT FASTCOV_PATH)
    list(APPEND OGS_PYTHON_PACKAGES "fastcov==1.14")
    set(FASTCOV_PATH ${LOCAL_VIRTUALENV_BIN_DIR}/fastcov CACHE INTERNAL "")
endif()

if(DEFINED ENV{CI})
    set(COVERAGE_ADDITIONAL_ARGS SKIP_HTML)
endif()

if(APPLE)
    # System gcov does not work:
    # https://github.com/RPGillespie6/fastcov/issues/36. Search for Homebrew
    # installed gcov (included in gcc package).
    find_program(
        GCOV_PATH NAMES gcov-12 gcov-11 gcov-10 HINTS $ENV{HOMEBREW_PREFIX}/bin
                                                      REQUIRED
    )
endif()

if(OGS_BUILD_TESTING)
    setup_target_for_coverage_fastcov(
        NAME
        testrunner_coverage
        BASE_DIRECTORY
        ${PROJECT_BINARY_DIR}
        EXECUTABLE
        $<TARGET_FILE:testrunner>
        -l
        warn
        --gtest_filter=-GeoLib.SearchNearestPointsInDenseGrid
        DEPENDENCIES
        testrunner
        FASTCOV_ARGS
        --branch-coverage
        --include
        ${PROJECT_SOURCE_DIR}
        ${COVERAGE_ADDITIONAL_ARGS}
        EXCLUDE
        Applications/CLI/
        ProcessLib/
    )
endif()

if(OGS_BUILD_CLI)
    setup_target_for_coverage_fastcov(
        NAME
        ctest_coverage
        BASE_DIRECTORY
        ${PROJECT_BINARY_DIR}
        EXECUTABLE
        ctest
        DEPENDENCIES
        all
        FASTCOV_ARGS
        --branch-coverage
        --include
        ${PROJECT_SOURCE_DIR}
        ${COVERAGE_ADDITIONAL_ARGS}
        EXCLUDE
        Applications/CLI/
        POST_CMD
        perl
        -i
        -pe
        s!${PROJECT_SOURCE_DIR}/!!g
        ctest_coverage.json
        NO_DEMANGLE
    )
endif()

if(UNIX)
    add_custom_target(clean_coverage find . -name '*.gcda' -delete)
endif()

configure_file(
    ${PROJECT_SOURCE_DIR}/scripts/test/generate_coverage_vis_data.in.py
    ${PROJECT_BINARY_DIR}/generate_coverage_vis_data.py @ONLY
)
