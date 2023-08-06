import os
import platform
import subprocess
import sys

binaries_list = [
    "addDataToRaster",
    "AddElementQuality",
    "AddFaultToVoxelGrid",
    "AddLayer",
    "appendLinesAlongPolyline",
    "AssignRasterDataToMesh",
    "checkMesh",
    "ComputeNodeAreasFromSurfaceMesh",
    "computeSurfaceNodeIDsInPolygonalRegion",
    "constructMeshesFromGeometry",
    "convertGEO",
    "convertToLinearMesh",
    "convertVtkDataArrayToVtkDataArray",
    "CreateBoundaryConditionsAlongPolylines",
    "createIntermediateRasters",
    "createLayeredMeshFromRasters",
    "createMeshElemPropertiesFromASCRaster",
    "createNeumannBc",
    "createQuadraticMesh",
    "createRaster",
    "editMaterialID",
    "ExtractBoundary",
    "ExtractMaterials",
    "ExtractSurface",
    "generateGeometry",
    "generateMatPropsFromMatID",
    "generateStructuredMesh",
    "geometryToGmshGeo",
    "GMSH2OGS",
    "GocadSGridReader",
    "GocadTSurfaceReader",
    "identifySubdomains",
    "IntegrateBoreholesIntoMesh",
    "ipDataToPointCloud",
    "Layers2Grid",
    "MapGeometryToMeshSurface",
    "Mesh2Raster",
    "MoveGeometry",
    "MoveMesh",
    "moveMeshNodes",
    "mpmetis",
    "NodeReordering",
    "ogs",
    "OGS2VTK",
    "partmesh",
    "PVD2XDMF",
    "queryMesh",
    "Raster2Mesh",
    "RemoveGhostData",
    "removeMeshElements",
    "ReorderMesh",
    "ResetPropertiesInPolygonalRegion",
    "reviseMesh",
    "scaleProperty",
    "swapNodeCoordinateAxes",
    "TecPlotTools",
    "tetgen",
    "TIN2VTK",
    "VTK2OGS",
    "VTK2TIN",
    "vtkdiff",
    "Vtu2Grid",
]


def ogs():
    raise SystemExit(ogs_with_args(sys.argv))


def ogs_with_args(argv):
    import ogs.simulator as sim

    return_code = sim.initialize(argv)

    # map mangled TCLAP status to usual exit status
    if return_code == 3:  # EXIT_ARGPARSE_FAILURE
        sim.finalize()
        return 1  # EXIT_FAILURE
    elif return_code == 2:  # EXIT_ARGPARSE_EXIT_OK
        sim.finalize()
        return 0  # EXIT_SUCCESS

    if return_code != 0:
        sim.finalize()
        return return_code

    return_code = sim.executeSimulation()
    sim.finalize()
    return return_code


if "PEP517_BUILD_BACKEND" not in os.environ:
    OGS_BIN_DIR = os.path.join(os.path.join(os.path.dirname(__file__), "..", "bin"))

    if platform.system() == "Windows":
        os.add_dll_directory(OGS_BIN_DIR)

    def _program(name, args):
        return subprocess.run([os.path.join(OGS_BIN_DIR, name)] + args).returncode

    FUNC_TEMPLATE = """def {0}(): raise SystemExit(_program("{0}", sys.argv[1:]))"""
    for f in binaries_list:
        if f == "ogs":
            continue  # provided by separate function
        exec(FUNC_TEMPLATE.format(f))
