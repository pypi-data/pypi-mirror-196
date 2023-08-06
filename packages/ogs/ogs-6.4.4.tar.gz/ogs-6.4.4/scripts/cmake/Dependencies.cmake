message(STATUS "┌─ Dependencies.cmake")
list(APPEND CMAKE_MESSAGE_INDENT "│    ")
set(CMAKE_FOLDER ThirdParty)

if(OGS_BUILD_TESTING)
    CPMAddPackage(
        NAME googletest
        GITHUB_REPOSITORY google/googletest
        VERSION ${ogs.minimum_version.gtest}
        GIT_TAG ${ogs.tested_version.gtest}
        OPTIONS "INSTALL_GTEST OFF" "gtest_force_shared_crt ON"
                "BUILD_SHARED_LIBS OFF"
        EXCLUDE_FROM_ALL YES
    )

    CPMAddPackage(
        NAME autocheck
        GITHUB_REPOSITORY ufz/autocheck
        GIT_TAG e388ecbb31c49fc2724c8d0436da313b6edca7fd
        DOWNLOAD_ONLY YES
    )
    if(autocheck_ADDED)
        add_library(autocheck INTERFACE IMPORTED)
        target_include_directories(
            autocheck SYSTEM INTERFACE ${autocheck_SOURCE_DIR}/include
        )
    endif()
endif()

# Check spdlog release for compatible fmt release. fmt may be provided by vtk
# _ext build.
if(NOT TARGET fmt::fmt)
    CPMFindPackage(
        NAME fmt
        GIT_TAG 9.1.0
        GITHUB_REPOSITORY fmtlib/fmt
        EXCLUDE_FROM_ALL YES
    )
endif()
CPMFindPackage(
    NAME spdlog
    GITHUB_REPOSITORY gabime/spdlog
    VERSION 1.11.0
    OPTIONS "BUILD_SHARED_LIBS OFF" "SPDLOG_BUILD_SHARED OFF"
            "SPDLOG_FMT_EXTERNAL_HO 1"
)
if(spdlog_ADDED)
    set_target_properties(
        spdlog
        PROPERTIES INTERFACE_SYSTEM_INCLUDE_DIRECTORIES
                   $<TARGET_PROPERTY:spdlog,INTERFACE_INCLUDE_DIRECTORIES>
    )
endif()

CPMFindPackage(
    NAME tclap
    GITHUB_REPOSITORY ufz/tclap
    VERSION 1.2.4
    GIT_TAG 098dd0fe07a31618f3c2a9f8727bb01c8c5d61e2
    DOWNLOAD_ONLY YES
)
if(tclap_ADDED)
    add_library(tclap INTERFACE IMPORTED)
    target_include_directories(
        tclap SYSTEM INTERFACE ${tclap_SOURCE_DIR}/include
    )
endif()

CPMAddPackage(
    NAME tetgen GITHUB_REPOSITORY ufz/tetgen
    GIT_TAG 603ba181ebfaed38eec88532720e282606009b73
)
if(tetgen_ADDED)
    install(PROGRAMS $<TARGET_FILE:tetgen> DESTINATION bin)
    list(APPEND DISABLE_WARNINGS_TARGETS tet tetgen)
endif()

if(OGS_USE_PYTHON OR OGS_BUILD_PYTHON_MODULE)
    CPMAddPackage(
        NAME pybind11 GITHUB_REPOSITORY pybind/pybind11 VERSION 2.10.3
    )
endif()

if(_build_chemistry_lib)
    CPMAddPackage(
        NAME iphreeqc
        GITHUB_REPOSITORY ufz/iphreeqc
        GIT_TAG b1047d3eb03e7ef1b850231be35acb9c6a2cf345
        DOWNLOAD_ONLY YES
    )
    if(iphreeqc_ADDED)
        include(scripts/cmake/iphreeqc.cmake)
        list(APPEND DISABLE_WARNINGS_TARGETS iphreeqc)
    endif()
endif()

CPMFindPackage(
    NAME Eigen3
    # Error as in
    # https://gitlab.com/gitlab-com/gl-infra/reliability/-/issues/8475
    # GITLAB_REPOSITORY libeigen/eigen
    URL https://gitlab.com/libeigen/eigen/-/archive/${ogs.minimum_version.eigen}/eigen-${ogs.minimum_version.eigen}.tar.gz
    GIT_TAG ${ogs.minimum_version.eigen}
    DOWNLOAD_ONLY YES
)
if(Eigen3_ADDED)
    add_library(Eigen3::Eigen INTERFACE IMPORTED)
    target_include_directories(
        Eigen3::Eigen SYSTEM INTERFACE ${Eigen3_SOURCE_DIR}
                                       ${OpenMP_CXX_INCLUDE_DIRS}
    )
endif()

if(OGS_USE_MFRONT)
    set(CMAKE_REQUIRE_FIND_PACKAGE_TFEL TRUE)
    CPMAddPackage(
        NAME MGIS
        GITHUB_REPOSITORY thelfer/MFrontGenericInterfaceSupport
        GIT_TAG rliv-2.0
        OPTIONS "enable-doxygen-doc OFF" "enable-fortran-bindings OFF"
                "enable-website OFF"
        EXCLUDE_FROM_ALL YES
    )
    if(MGIS_ADDED)
        list(APPEND DISABLE_WARNINGS_TARGETS MFrontGenericInterface)
    endif()
endif()

CPMFindPackage(
    NAME Boost
    VERSION ${ogs.minimum_version.boost}
    URL https://gitlab.opengeosys.org/ogs/libs/boost-subset/-/jobs/187805/artifacts/raw/ogs-boost-${ogs.minimum_version.boost}.tar.gz
)
if(Boost_ADDED)
    add_library(Boost::boost INTERFACE IMPORTED)
    target_include_directories(Boost::boost INTERFACE "${Boost_SOURCE_DIR}")
else()
    target_include_directories(Boost::boost INTERFACE "${Boost_INCLUDE_DIR}")
endif()

CPMFindPackage(
    NAME LibXml2
    GITHUB_REPOSITORY GNOME/libxml2
    VERSION ${ogs.minimum_version.libxml2}
    OPTIONS "BUILD_SHARED_LIBS OFF"
            "LIBXML2_WITH_TESTS OFF"
            "LIBXML2_WITH_PROGRAMS OFF"
            "LIBXML2_WITH_ICONV OFF"
            "LIBXML2_WITH_ICU OFF"
            "LIBXML2_WITH_LZMA OFF"
            "LIBXML2_WITH_PYTHON OFF"
            "LIBXML2_WITH_ZLIB OFF"
    EXCLUDE_FROM_ALL YES
)
if(LibXml2_ADDED)
    add_library(LibXml2::LibXml2 ALIAS LibXml2)
    set(LIBXML2_INCLUDE_DIR ${LibXml2_SOURCE_DIR})
    list(APPEND DISABLE_WARNINGS_TARGETS LibXml2)
endif()

CPMAddPackage(
    NAME xmlpatch
    VERSION 0.4.2
    GIT_REPOSITORY https://gitlab.opengeosys.org/ogs/libs/xmlpatch.git
    OPTIONS "BUILD_SHARED_LIBS OFF"
)

if(OGS_BUILD_SWMM)
    CPMAddPackage(
        NAME SWMMInterface
        GITHUB_REPOSITORY ufz/SwmmInterface
        GIT_TAG 141e05ae1f419918799d7bf9178ebcd97feb1ed3
        OPTIONS "BUILD_SHARED_LIBS OFF"
    )
    if(SWMMInterface_ADDED)
        target_include_directories(
            SwmmInterface SYSTEM PUBLIC ${SWMMInterface_SOURCE_DIR}
        )
        list(APPEND DISABLE_WARNINGS_TARGETS SWMM SwmmInterface)
    endif()
endif()

CPMFindPackage(
    NAME nlohmann_json
    VERSION 3.6.1
    # the git repo is incredibly large, so we download the archived include
    # directory
    URL https://github.com/nlohmann/json/releases/download/v3.6.1/include.zip
    URL_HASH
        SHA256=69cc88207ce91347ea530b227ff0776db82dcb8de6704e1a3d74f4841bc651cf
)
if(nlohmann_json_ADDED)
    add_library(nlohmann_json::nlohmann_json INTERFACE IMPORTED)
    target_include_directories(
        nlohmann_json::nlohmann_json INTERFACE ${nlohmann_json_SOURCE_DIR}
    )
endif()

if(OGS_BUILD_GUI)
    CPMAddPackage(
        NAME rapidxml
        VERSION 1.13
        GITHUB_REPOSITORY ufz/rapidxml
        GIT_TAG 2ae4b2888165a393dfb6382168825fddf00c27b9
        EXCLUDE_FROM_ALL YES
    )
    if(rapidxml_ADDED)
        add_library(rapidxml INTERFACE IMPORTED)
        target_include_directories(rapidxml INTERFACE ${rapidxml_SOURCE_DIR})
    endif()
endif()

if(OGS_BUILD_GUI)
    find_package(Shapelib QUIET)
    if(Shapelib_FOUND)
        add_library(shp INTERFACE IMPORTED)
        target_include_directories(shp INTERFACE ${Shapelib_INCLUDE_DIRS})
        target_link_libraries(shp INTERFACE ${Shapelib_LIBRARIES})
    else()
        CPMAddPackage(
            NAME Shapelib
            GITHUB_REPOSITORY OSGeo/shapelib
            VERSION 1.5.0-dev
            GIT_TAG 21ae8fc16afa15a1b723077b6cec3a9abc592f6a
            EXCLUDE_FROM_ALL YES
        )
        target_include_directories(
            shp INTERFACE $<BUILD_INTERFACE:${Shapelib_SOURCE_DIR}>
        )
    endif()
endif()

if(OGS_USE_CVODE)
    CPMAddPackage(
        NAME CVODE
        GITHUB_REPOSITORY ufz/cvode
        VERSION 2.8.2
        GIT_TAG 42d786bff4f950045d2de941677ecd4432cec855
        OPTIONS "EXAMPLES_ENABLE OFF"
        EXCLUDE_FROM_ALL YES
    )
    if(CVODE_ADDED)
        add_library(CVODE::CVODE INTERFACE IMPORTED)
        target_include_directories(
            CVODE::CVODE INTERFACE ${CVODE_SOURCE_DIR}/include
                                   ${CVODE_BINARY_DIR}/include
        )
        target_link_libraries(
            CVODE::CVODE INTERFACE sundials_cvode_static
                                   sundials_nvecserial_static
        )
    endif()
endif()

# VTK ###
# ~~~
# if(OGS_USE_INSITU)
#     find_package(ParaView REQUIRED)
# endif()
# ~~~
CPMAddPackage(
    NAME exprtk
    GIT_REPOSITORY https://gitlab.opengeosys.org/ogs/libs/exprtk.git
    GIT_TAG 2a5c62b93c9661470e69be572f22d821308b6f61
    DOWNLOAD_ONLY YES
)
if(exprtk_ADDED)
    add_library(exprtk INTERFACE IMPORTED)
    target_include_directories(exprtk SYSTEM INTERFACE ${exprtk_SOURCE_DIR})
endif()

CPMAddPackage(
    NAME range-v3
    GITHUB_REPOSITORY ericniebler/range-v3
    VERSION 0.12.0
    GIT_TAG 0.12.0
    EXCLUDE_FROM_ALL YES
)

CPMFindPackage(
    NAME boost_mp11
    VERSION 1.79.0
    GITHUB_REPOSITORY boostorg/mp11
    GIT_TAG boost-1.79.0
)

if(OGS_BUILD_TESTING OR OGS_BUILD_UTILS)
    CPMAddPackage(
        NAME vtkdiff GITHUB_REPOSITORY ufz/vtkdiff
        GIT_TAG 788100291f73e472febf7e5550eea36ec4be518b
    )
    if(vtkdiff_ADDED)
        install(PROGRAMS $<TARGET_FILE:vtkdiff> DESTINATION bin)
    endif()
endif()

if(OGS_USE_PETSC)
    include(CheckCXXSymbolExists)
    set(CMAKE_REQUIRED_INCLUDES "${HDF5_INCLUDE_DIRS}")
    set(CMAKE_REQUIRED_LIBRARIES "${HDF5_LIBRARIES}")
    check_cxx_symbol_exists(H5Pset_fapl_mpio hdf5.h HAVE_H5Pset_fapl_mpio)
    unset(CMAKE_REQUIRED_INCLUDES)
    if(NOT HAVE_H5Pset_fapl_mpio)
        message(FATAL_ERROR "HDF5 was not build with MPI support! "
                            "(Enable with HDF5_ENABLE_PARALLEL)"
        )
    endif()
endif()

# Does not compile in Debug-mode, see #3175.
if(CMAKE_BUILD_TYPE MATCHES "Rel" AND OGS_BUILD_TESTING)
    set(XDMF_LIBNAME OgsXdmf CACHE STRING "")
    CPMAddPackage(
        NAME xdmf
        VERSION 3.0.0
        GIT_REPOSITORY https://gitlab.opengeosys.org/ogs/xdmflib.git
        GIT_TAG 92a851f1acb87ad5367eb62f9b97785bedb700bb
        OPTIONS "XDMF_LIBNAME OgsXdmf" "CMAKE_MACOSX_RPATH ON"
                "HDF5_C_INCLUDE_DIR ${HDF5_INCLUDE_DIRS}"
        EXCLUDE_FROM_ALL YES
    )
    if(xdmf_ADDED)
        target_include_directories(
            OgsXdmf PUBLIC ${xdmf_SOURCE_DIR} ${xdmf_BINARY_DIR}
        )

        target_link_libraries(OgsXdmf Boost::boost)
        target_include_directories(
            OgsXdmfCore PUBLIC ${xdmf_SOURCE_DIR}/core ${xdmf_BINARY_DIR}/core
            PRIVATE ${xdmf_SOURCE_DIR}/CMake/VersionSuite
        )
        target_link_libraries(
            OgsXdmfCore PUBLIC Boost::boost LibXml2::LibXml2 ${HDF5_LIBRARIES}
        )

        set_target_properties(
            OgsXdmf OgsXdmfCore
            PROPERTIES RUNTIME_OUTPUT_DIRECTORY
                       ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}
                       LIBRARY_OUTPUT_DIRECTORY
                       ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}
                       ARCHIVE_OUTPUT_DIRECTORY
                       ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}
        )
        if(BUILD_SHARED_LIBS)
            install(TARGETS OgsXdmf OgsXdmfCore
                    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
            )
        endif()
        list(APPEND DISABLE_WARNINGS_TARGETS OgsXdmf OgsXdmfCore)
    endif()
endif()

CPMAddPackage(
    NAME GroupSourcesByFolder.cmake
    GITHUB_REPOSITORY TheLartians/GroupSourcesByFolder.cmake VERSION 1.0
)

if(OGS_BUILD_UTILS)
    CPMAddPackage(
        NAME metis
        GIT_REPOSITORY https://gitlab.opengeosys.org/ogs/libs/metis.git
        GIT_TAG d98094f42d0faf9d0e06eb149c870fb714623ecc
        VERSION 5.1.0
        DOWNLOAD_ONLY YES
    )
    include(${PROJECT_SOURCE_DIR}/scripts/cmake/MetisSetup.cmake)
endif()

# Disable warnings
if(WIN32 AND VTK_ADDED)
    list(APPEND DISABLE_WARNINGS_TARGETS vtksys)
endif()
foreach(target ${DISABLE_WARNINGS_TARGETS})
    target_compile_options(
        ${target} PRIVATE $<$<CXX_COMPILER_ID:Clang,AppleClang,GNU>:-w>
                          $<$<CXX_COMPILER_ID:MSVC>:/W0>
    )
endforeach()

# Hack: Disable tests from dependencies
configure_file(
    ${PROJECT_SOURCE_DIR}/scripts/cmake/test/CTestCustom.in.cmake
    ${PROJECT_BINARY_DIR}/CTestCustom.cmake @ONLY
)

find_program(CLANG_FORMAT_PROGRAM clang-format)
find_program(CMAKE_FORMAT_PROGRAM cmake-format)

if(CLANG_FORMAT_PROGRAM OR CMAKE_FORMAT_PROGRAM)
    if(NOT CMAKE_FORMAT_PROGRAM)
        set(_skip_cmake "FORMAT_SKIP_CMAKE YES")
    endif()
    CPMAddPackage(
        NAME Format.cmake
        VERSION 1.7.0
        GITHUB_REPOSITORY TheLartians/Format.cmake
        OPTIONS
            ${_skip_cmake}
            "CMAKE_FORMAT_EXCLUDE scripts/cmake/CPM.cmake|.*/Tests.cmake|scripts/cmake/jedbrown/.*|scripts/cmake/conan/conan.cmake|scripts/cmake/vector-of-bool/.*"
    )
endif()

# Third-party licenses
cpm_licenses_create_disclaimer_target(
    write-licenses "${PROJECT_BINARY_DIR}/third_party_licenses_cpm.txt"
    "${CPM_PACKAGES}"
)

unset(CMAKE_FOLDER)
list(POP_BACK CMAKE_MESSAGE_INDENT)
message(STATUS "└─ End Dependencies.cmake")
