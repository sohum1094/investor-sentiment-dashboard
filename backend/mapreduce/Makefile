.SUFFIXES:  # Clear default suffixes to prevent implicit rules

# Define variables
OBJS_DIR = .objs

# Get all the mapper and reducer source files
MAPPERS_SRCS = $(wildcard mappers/*.c)
MAPPERS = $(MAPPERS_SRCS:mappers/%.c=mapper_%)

REDUCERS_SRCS = $(wildcard reducers/*.c)
REDUCERS = $(REDUCERS_SRCS:reducers/%.c=reducer_%)

# Tools
TOOLS_SRCS = mapreduce.c splitter.c
TOOLS = $(TOOLS_SRCS:%.c=%)

# Dependencies
MAPPERS_DEPS = core/mapper.c core/utils.c
REDUCERS_DEPS = core/reducer.c core/libds.c core/utils.c
TOOLS_DEPS = core/utils.c

# Compiler settings
CC = gcc
WARNINGS = -Wall -Wextra -Werror -Wno-error=unused-parameter
INC = -Icore/
CFLAGS_COMMON = $(WARNINGS) $(INC) -std=c99 -c -MMD -MP -D_GNU_SOURCE
CFLAGS_RELEASE = $(CFLAGS_COMMON) -O2

LD = gcc
LDFLAGS = -lm

# Phony targets
.PHONY: all release clean

all: release

release: $(MAPPERS) $(REDUCERS) $(TOOLS)

# Include dependency files
-include $(shell find $(OBJS_DIR) -name '*.d')

# Create the OBJS_DIR if it doesn't exist
$(OBJS_DIR):
	mkdir -p $(OBJS_DIR)

# Pattern rule to compile .c files into .o files
$(OBJS_DIR)/%.o: %.c | $(OBJS_DIR)
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS_RELEASE) $< -o $@

# Build rules for mappers
mapper_%: $(MAPPERS_DEPS:%.c=$(OBJS_DIR)/%.o) $(OBJS_DIR)/mappers/%.o
	$(LD) $^ $(LDFLAGS) -o $@

# Build rules for reducers
reducer_%: $(REDUCERS_DEPS:%.c=$(OBJS_DIR)/%.o) $(OBJS_DIR)/reducers/%.o
	$(LD) $^ $(LDFLAGS) -o $@

# Build rules for tools
$(TOOLS): %: $(OBJS_DIR)/%.o $(TOOLS_DEPS:%.c=$(OBJS_DIR)/%.o)
	$(LD) $^ $(LDFLAGS) -o $@

# Clean target
clean:
	rm -rf $(OBJS_DIR) $(MAPPERS) $(REDUCERS) $(TOOLS)

