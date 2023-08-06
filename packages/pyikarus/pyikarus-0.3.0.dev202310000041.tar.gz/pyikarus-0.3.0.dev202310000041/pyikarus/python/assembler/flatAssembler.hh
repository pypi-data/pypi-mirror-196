// SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
// SPDX-License-Identifier: LGPL-3.0-or-later

#pragma once

#include <dune/functions/functionspacebases/lagrangebasis.hh>
#include <dune/functions/functionspacebases/powerbasis.hh>
#include <dune/grid/yaspgrid.hh>
#include <dune/python/common/typeregistry.hh>
//#include <dune/python/pybind11/numpy.h>
#include <dune/python/pybind11/eigen.h>
#include <dune/python/pybind11/pybind11.h>
#include <dune/python/pybind11/stl.h>

#include <pyikarus/finiteElements/feRequirements.hh>

namespace Ikarus::Python {

#define MAKE_ASSEMBLER_REGISTERY_FUNCTION(name)         \
  template <class Assembler, class... options>  \
void register##name(pybind11::handle scope, pybind11::class_<Assembler, options...> cls) {  \
  using pybind11::operator""_a;  \
  using FEContainer    = typename Assembler::FEContainer;   \
  using Basis    = typename Assembler::Basis;   \
  using DirichletValuesType    = typename Assembler::DirichletValuesType;   \
  using FERequirementType    = typename Assembler::FERequirementType;   \
\
  cls.def(pybind11::init([](const pybind11::list& fes, const DirichletValuesType& dirichletValues) {   \
            FEContainer fesV = fes.template cast< FEContainer >();  \
            return new Assembler(std::move(fesV),dirichletValues);   \
          }),   \
          pybind11::keep_alive<1, 2>(), pybind11::keep_alive<1, 3>());   \
\
/* sparse matrices need to be copied to python therefore we remove the reference of the return type, see */  \
/* https://github.com/pybind/pybind11/blob/cbb876cc7b02c5f57e715cbc2c46ead3d1fbcf79/tests/test_eigen_matrix.cpp#L332-L341 */  \
cls.def("getMatrix", [](Assembler& self, const FERequirementType& req) -> std::remove_cvref_t<   \
    decltype(self.getReducedMatrix(req))> { return self.getMatrix(req); });   \
cls.def("getReducedMatrix", [](Assembler& self, const FERequirementType& req) -> std::remove_cvref_t< \
    decltype(self.getReducedMatrix(req))> { return self.getReducedMatrix(req); }); \
cls.def("getVector", [](Assembler& self, const FERequirementType& req) { return self.getVector(req); }, pybind11::return_value_policy::reference); \
cls.def("getScalar", [](Assembler& self, const FERequirementType& req) { return self.getScalar(req); }, pybind11::return_value_policy::reference); \
cls.def("getReducedVector", [](Assembler& self, const FERequirementType& req) { return self.getReducedVector(req); }, pybind11::return_value_policy::reference); \
}

MAKE_ASSEMBLER_REGISTERY_FUNCTION(SparseFlatAssembler);
MAKE_ASSEMBLER_REGISTERY_FUNCTION(DenseFlatAssembler);


}  // namespace Ikarus::Python
