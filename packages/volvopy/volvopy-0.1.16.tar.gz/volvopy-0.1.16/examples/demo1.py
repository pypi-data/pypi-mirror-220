#!/usr/bin/env python3

import os

# Running this demo requires the `volvopy` package to be installed by `pip`!
from volvopy import volvo_api as vp

DEBUG = True
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]

example_con = vp.Connected_Vehicle(debug=DEBUG)
example_con.get_all()

example_nrg = vp.Energy(debug=DEBUG)
example_nrg.get_all()

example_xtnd = vp.Extended_Vehicle(debug=DEBUG)
example_xtnd.get_all()

example_loc = vp.Location(debug=DEBUG)
example_loc.get_all()
