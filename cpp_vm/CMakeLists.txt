cmake_minimum_required(VERSION 3.16)
project(vulcan_rsvm CXX C)
set(CMAKE_CXX_STANDARD 17)
if(NOT OIRIA_ROOT)
  if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/rs_vm/vm/rs_vm.cpp")
    set(VM "${CMAKE_CURRENT_SOURCE_DIR}/rs_vm")
  elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../../OIRIA_OS_espIDF/os_code/core/rs_vm/vm/rs_vm.cpp")
    set(VM "${CMAKE_CURRENT_SOURCE_DIR}/../../OIRIA_OS_espIDF/os_code/core/rs_vm")
  endif()
else()
  set(VM "${OIRIA_ROOT}/os_code/core/rs_vm")
endif()
if(NOT VM)
  message(FATAL_ERROR "Set -DOIRIA_ROOT=... or copy os_code/core/rs_vm to cpp_vm/rs_vm")
endif()
add_executable(rsvm
  rsvm_cli.cpp
  rsvm_host_desktop.cpp
  ${VM}/vm/rs_vm.cpp
  ${VM}/vm/rs_vm_parse.cpp
  ${VM}/vm/rs_vm_latex.c
)
if(EXISTS ${VM}/vm/rs_vm_opt.cpp)
  target_sources(rsvm PRIVATE ${VM}/vm/rs_vm_opt.cpp)
endif()
if(EXISTS ${VM}/vm/rs_vm_struct.cpp)
  target_sources(rsvm PRIVATE ${VM}/vm/rs_vm_struct.cpp)
endif()
target_include_directories(rsvm PRIVATE ${VM}/.. ${VM}/vm ${OIRIA_ROOT} ${CMAKE_CURRENT_SOURCE_DIR})
