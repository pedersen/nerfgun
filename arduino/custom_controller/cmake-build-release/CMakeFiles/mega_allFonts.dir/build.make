# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.19

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/marvin/.local/share/JetBrains/Toolbox/apps/CLion/ch-0/211.7442.42/bin/cmake/linux/bin/cmake

# The command to remove a file.
RM = /home/marvin/.local/share/JetBrains/Toolbox/apps/CLion/ch-0/211.7442.42/bin/cmake/linux/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/marvin/src/nerfgun/arduino/custom_controller

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release

# Include any dependencies generated for this target.
include CMakeFiles/mega_allFonts.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/mega_allFonts.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/mega_allFonts.dir/flags.make

CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.obj: CMakeFiles/mega_allFonts.dir/flags.make
CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.obj: ../libs/openGLCD/gText.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.obj"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.obj -c /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/gText.cpp

CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.i"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/gText.cpp > CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.i

CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.s"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/gText.cpp -o CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.s

CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.obj: CMakeFiles/mega_allFonts.dir/flags.make
CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.obj: ../libs/openGLCD/glcd.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.obj"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.obj -c /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/glcd.cpp

CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.i"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/glcd.cpp > CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.i

CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.s"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/glcd.cpp -o CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.s

CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.obj: CMakeFiles/mega_allFonts.dir/flags.make
CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.obj: ../libs/openGLCD/glcd_Device.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.obj"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.obj -c /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/glcd_Device.cpp

CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.i"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/glcd_Device.cpp > CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.i

CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.s"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/glcd_Device.cpp -o CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.s

CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.obj: CMakeFiles/mega_allFonts.dir/flags.make
CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.obj: ../libs/openGLCD/openGLCD.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.obj"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.obj -c /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/openGLCD.c

CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.i"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/openGLCD.c > CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.i

CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.s"
	/opt/arduino1.8.15/hardware/tools/avr/bin/avr-gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/marvin/src/nerfgun/arduino/custom_controller/libs/openGLCD/openGLCD.c -o CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.s

# Object files for target mega_allFonts
mega_allFonts_OBJECTS = \
"CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.obj" \
"CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.obj" \
"CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.obj" \
"CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.obj"

# External object files for target mega_allFonts
mega_allFonts_EXTERNAL_OBJECTS =

libmega_allFonts.a: CMakeFiles/mega_allFonts.dir/libs/openGLCD/gText.cpp.obj
libmega_allFonts.a: CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd.cpp.obj
libmega_allFonts.a: CMakeFiles/mega_allFonts.dir/libs/openGLCD/glcd_Device.cpp.obj
libmega_allFonts.a: CMakeFiles/mega_allFonts.dir/libs/openGLCD/openGLCD.c.obj
libmega_allFonts.a: CMakeFiles/mega_allFonts.dir/build.make
libmega_allFonts.a: CMakeFiles/mega_allFonts.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking CXX static library libmega_allFonts.a"
	$(CMAKE_COMMAND) -P CMakeFiles/mega_allFonts.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/mega_allFonts.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/mega_allFonts.dir/build: libmega_allFonts.a

.PHONY : CMakeFiles/mega_allFonts.dir/build

CMakeFiles/mega_allFonts.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/mega_allFonts.dir/cmake_clean.cmake
.PHONY : CMakeFiles/mega_allFonts.dir/clean

CMakeFiles/mega_allFonts.dir/depend:
	cd /home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/marvin/src/nerfgun/arduino/custom_controller /home/marvin/src/nerfgun/arduino/custom_controller /home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release /home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release /home/marvin/src/nerfgun/arduino/custom_controller/cmake-build-release/CMakeFiles/mega_allFonts.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/mega_allFonts.dir/depend

