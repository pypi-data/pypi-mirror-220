#################################################################################
# WaterTAP Copyright (c) 2020-2023, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory, Oak Ridge National Laboratory,
# National Renewable Energy Laboratory, and National Energy Technology
# Laboratory (subject to receipt of any required approvals from the U.S. Dept.
# of Energy). All rights reserved.
#
# Please see the files COPYRIGHT.md and LICENSE.md for full copyright and license
# information, respectively. These files are also available online at the URL
# "https://github.com/watertap-org/watertap/"
#################################################################################
"""
Tests for thickener unit example.
"""

import pytest
from pyomo.environ import (
    ConcreteModel,
    value,
    assert_optimal_termination,
)

from idaes.core import (
    FlowsheetBlock,
    MaterialBalanceType,
    MomentumBalanceType,
)

from idaes.models.unit_models.separator import SplittingType

from pyomo.environ import (
    units,
)

from idaes.core.solvers import get_solver
from idaes.core.util.model_statistics import (
    degrees_of_freedom,
    number_variables,
    number_total_constraints,
    number_unused_variables,
)
import idaes.core.util.scaling as iscale
from idaes.core.util.testing import (
    initialization_tester,
)

from idaes.core.util.exceptions import (
    ConfigurationError,
)
from watertap.unit_models.thickener import Thickener
from watertap.property_models.activated_sludge.asm1_properties import (
    ASM1ParameterBlock,
)

from pyomo.util.check_units import assert_units_consistent


# -----------------------------------------------------------------------------
# Get default solver for testing
solver = get_solver()


# -----------------------------------------------------------------------------
@pytest.mark.unit
def test_config():
    m = ConcreteModel()

    m.fs = FlowsheetBlock(dynamic=False)

    m.fs.props = ASM1ParameterBlock()

    m.fs.unit = Thickener(property_package=m.fs.props)

    assert len(m.fs.unit.config) == 15

    assert not m.fs.unit.config.dynamic
    assert not m.fs.unit.config.has_holdup
    assert m.fs.unit.config.material_balance_type == MaterialBalanceType.useDefault
    assert m.fs.unit.config.momentum_balance_type == MomentumBalanceType.pressureTotal
    assert "underflow" in m.fs.unit.config.outlet_list
    assert "overflow" in m.fs.unit.config.outlet_list
    assert SplittingType.componentFlow is m.fs.unit.config.split_basis


@pytest.mark.unit
def test_list_error():
    m = ConcreteModel()

    m.fs = FlowsheetBlock(dynamic=False)

    m.fs.props = ASM1ParameterBlock()

    with pytest.raises(
        ConfigurationError,
        match="fs.unit encountered unrecognised "
        "outlet_list. This should not "
        "occur - please use overflow "
        "and underflow as outlets.",
    ):
        m.fs.unit = Thickener(
            property_package=m.fs.props, outlet_list=["outlet1", "outlet2"]
        )


# -----------------------------------------------------------------------------
class TestThick(object):
    @pytest.fixture(scope="class")
    def tu(self):
        m = ConcreteModel()
        m.fs = FlowsheetBlock(dynamic=False)

        m.fs.props = ASM1ParameterBlock()

        m.fs.unit = Thickener(property_package=m.fs.props)

        m.fs.unit.inlet.flow_vol.fix(300 * units.m**3 / units.day)
        m.fs.unit.inlet.temperature.fix(308.15 * units.K)
        m.fs.unit.inlet.pressure.fix(1 * units.atm)

        m.fs.unit.inlet.conc_mass_comp[0, "S_I"].fix(28.0643 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "S_S"].fix(0.67336 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "X_I"].fix(3036.2175 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "X_S"].fix(63.2392 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "X_BH"].fix(
            4442.8377 * units.mg / units.liter
        )
        m.fs.unit.inlet.conc_mass_comp[0, "X_BA"].fix(332.5958 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "X_P"].fix(1922.8108 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "S_O"].fix(1.3748 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "S_NO"].fix(9.1948 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "S_NH"].fix(0.15845 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "S_ND"].fix(0.55943 * units.mg / units.liter)
        m.fs.unit.inlet.conc_mass_comp[0, "X_ND"].fix(4.7411 * units.mg / units.liter)
        m.fs.unit.inlet.alkalinity.fix(4.5646 * units.mol / units.m**3)

        return m

    @pytest.mark.build
    @pytest.mark.unit
    def test_build(self, tu):

        assert hasattr(tu.fs.unit, "inlet")
        assert len(tu.fs.unit.inlet.vars) == 5
        assert hasattr(tu.fs.unit.inlet, "flow_vol")
        assert hasattr(tu.fs.unit.inlet, "conc_mass_comp")
        assert hasattr(tu.fs.unit.inlet, "temperature")
        assert hasattr(tu.fs.unit.inlet, "pressure")
        assert hasattr(tu.fs.unit.inlet, "alkalinity")

        assert hasattr(tu.fs.unit, "underflow")
        assert len(tu.fs.unit.underflow.vars) == 5
        assert hasattr(tu.fs.unit.underflow, "flow_vol")
        assert hasattr(tu.fs.unit.underflow, "conc_mass_comp")
        assert hasattr(tu.fs.unit.underflow, "temperature")
        assert hasattr(tu.fs.unit.underflow, "pressure")
        assert hasattr(tu.fs.unit.underflow, "alkalinity")

        assert hasattr(tu.fs.unit, "overflow")
        assert len(tu.fs.unit.overflow.vars) == 5
        assert hasattr(tu.fs.unit.overflow, "flow_vol")
        assert hasattr(tu.fs.unit.overflow, "conc_mass_comp")
        assert hasattr(tu.fs.unit.overflow, "temperature")
        assert hasattr(tu.fs.unit.overflow, "pressure")
        assert hasattr(tu.fs.unit.overflow, "alkalinity")

        assert number_variables(tu) == 76
        assert number_total_constraints(tu) == 60
        assert number_unused_variables(tu) == 0

    @pytest.mark.unit
    def test_dof(self, tu):
        assert degrees_of_freedom(tu) == 0

    @pytest.mark.unit
    def test_units(self, tu):
        assert_units_consistent(tu)

    @pytest.mark.solver
    @pytest.mark.skipif(solver is None, reason="Solver not available")
    @pytest.mark.component
    def test_initialize(self, tu):

        iscale.calculate_scaling_factors(tu)
        initialization_tester(tu)

    @pytest.mark.solver
    @pytest.mark.skipif(solver is None, reason="Solver not available")
    @pytest.mark.component
    def test_solve(self, tu):
        solver = get_solver()
        results = solver.solve(tu)
        assert_optimal_termination(results)

    @pytest.mark.solver
    @pytest.mark.skipif(solver is None, reason="Solver not available")
    @pytest.mark.component
    def test_solution(self, tu):
        assert pytest.approx(101325.0, rel=1e-3) == value(
            tu.fs.unit.overflow.pressure[0]
        )
        assert pytest.approx(308.15, rel=1e-3) == value(
            tu.fs.unit.overflow.temperature[0]
        )
        assert pytest.approx(0.003115, rel=1e-3) == value(
            tu.fs.unit.overflow.flow_vol[0]
        )
        assert pytest.approx(0.02806, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "S_I"]
        )
        assert pytest.approx(0.000673, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "S_S"]
        )
        assert pytest.approx(0.06768, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "X_I"]
        )
        assert pytest.approx(0.001409, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "X_S"]
        )
        assert pytest.approx(0.04286, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "X_P"]
        )
        assert pytest.approx(0.099046, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "X_BH"]
        )
        assert pytest.approx(0.007414, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "X_BA"]
        )
        assert pytest.approx(0.001374, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "S_O"]
        )
        assert pytest.approx(0.009194, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "S_NO"]
        )
        assert pytest.approx(0.0001584, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "S_NH"]
        )
        assert pytest.approx(0.0005594, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "S_ND"]
        )
        assert pytest.approx(0.0001056, rel=1e-3) == value(
            tu.fs.unit.overflow.conc_mass_comp[0, "X_ND"]
        )
        assert pytest.approx(0.004564, rel=1e-3) == value(
            tu.fs.unit.overflow.alkalinity[0]
        )

    @pytest.mark.solver
    @pytest.mark.skipif(solver is None, reason="Solver not available")
    @pytest.mark.component
    def test_conservation(self, tu):
        assert (
            abs(
                value(
                    tu.fs.unit.inlet.flow_vol[0] * tu.fs.props.dens_mass
                    - tu.fs.unit.overflow.flow_vol[0] * tu.fs.props.dens_mass
                    - tu.fs.unit.underflow.flow_vol[0] * tu.fs.props.dens_mass
                )
            )
            <= 1e-6
        )
        for i in tu.fs.props.solute_set:
            assert (
                abs(
                    value(
                        tu.fs.unit.inlet.flow_vol[0]
                        * tu.fs.unit.inlet.conc_mass_comp[0, i]
                        - tu.fs.unit.overflow.flow_vol[0]
                        * tu.fs.unit.overflow.conc_mass_comp[0, i]
                        - tu.fs.unit.underflow.flow_vol[0]
                        * tu.fs.unit.underflow.conc_mass_comp[0, i]
                    )
                )
                <= 1e-6
            )

    @pytest.mark.unit
    def test_report(self, tu):
        tu.fs.unit.report()
