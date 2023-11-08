# Configure with [fxsdk build-fx] or [fxsdk build-cg], which provide the
# toolchain file and module path of the fxSDK

cmake_minimum_required(VERSION 3.15)
project(MyAddin)

include(GenerateG3A)
include(Fxconv)
find_package(Gint 2.9 REQUIRED)

set(SOURCES
  src/jTetris.cpp
  src/tabs.cpp
  src/tetrisTab.cpp
  src/tetrisGame.cpp
  src/piece.cpp
  src/casioFX-CG50.cpp
)
# Shared assets, fx-9860G-only assets and fx-CG-50-only assets
set(ASSETS
  assets-cg/font_default.png
  assets-cg/font_vert.png
 )
set(ASSETS_fx
  assets-fx/example.png
  # ...
)
set(ASSETS_cg
  assets-cg/example.png
  # ...
)

fxconv_declare_assets(${ASSETS} ${ASSETS_fx} ${ASSETS_cg} WITH_METADATA)

add_executable(myaddin ${SOURCES} ${ASSETS} ${ASSETS_${FXSDK_PLATFORM}})
target_compile_options(myaddin PRIVATE -Wall -Wextra -Os)
target_link_libraries(myaddin Gint::Gint -lstdc++)

if("${FXSDK_PLATFORM_LONG}" STREQUAL fx9860G)
  generate_g1a(TARGET myaddin OUTPUT "MyAddin.g1a"
    NAME "MyAddin" ICON assets-fx/icon.png)
elseif("${FXSDK_PLATFORM_LONG}" STREQUAL fxCG50)
  generate_g3a(TARGET myaddin OUTPUT "jtetris.g3a"
    NAME "jTetris" ICONS assets-cg/icon-uns.png assets-cg/icon-sel.png)
endif()
