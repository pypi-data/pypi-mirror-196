/**
 * \file
 * \copyright
 * Copyright (c) 2012-2023, OpenGeoSys Community (http://www.opengeosys.org)
 *            Distributed under a Modified BSD License.
 *              See accompanying file LICENSE.txt or
 *              http://www.opengeosys.org/project/license
 *
 */

#pragma once

#include <MGIS/Behaviour/Variable.hxx>
#include <boost/mp11.hpp>

#include "BaseLib/cpp23.h"
#include "MathLib/KelvinVector.h"

namespace MaterialLib::Solids::MFront
{
namespace detail
{
//! Buffer of zeroes backing tangent operator blocks not provided by MFront.
//! The chosen size is the largest possible block size, corresponding to a
//! derivative dFull3DTensor/dFull3DTensor.
static constexpr std::array<double, 3 * 3 * 3 * 3>
    OGSMFrontTangentOperatorBlocksViewZeroes = {};
}  // namespace detail

/// Used for disambiguation with MFront's thermodynamic forces data.
struct OGSMFrontTangentOperatorData
{
    std::vector<double> data;
};

/**
 * Provides convenient access to the individual blocks of MFront's tangent
 * operator data.
 *
 * \tparam DisplacementDim the displacement dimension
 * \tparam Gradients a list (of types) of gradients driving the MFront behaviour
 * \tparam TDynForces a list (of types) of thermodynamic forces
 * \tparam ExtStateVars a list (of types) of external state variables
 *
 * "Gradients" is MFront nomenclature for the quantities driving an MFront
 * behaviour.
 *
 * "Thermodynamic forces" are the quantities an MFront behaviour computes.
 *
 * "External state variables" are additional quantities driving the MFront
 * behaviour, e.g. temperature.
 *
 * \c Gradients, \c TDynForces and \c ExtStateVars are lists of types. Type in
 * these lists is expected to behave like Strain and the other classes in
 * Variable.h.
 *
 * MFront's tangent operator blocks are stored in a single vector of double
 * values. The implementer of an MFront behaviour can decide which blocks she
 * wants to provide and in which order.
 */
template <int DisplacementDim,
          typename Gradients,
          typename TDynForces,
          typename ExtStateVars>
class OGSMFrontTangentOperatorBlocksView
{
    static_assert(boost::mp11::mp_is_set<Gradients>::value);
    static_assert(boost::mp11::mp_is_set<TDynForces>::value);
    static_assert(boost::mp11::mp_is_set<ExtStateVars>::value);

    using GradientsAndExtStateVars =
        boost::mp11::mp_append<Gradients, ExtStateVars>;

    static_assert(boost::mp11::mp_is_set<GradientsAndExtStateVars>::value);

    using ForcesGradsCombinations = boost::mp11::
        mp_product<boost::mp11::mp_list, TDynForces, GradientsAndExtStateVars>;

    /// Indicates that the associated tangent operator block is not present in
    /// the data.
    static constexpr std::size_t invalid_offset_ = -1;

public:
    /// Constructs a view for the tangent operator blocks \c to_blocks of some
    /// MFront behaviour.
    explicit OGSMFrontTangentOperatorBlocksView(
        std::vector<std::pair<mgis::behaviour::Variable,
                              mgis::behaviour::Variable>> const& to_blocks)
    {
        offsets_.fill(invalid_offset_);

        boost::mp11::mp_for_each<ForcesGradsCombinations>(
            [&to_blocks, this]<typename Force, typename GradOrExtStateVar>(
                boost::mp11::mp_list<Force, GradOrExtStateVar>)
            {
                std::size_t data_offset = 0;
                for (auto const& [force, grad] : to_blocks)
                {
                    if (force.name == Force::name &&
                        grad.name == GradOrExtStateVar::name)
                    {
                        auto const block_idx =
                            blockIndex<Force, GradOrExtStateVar>();
                        offsets_[block_idx] = data_offset;
                        return;
                    }

                    data_offset += size(force.type) * size(grad.type);
                }
            });
    }

    /// Read access to the block dForce/dGradOrExtStateVar.
    ///
    /// Returns an Eigen::Map, or a double value in the 1x1 case.
    ///
    /// If the block is not provided by the MFront behavior, the returned data
    /// is all zero.
    template <typename Force, typename GradOrExtStateVar>
    auto block(Force,
               GradOrExtStateVar,
               OGSMFrontTangentOperatorData const& data) const
    {
        static_assert(boost::mp11::mp_contains<TDynForces, Force>::value);
        static_assert(boost::mp11::mp_contains<GradientsAndExtStateVars,
                                               GradOrExtStateVar>::value);

        constexpr auto index = blockIndex<Force, GradOrExtStateVar>();
        const auto offset = offsets_[index];

        constexpr auto force_size = Force::template size<DisplacementDim>();
        constexpr auto grad_size =
            GradOrExtStateVar::template size<DisplacementDim>();

        if constexpr (grad_size == 1 && force_size == 1)
        {
            if (offset == invalid_offset_)
            {
                return 0.0;
            }

            return data.data[offset];
        }
        else
        {
            constexpr auto order =
                grad_size == 1 ? Eigen::ColMajor : Eigen::RowMajor;

            using Result = Eigen::Map<
                const Eigen::Matrix<double, force_size, grad_size, order>>;

            if (offset == invalid_offset_)
            {
                return Result{
                    detail::OGSMFrontTangentOperatorBlocksViewZeroes.data()};
            }

            return Result{data.data.data() + offset};
        }
    }

private:
    static constexpr std::size_t size(mgis::behaviour::Variable::Type vt)
    {
        using VT = mgis::behaviour::Variable::Type;

        switch (vt)
        {
            case VT::SCALAR:
                return 1;
            case VT::STENSOR:
                return MathLib::KelvinVector::kelvin_vector_dimensions(
                    DisplacementDim);
            case VT::VECTOR:
                return DisplacementDim;
            case VT::TENSOR:
                return DisplacementDim * DisplacementDim;
        }

        OGS_FATAL("Unsupported variable type {}", BaseLib::to_underlying(vt));
    }

    /// Computes the index of a tangent operator block in the #offsets_ array.
    template <typename Force, typename GradOrExtStateVar>
    static constexpr std::size_t blockIndex()
    {
        constexpr auto force_idx =
            boost::mp11::mp_find<TDynForces, Force>::value;
        constexpr auto grad_idx =
            boost::mp11::mp_find<GradientsAndExtStateVars,
                                 GradOrExtStateVar>::value;
        constexpr auto stride =
            boost::mp11::mp_size<GradientsAndExtStateVars>::value;

        return force_idx * stride + grad_idx;
    }

    /// Stores the data offsets of each tangent operator block.
    ///
    /// A value of #invalid_offset_ indicates that the tangent operator block is
    /// not provided by the MFront behaviour.
    std::array<std::size_t,
               boost::mp11::mp_size<ForcesGradsCombinations>::value>
        offsets_;
};
}  // namespace MaterialLib::Solids::MFront
