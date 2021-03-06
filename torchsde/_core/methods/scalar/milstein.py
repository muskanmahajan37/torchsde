# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from torchsde._core import base_solver
from torchsde._core.methods.diagonal import milstein
from torchsde._core.methods.scalar import utils


class MilsteinScalar(base_solver.GenericSDESolver):

    def __init__(self, sde, bm, y0, dt, adaptive, rtol, atol, dt_min, options):
        super(MilsteinScalar, self).__init__(
            sde=sde, bm=bm, y0=y0, dt=dt, adaptive=adaptive, rtol=rtol, atol=atol, dt_min=dt_min, options=options)
        self._milstein_diagonal = milstein.MilsteinDiagonal(
            sde=sde, bm=bm, y0=y0, dt=dt, adaptive=adaptive, rtol=rtol, atol=atol, dt_min=dt_min, options=options)
        utils.check_scalar_bm(bm(0.0))  # Brownian motion of size (batch_size, 1).

    def step(self, t0, y0, dt):
        return self._milstein_diagonal.step(t0, y0, dt)  # Relies on broadcasting.

    @property
    def strong_order(self):
        return 1.0

    @property
    def weak_order(self):
        return 1.0
