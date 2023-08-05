# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 European Union;
# Licensed under the EUPL, Version 1.2 or – as soon they will be approved by the European Commission
# – subsequent versions of the EUPL (the "Licence");
#
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
"""
It provides GEARSHIFT architecture model `dsp`.

Sub-Modules:

.. currentmodule:: gearshift.core.model

.. autosummary::
    :nosignatures:
    :toctree: model/

    scaleTrace
    calculateShiftpointsNdvFullPC
"""

import schedula as sh
from .scaleTrace import dsp as _scaleTrace
from .calculateShiftpointsNdvFullPC import dsp as _calculateShiftpointsNdvFullPC

dsp = sh.BlueDispatcher(
    name="GEARSHIFT model",
    description="Calculates the speed trace with scaleTrace and predict the gearshift "
    "with calculateShiftpointsNdvFullPC",
)

dsp.add_data(
    data_id="execution_case", description="User input data of PYCSIS calibration stage."
)

dsp.add_function(
    function_id="speedTrace",
    function=sh.SubDispatch(_scaleTrace),
    inputs=["execution_case"],
    outputs=["speed_trace"],
    description="This function calibrates the speed trance, following the Sub-Annex 1",
)

dsp.add_function(
    function_id="calculateShiftpointsNdvFullPC",
    function=sh.SubDispatch(_calculateShiftpointsNdvFullPC),
    inputs=["execution_case", "speed_trace"],
    outputs=["shift_points"],
    description="This function calibrates the speed trance, following the Sub-Annex 1",
)
