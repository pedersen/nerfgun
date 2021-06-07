cmake_minimum_required(VERSION 3.1.0)
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/cmake/ArduinoToolchain.cmake)
set(CMAKE_CXX_STANDARD 17)
set(PROJECT_NAME custom_controller)


set(${PROJECT_NAME}_BOARD megaADK)
# set(ARDUINO_CPU)
project(${PROJECT_NAME})

# Define additional source and header files or default arduino sketch files
set(${PROJECT_NAME}_SRCS "${PROJECT_SOURCE_DIR}/library/"
        "${ARDUINO_SDK_PATH}/hardware/arduino/avr/libraries/SoftwareSerial/src/SoftwareSerial.cpp")
set(${PROJECT_NAME}_HDRS "${PROJECT_SOURCE_DIR}/library/")

### Additional static libraries to include in the target.
# set(${PROJECT_NAME}_LIBS)

### Main sketch file
set(${PROJECT_NAME}_SKETCH custom_controller.ino)
#target_sources(${PROJECT_NAME}_SKETCH "${PROJECT_SOURCE_DIR}/library/")

### Add project directories into the build
# add_subdirectory()

### Additional settings to add non-standard or your own Arduino libraries.
# For this example (libs will contain additional arduino libraries)
# An Arduino library my_lib will contain files in libs/my_lib/: my_lib.h, my_lib.cpp + any other cpp files
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/
        "${PROJECT_SOURCE_DIR}/library/")

# For nested library sources replace ${LIB_NAME} with library name for each library
#set(SoftwareSerial_RECURSE true)

#### Additional settings for programmer. From programmers.txt
set(${PROJECT_NAME}_PROGRAMMER avrisp)
set(${PROJECT_NAME}_PORT /dev/ttyACM0)
# set(mega.upload.speed 9600)

## Verbose build process
set(${PROJECT_NAME}_AFLAGS -v)

generate_arduino_firmware(${PROJECT_NAME})


print_board_list()
print_programmer_list()
include_directories("${PROJECT_SOURCE_DIR}/library/")
