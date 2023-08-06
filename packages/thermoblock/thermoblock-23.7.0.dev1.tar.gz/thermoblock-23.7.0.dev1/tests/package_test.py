# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Physicscore contributors (https://github.com/physicscore)
import thermoblock as pkg


def test_has_version():
    assert hasattr(pkg, '__version__')
