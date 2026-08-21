cmake_minimum_required(VERSION 3.8)
cmake_policy(SET CMP0009 NEW)
project(robot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

ament_environment_hooks(
  "${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/fastdds_udp.sh.in"
)

function(install_resource_files resource_dir)
  file(
    GLOB_RECURSE resource_files
    RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
    "${resource_dir}/*"
  )

  if(resource_dir STREQUAL "urdf")
    list(FILTER resource_files EXCLUDE REGEX "^urdf/(build|install|log)(/|$)")
  endif()

  foreach(resource_file IN LISTS resource_files)
    set(source_file "${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}")
    if(IS_DIRECTORY "${source_file}")
      continue()
    endif()

    get_filename_component(destination_dir "${resource_file}" DIRECTORY)
    install(
      FILES "${resource_file}"
      DESTINATION "share/${PROJECT_NAME}/${destination_dir}"
    )
  endforeach()
endfunction()

install_resource_files(launch)
install_resource_files(worlds)
install_resource_files(urdf)
install_resource_files(config)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
