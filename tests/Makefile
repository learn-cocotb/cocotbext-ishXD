SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/auxch/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/artix7/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/test_streams/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/debug/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../verilog/unisim/*.v)
VERILOG_SOURCES += $(wildcard $(PWD)/../tests/wrappers/*.v)


all: sink src

sink:
	rm -rf sim_build
	$(MAKE) sim MODULE=dp_sink TOPLEVEL=tb_dummy_sink_new
src:
	rm -rf sim_build
	$(MAKE) sim MODULE=dp_src TOPLEVEL=tb_data_stream


# Help Message
help:
	@echo "Makefile for running Cocotb testbenches with explicit targets"
	@echo "Usage:"
	@echo "  make all              Run all tests"
	@echo "  make src   Run test for tb_test_source"
	@echo "  make sink    Run test for tb_dummy_sink"


include $(shell cocotb-config --makefiles)/Makefile.sim

