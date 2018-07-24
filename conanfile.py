
from conans import ConanFile, CMake, tools


class CppNetLibUriConan(ConanFile):
    name = "cpp-netlib-uri"
    version = "0.0.1"
    license = "Boost Software License"
    url = "https://github.com/cpp-netlib/uri"
    description = "Code that was originally meant to track the proposal for a C++ URI."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run( "git clone --depth 1 --recursive https://github.com/cpp-netlib/uri" )
        
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("uri/CMakeLists.txt", "project(Uri)",
                              '''project(Uri)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="uri")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        
        self.copy("*.h",   dst="include", src="uri/include")
        self.copy("*.hpp", dst="include", src="uri/include")
        
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("lib/libnetwork-uri.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["network-uri"]

