/**
 * \file
 * \copyright
 * Copyright (c) 2012-2023, OpenGeoSys Community (http://www.opengeosys.org)
 *            Distributed under a Modified BSD License.
 *              See accompanying file LICENSE.txt or
 *              http://www.opengeosys.org/project/license
 *
 */

#include "CreateOutputConfig.h"

#include <map>

#include "BaseLib/Algorithm.h"
#include "BaseLib/ConfigTree.h"

namespace ProcessLib
{
OutputConfig createOutputConfig(const BaseLib::ConfigTree& config)
{
    OutputConfig output_config;

    output_config.output_type = [](auto output_type)
    {
        try
        {
            const std::map<std::string, OutputType> outputType_to_enum = {
                {"VTK", OutputType::vtk}, {"XDMF", OutputType::xdmf}};
            auto type = outputType_to_enum.at(output_type);

            return type;
        }
        catch (std::out_of_range&)
        {
            OGS_FATAL(
                "No supported file type provided. Read `{:s}' from <output><type> \
                in prj File. Supported: VTK, XDMF.",
                output_type);
        }
        //! \ogs_file_param{prj__time_loop__output__type}
    }(config.getConfigParameter<std::string>("type"));

    output_config.prefix =
        //! \ogs_file_param{prj__time_loop__output__prefix}
        config.getConfigParameter<std::string>("prefix", "{:meshname}");

    output_config.suffix =
        //! \ogs_file_param{prj__time_loop__output__suffix}
        config.getConfigParameter<std::string>("suffix",
                                               "_ts_{:timestep}_t_{:time}");

    output_config.compress_output =
        //! \ogs_file_param{prj__time_loop__output__compress_output}
        config.getConfigParameter("compress_output", true);

    auto const hdf =
        //! \ogs_file_param{prj__time_loop__output__hdf}
        config.getConfigSubtreeOptional("hdf");

    output_config.number_of_files = [&hdf]() -> unsigned int
    {
        if (hdf)
        {
            //! \ogs_file_param{prj__time_loop__output__hdf__number_of_files}
            return hdf->getConfigParameter<unsigned int>("number_of_files");
        }
        return 1;
    }();

    output_config.data_mode =
        //! \ogs_file_param{prj__time_loop__output__data_mode}
        config.getConfigParameter<std::string>("data_mode", "Appended");

    // Construction of output times
    auto& repeats_each_steps = output_config.repeats_each_steps;

    //! \ogs_file_param{prj__time_loop__output__timesteps}
    if (auto const timesteps = config.getConfigSubtreeOptional("timesteps"))
    {
        //! \ogs_file_param{prj__time_loop__output__timesteps__pair}
        for (auto pair : timesteps->getConfigSubtreeList("pair"))
        {
            //! \ogs_file_param{prj__time_loop__output__timesteps__pair__repeat}
            auto repeat = pair.getConfigParameter<unsigned>("repeat");
            //! \ogs_file_param{prj__time_loop__output__timesteps__pair__each_steps}
            auto each_steps = pair.getConfigParameter<unsigned>("each_steps");

            assert(repeat != 0 && each_steps != 0);
            repeats_each_steps.emplace_back(repeat, each_steps);
        }

        if (repeats_each_steps.empty())
        {
            OGS_FATAL(
                "You have not given any pair (<repeat/>, <each_steps/>) that "
                "defines at which timesteps output shall be written. "
                "Aborting.");
        }
    }
    else
    {
        repeats_each_steps.emplace_back(1, 1);
    }

    //! \ogs_file_param{prj__time_loop__output__variables}
    auto const out_vars = config.getConfigSubtree("variables");

    auto& output_variables = output_config.output_variables;
    for (auto out_var :
         //! \ogs_file_param{prj__time_loop__output__variables__variable}
         out_vars.getConfigParameterList<std::string>("variable"))
    {
        if (output_variables.find(out_var) != output_variables.cend())
        {
            OGS_FATAL("output variable `{:s}' specified more than once.",
                      out_var);
        }

        DBUG("adding output variable `{:s}'", out_var);
        output_variables.insert(out_var);
    }

    output_config.output_extrapolation_residuals =
        //! \ogs_file_param{prj__time_loop__output__output_extrapolation_residuals}
        config.getConfigParameter<bool>("output_extrapolation_residuals",
                                        false);

    auto& mesh_names_for_output = output_config.mesh_names_for_output;
    //! \ogs_file_param{prj__time_loop__output__meshes}
    if (auto const meshes_config = config.getConfigSubtreeOptional("meshes"))
    {
        if (output_config.prefix.find("{:meshname}") == std::string::npos)
        {
            OGS_FATAL(
                "There are multiple meshes defined in the output section of "
                "the project file, but the prefix doesn't contain "
                "'{{:meshname}}'. Thus the names for the files, the simulation "
                "results should be written to, would not be distinguishable "
                "for different meshes.");
        }
        //! \ogs_file_param{prj__time_loop__output__meshes__mesh}
        for (auto mesh_config : meshes_config->getConfigParameterList("mesh"))
        {
            // TODO CL check here that meshes name can be found in meshes list?
            mesh_names_for_output.push_back(
                mesh_config.getValue<std::string>());
            INFO("Configure mesh '{:s}' for output.",
                 mesh_names_for_output.back());
        }
    }

    if (auto const geometrical_sets_config =
            //! \ogs_file_param{prj__time_loop__output__geometrical_sets}
        config.getConfigSubtreeOptional("geometrical_sets"))
    {
        for (
            auto geometrical_set_config :
            //! \ogs_file_param{prj__time_loop__output__geometrical_sets__geometrical_set}
            geometrical_sets_config->getConfigSubtreeList("geometrical_set"))
        {
            auto const geometrical_set_name =
                //! \ogs_file_param{prj__time_loop__output__geometrical_sets__geometrical_set__name}
                geometrical_set_config.getConfigParameter<std::string>("name",
                                                                       "");
            auto const geometry_name =
                //! \ogs_file_param{prj__time_loop__output__geometrical_sets__geometrical_set__geometry}
                geometrical_set_config.getConfigParameter<std::string>(
                    "geometry");
            mesh_names_for_output.push_back(geometrical_set_name + "_" +
                                            geometry_name);
        }
    }

    output_config.fixed_output_times =
        //! \ogs_file_param{prj__time_loop__output__fixed_output_times}
        config.getConfigParameter<std::vector<double>>("fixed_output_times",
                                                       {});

    // Remove possible duplicated elements and sort.
    BaseLib::makeVectorUnique(output_config.fixed_output_times);

    output_config.output_iteration_results =
        //! \ogs_file_param{prj__time_loop__output__output_iteration_results}
        config.getConfigParameter<bool>("output_iteration_results", false);

    return output_config;
}
}  // namespace ProcessLib
