cmake_minimum_required(VERSION 3.14)

project(encuid2)

include(FetchContent)

FetchContent_Declare(
    tiny-aes-c
    GIT_REPOSITORY https://github.com/kokke/tiny-AES-c.git
    GIT_TAG master
    PATCH_COMMAND
        git reset --hard &&
        git apply ${CMAKE_CURRENT_SOURCE_DIR}/swtg_nonsense.patch
)

FetchContent_MakeAvailable(tiny-aes-c)

target_compile_options(tiny-aes PRIVATE -DSWTG=1 -DECB=1 -DCBC=0 -DCTR=0)

add_executable(${PROJECT_NAME} encuid2.c)

target_link_libraries(${PROJECT_NAME} PRIVATE tiny-aes)

target_include_directories(${PROJECT_NAME} PRIVATE ${tiny-aes-c_SOURCE_DIR})
