# SPDX-FileCopyrightText: 2022 Joe Freeman joe@freemansoft.com
#
# SPDX-License-Identifier: MIT
#
# Copy this file to boot.py to enable repl over uart0
# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()
import machine
import os

u = machine.UART(0, baudrate=115200)
os.dupterm(u)
