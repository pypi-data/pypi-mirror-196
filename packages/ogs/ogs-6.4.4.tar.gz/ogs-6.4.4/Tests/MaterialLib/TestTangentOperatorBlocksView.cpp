/**
 * \file
 * \copyright
 * Copyright (c) 2012-2023, OpenGeoSys Community (http://www.opengeosys.org)
 *            Distributed under a Modified BSD License.
 *              See accompanying file LICENSE.txt or
 *              http://www.opengeosys.org/project/license
 *
 */

#ifdef OGS_USE_MFRONT

#include <gtest/gtest.h>

#include <numeric>

#include "MaterialLib/SolidModels/MFront/TangentOperatorBlocksView.h"
#include "MaterialLib/SolidModels/MFront/Variable.h"
#include "OGSMFrontTestVariables.h"
#include "Tests/TestTools.h"

template <class Dim>
struct MaterialLib_TangentOperatorBlocksView : ::testing::Test
{
};

using MaterialLib_TangentOperatorBlocksView_TestCases =
    ::testing::Types<std::integral_constant<int, 2>,
                     std::integral_constant<int, 3>>;

TYPED_TEST_SUITE(MaterialLib_TangentOperatorBlocksView,
                 MaterialLib_TangentOperatorBlocksView_TestCases);

TYPED_TEST(MaterialLib_TangentOperatorBlocksView, Test1)
{
    namespace MB = mgis::behaviour;
    using Var = MB::Variable;
    using namespace boost::mp11;
    namespace MSM = MaterialLib::Solids::MFront;

    constexpr int dim = TypeParam::value;
    constexpr int kv_size =
        MathLib::KelvinVector::kelvin_vector_dimensions(dim);

    const std::vector to_blocks{
        // dsigma/dtensor
        std::pair{Var{"Stress", Var::STENSOR}, Var{"tensor", Var::TENSOR}},
        // dvector/dp
        std::pair{Var{"vector", Var::VECTOR},
                  Var{"LiquidPressure", Var::SCALAR}},
        // dsigma/dT
        std::pair{Var{"Stress", Var::STENSOR},
                  Var{"Temperature", Var::SCALAR}}};

    const std::size_t total_data_size = kv_size * dim * dim + dim + kv_size;

    using Gradients = mp_list<MSM::LiquidPressure, Tensor>;
    using TDynForces = mp_list<Vector, MSM::Stress>;
    using ExtStateVars = mp_list<MSM::Temperature>;

    MSM::OGSMFrontTangentOperatorBlocksView<dim,
                                            Gradients,
                                            TDynForces,
                                            ExtStateVars>
        view(to_blocks);

    MSM::OGSMFrontTangentOperatorData data{};
    data.data.resize(total_data_size);
    std::iota(begin(data.data), end(data.data), 0);

    // dvector/dp != 0
    {
        using Vec = Eigen::Vector<double, dim>;
        auto const offset = kv_size * dim * dim;
        Vec const expected = Vec::LinSpaced(offset, offset + dim - 1);

        auto const b = view.block(Vector{}, MSM::liquid_pressure, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, expected, b);
    }

    // dvector/dtensor = 0
    {
        using Mat = Eigen::Matrix<double, dim, dim * dim>;
        Mat const zero = Mat::Zero();

        auto const b = view.block(Vector{}, Tensor{}, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, zero, b);
    }

    // dvector/T = 0
    {
        using Vec = Eigen::Vector<double, dim>;
        Vec const zero = Vec::Zero();

        auto const b = view.block(Vector{}, MSM::temperature, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, zero, b);
    }

    // dsigma/dp = 0
    {
        using Vec = Eigen::Vector<double, kv_size>;
        Vec const zero = Vec::Zero();

        auto const b = view.block(MSM::stress, MSM::liquid_pressure, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, zero, b);
    }

    // dsigma/dtensor != 0
    {
        using Mat = Eigen::Matrix<double, kv_size, dim * dim>;
        Mat expected = Mat::Zero();
        for (int r = 0; r < kv_size; ++r)
        {
            for (int c = 0; c < dim * dim; ++c)
            {
                expected(r, c) = dim * dim * r + c;
            }
        }

        auto const b = view.block(MSM::stress, Tensor{}, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, expected, b);
    }

    // dsigma/dT != 0
    {
        using Vec = Eigen::Vector<double, kv_size>;
        auto const offset = kv_size * dim * dim + dim;
        Vec const expected = Vec::LinSpaced(offset, offset + kv_size - 1);

        auto const b = view.block(MSM::stress, MSM::temperature, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, expected, b);
    }
}

TYPED_TEST(MaterialLib_TangentOperatorBlocksView, Test2)
{
    namespace MB = mgis::behaviour;
    using Var = MB::Variable;
    using namespace boost::mp11;
    namespace MSM = MaterialLib::Solids::MFront;

    constexpr int dim = TypeParam::value;
    constexpr int kv_size =
        MathLib::KelvinVector::kelvin_vector_dimensions(dim);

    const std::vector to_blocks{
        // dsigma/dtensor
        std::pair{Var{"Stress", Var::STENSOR}, Var{"tensor", Var::TENSOR}},
        // dvector/dp
        std::pair{Var{"Saturation", Var::VECTOR},
                  Var{"LiquidPressure", Var::SCALAR}}};

    const std::size_t total_data_size = kv_size * dim * dim + 1;

    using Gradients = mp_list<MSM::LiquidPressure, Tensor>;
    using TDynForces = mp_list<MSM::Saturation, MSM::Stress>;
    using ExtStateVars = mp_list<MSM::Temperature>;

    MSM::OGSMFrontTangentOperatorBlocksView<dim,
                                            Gradients,
                                            TDynForces,
                                            ExtStateVars>
        view(to_blocks);

    MSM::OGSMFrontTangentOperatorData data{};
    data.data.resize(total_data_size);
    std::iota(begin(data.data), end(data.data), 0);

    // dsat/dp != 0
    {
        auto const offset = kv_size * dim * dim;
        auto const expected = offset;

        auto const b = view.block(MSM::saturation, MSM::liquid_pressure, data);

        // double comparison (not Eigen::Map), not contained in the first test
        // case
        EXPECT_DOUBLE_EQ(expected, b);
    }

    // dsat/dtensor = 0
    {
        using Vec = Eigen::RowVector<double, dim * dim>;
        Vec const zero = Vec::Zero();

        auto const b = view.block(MSM::saturation, Tensor{}, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, zero, b);
    }

    // dsat/dT = 0
    {
        auto const b = view.block(MSM::saturation, MSM::temperature, data);

        EXPECT_DOUBLE_EQ(0, b);
    }

    // dsigma/dp = 0
    {
        using Vec = Eigen::Vector<double, kv_size>;
        Vec const zero = Vec::Zero();

        auto const b = view.block(MSM::stress, MSM::liquid_pressure, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, zero, b);
    }

    // dsigma/dtensor != 0
    {
        using Mat = Eigen::Matrix<double, kv_size, dim * dim>;
        Mat expected = Mat::Zero();
        for (int r = 0; r < kv_size; ++r)
        {
            for (int c = 0; c < dim * dim; ++c)
            {
                expected(r, c) = dim * dim * r + c;
            }
        }

        auto const b = view.block(MSM::stress, Tensor{}, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, expected, b);
    }

    // dsigma/dT == 0
    {
        using Vec = Eigen::Vector<double, kv_size>;
        Vec const zero = Vec::Zero();

        auto const b = view.block(MSM::stress, MSM::temperature, data);

        EXPECT_PRED_FORMAT2(Tests::EigenIsNear{}, zero, b);
    }
}

#endif
