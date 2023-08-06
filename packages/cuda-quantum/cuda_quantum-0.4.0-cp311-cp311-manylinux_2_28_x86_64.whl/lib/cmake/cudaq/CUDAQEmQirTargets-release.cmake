#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "cudaq::cudaq-em-qir" for configuration "Release"
set_property(TARGET cudaq::cudaq-em-qir APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(cudaq::cudaq-em-qir PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "nvqir::nvqir;cudaq::cudaq-common"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libcudaq-em-qir.so"
  IMPORTED_SONAME_RELEASE "libcudaq-em-qir.so"
  )

list(APPEND _cmake_import_check_targets cudaq::cudaq-em-qir )
list(APPEND _cmake_import_check_files_for_cudaq::cudaq-em-qir "${_IMPORT_PREFIX}/lib/libcudaq-em-qir.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
