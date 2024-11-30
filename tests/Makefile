# regression:
# 	echo Running regression
# .PHONY: regression

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

TOPLEVEL = tb_dummy_sink
MODULE = dp_sink

VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/auxch/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/artix7/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/test_streams/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/debug/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/unisim/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../tests/wrappers/*.v)

include $(shell cocotb-config --makefiles)/Makefile.sim

