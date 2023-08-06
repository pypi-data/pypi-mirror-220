add_subdirectory(cpp)

if (BUILD_PYTHON)
    message(STATUS "Building Python bindings for itkpix-efuse-codec")
    add_subdirectory(python)
endif()
