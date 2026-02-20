import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy


class AlayaLiteConan(ConanFile):
    name = "AlayaLite"
    version = "0.1.1a1"
    settings = "os", "compiler", "build_type", "arch"
    package_type = "header-library"
    exports_sources = "include/*", "python/*", "python/*/*", "python/*/*/*", "cmake/*", "CMakeLists.txt"
    platform_tool_requires = "cmake/3.23.5"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("gtest/1.16.0")
        self.requires("concurrentqueue/1.0.4")
        self.requires("pybind11/2.13.6")
        self.requires("spdlog/1.14.0")
        self.requires("eigen/3.4.0")

        if self.settings.os == "Linux":
            self.requires("libcoro/0.14.1")

    def configure(self):
        self.options["*"].shared = False
        self.options["*"].fPIC = True
        self.options["spdlog"].header_only = True

        if self.settings.os == "Linux":
            self.options["libcoro"].feature_networking = False
            self.options["libcoro"].feature_tls = False
            self.options["libcoro"].build_examples = False
            self.options["libcoro"].build_tests = False

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        cmake = CMakeDeps(self)
        cmake.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        copy(
            self,
            "*.h",
            src=os.path.join(self.export_sources_folder, "include"),
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*.hpp",
            src=os.path.join(self.export_sources_folder, "include"),
            dst=os.path.join(self.package_folder, "include"),
        )

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
