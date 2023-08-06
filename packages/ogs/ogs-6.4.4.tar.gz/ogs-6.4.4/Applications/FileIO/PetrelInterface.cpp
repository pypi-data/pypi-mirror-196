/**
 * \file
 * \author Thomas Fischer
 * \date   2010-02-16
 * \brief  Implementation of the PetrelInterface class.
 *
 * \copyright
 * Copyright (c) 2012-2023, OpenGeoSys Community (http://www.opengeosys.org)
 *            Distributed under a Modified BSD License.
 *              See accompanying file LICENSE.txt or
 *              http://www.opengeosys.org/project/license
 *
 * @file PetrelInterface.cpp
 * @date 2010-02-16
 * @author Thomas Fischer
 */

#include "PetrelInterface.h"

#include <fstream>

#include "BaseLib/Logging.h"
#include "BaseLib/StringTools.h"
#include "GeoLib/GEOObjects.h"
#include "GeoLib/StationBorehole.h"

namespace FileIO
{
PetrelInterface::PetrelInterface(std::list<std::string> const& sfc_fnames,
                                 std::list<std::string> const& well_path_fnames,
                                 std::string& unique_model_name,
                                 GeoLib::GEOObjects* geo_obj)
    : _unique_name(unique_model_name)
{
    for (auto const& surface_fname : sfc_fnames)
    {
        INFO("PetrelInterface::PetrelInterface(): open surface file.");
        std::ifstream in(surface_fname);
        if (in)
        {
            INFO("PetrelInterface::PetrelInterface(): \tdone.");
            readPetrelSurfacePoints(in);
            in.close();
        }
        else
        {
            WARN(
                "PetrelInterface::PetrelInterface(): \tCould not open file "
                "{:s}.",
                surface_fname);
        }
    }

    for (auto const& well_path_fname : well_path_fnames)
    {
        INFO("PetrelInterface::PetrelInterface(): open well path file.");
        std::ifstream in(well_path_fname);
        if (in)
        {
            INFO("PetrelInterface::PetrelInterface(): \tdone.");
            readPetrelWellTrace(in);
            in.close();
        }
        else
        {
            WARN(
                "PetrelInterface::PetrelInterface(): \tCould not open well "
                "path file {:s}.",
                well_path_fname);
        }
    }

    // move data to GEOObject
    geo_obj->addPointVec(std::move(pnt_vec), _unique_name);
    if (!well_vec.empty())
    {
        geo_obj->addStationVec(std::move(well_vec), _unique_name);
    }
}

void PetrelInterface::readPetrelSurfacePoints(std::istream& in)
{
    char buffer[MAX_COLS_PER_ROW];
    in.getline(buffer, MAX_COLS_PER_ROW);
    std::string line(buffer);

    if (line.find("# Petrel Points with attributes") != std::string::npos)
    {
        // read header
        // read Version string
        in.getline(buffer, MAX_COLS_PER_ROW);
        // read string BEGIN HEADER
        in.getline(buffer, MAX_COLS_PER_ROW);

        in.getline(buffer, MAX_COLS_PER_ROW);
        line = buffer;
        while (line.find("END HEADER") == std::string::npos)
        {
            in.getline(buffer, MAX_COLS_PER_ROW);
            line = buffer;
        }

        // read points
        while (in)
        {
            auto point = std::make_unique<GeoLib::Point>();
            in >> (*point)[0] >> (*point)[1] >> (*point)[2];
            if (in)
            {
                pnt_vec.push_back(point.release());
            }
        }
    }
    else
    {
        WARN(
            "PetrelInterface::readPetrelSurface(): problem reading petrel "
            "points from line\n'{:s}'.",
            line);
    }
}

void PetrelInterface::readPetrelWellTrace(std::istream& in)
{
    char buffer[MAX_COLS_PER_ROW];
    in.getline(buffer, MAX_COLS_PER_ROW);
    std::string line(buffer);

    if (line.find("# WELL TRACE FROM PETREL") != std::string::npos)
    {
        // read header
        // read well name
        in.getline(buffer, MAX_COLS_PER_ROW);
        line = buffer;
        std::list<std::string> str_list(BaseLib::splitString(line, ' '));
        std::list<std::string>::const_iterator it(str_list.begin());
        while (it != str_list.end())
        {
            INFO("PetrelInterface::readPetrelWellTrace(): well name: {:s}.",
                 it->c_str());
            ++it;
        }

        // read well head x coordinate
        in.getline(buffer, MAX_COLS_PER_ROW);
        line = buffer;
        str_list = BaseLib::splitString(line, ' ');
        it = str_list.begin();
        while (it != str_list.end())
        {
            INFO(
                "PetrelInterface::readPetrelWellTrace(): well head x coord: "
                "{:s}.",
                it->c_str());
            ++it;
        }
        it = (str_list.end())--;
        --it;
        char* buf;
        double well_head_x(strtod((*it).c_str(), &buf));

        // read well head y coordinate
        in.getline(buffer, MAX_COLS_PER_ROW);
        line = buffer;
        str_list = BaseLib::splitString(line, ' ');
        it = str_list.begin();
        while (it != str_list.end())
        {
            INFO(
                "PetrelInterface::readPetrelWellTrace(): well head y coord: "
                "{:s}.",
                it->c_str());
            ++it;
        }
        it = (str_list.end())--;
        --it;
        double well_head_y(strtod((*it).c_str(), &buf));

        // read well KB
        in.getline(buffer, MAX_COLS_PER_ROW);
        line = buffer;
        str_list = BaseLib::splitString(line, ' ');
        it = str_list.begin();
        while (it != str_list.end())
        {
            INFO("PetrelInterface::readPetrelWellTrace(): well kb entry: {:s}.",
                 it->c_str());
            ++it;
        }
        it = --(str_list.end());
        double well_kb(strtod((*it).c_str(), &buf));

        INFO("PetrelInterface::readPetrelWellTrace(): {:f}, {:f}, {:f}.",
             well_head_x,
             well_head_y,
             well_kb);
        double const depth = 0.0;
        std::string const borehole_name = "";
        int const date = 0;
        well_vec.push_back(new GeoLib::StationBorehole(
            well_head_x, well_head_y, well_kb, depth, borehole_name, date));

        // read well type
        in.getline(buffer, MAX_COLS_PER_ROW);
        //        std::string type(*((str_list.end())--));

        readPetrelWellTraceData(in);
    }
}

void PetrelInterface::readPetrelWellTraceData(std::istream& in)
{
    char buffer[MAX_COLS_PER_ROW];
    in.getline(buffer, MAX_COLS_PER_ROW);
    std::string line(buffer);

    // read yet another header line
    in.getline(buffer, MAX_COLS_PER_ROW);
    line = buffer;
    while (line[0] == '#')
    {
        in.getline(buffer, MAX_COLS_PER_ROW);
        line = buffer;
    }

    // read column information
    std::list<std::string> str_list = BaseLib::splitString(line, ' ');
    auto it = str_list.begin();
    while (it != str_list.end())
    {
        INFO(
            "PetrelInterface::readPetrelWellTraceData(): column information: "
            "{:s}.",
            it->c_str());
        ++it;
    }

    // read points
    double md;
    double x;
    double y;
    double z;
    double tvd;
    double dx;
    double dy;
    double azim;
    double incl;
    double dls;
    in.getline(buffer, MAX_COLS_PER_ROW);
    line = buffer;
    while (in)
    {
        if (line.size() > 1 && line[0] != '#')
        {
            std::stringstream stream(line);
            stream >> md;
            stream >> x >> y >> z;
            //            pnt_vec->push_back (new GeoLib::Point (x,y,z));
            static_cast<GeoLib::StationBorehole*>(well_vec.back())
                ->addSoilLayer(x, y, z, "unknown");
            stream >> tvd >> dx >> dy >> azim >> incl >> dls;
        }
        in.getline(buffer, MAX_COLS_PER_ROW);
        line = buffer;
    }
}
}  // end namespace FileIO
