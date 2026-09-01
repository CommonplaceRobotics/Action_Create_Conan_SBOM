import os

from conan import ConanFile
from conan.tools.build import cross_building
from conan.tools.cmake import CMakeToolchain


class Recipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    # Make sure grpc build and tool requirements use the same options so it won't be built twice (to save time)
    grpc_options = {
        "csharp_ext": "False",
        "csharp_plugin": "False",
        "node_plugin": "False",
        "objective_c_plugin": "False",
        "otel_plugin": "False",
        "php_plugin": "False",
        "python_plugin": "False",
        "ruby_plugin": "False",
    }

    def requirements(self):
        # These requirements are linked to the product binary
        # Boost kann nicht weiter geupdated werden wegen Abhängigkeit in SerialInterfaceOrangeApps (vielleicht geht noch 1.87, aber 1.88 definitiv nicht)
        self.requires("boost/[1.86.0]")
        self.requires("b64/[^2]")
        self.requires("eigen/[^5]")
        self.requires("grpc/1.82.0", options=self.grpc_options, run=True)
        self.requires("libjpeg/9f")
        self.requires("libmodbus/[^3]")
        self.requires("openssl/[^3]")
        self.requires("paho-mqtt-c/[^1]")
        self.requires("tinyxml2/[^11]")
        self.requires("zlib/[^1]")

        if self.settings.os == "Linux":
            # For soloud
            self.requires("libalsa/[^1.2]", options={"shared": True})
            # For phidgets
            self.requires(
                "libusb/[^1.0.29]", options={"shared": True, "enable_udev": False}
            )

            # if str(self.settings.arch).startswith("arm"):
            # For LEDs + Anybus
            # self.requires(
            #    "libgpiod/2.2.5", options={"shared": True, "enable_bindings_cxx": True}
            # )

    def build_requirements(self):
        # These requirements are tools or for testing and therefore are not part of the product

        # gtest for testing
        self.test_requires("gtest/[^1]")

        # If cross compiling
        # TODO: Hilft der Workaround für Windows?
        if cross_building(self) and not self.settings.os == "Windows":
            self.tool_requires("grpc/1.82.0", options=self.grpc_options)

        # Needed for protoc only, auto-picks the version req'd by grpc
        self.tool_requires("protobuf/[^6.0.0]")

    def layout(self):
        # Defines the directory structure
        if self.settings.os == "Windows":
            self.folders.generators = os.path.join(
                "out",
                "conan",
                str(self.settings.os),
                str(self.settings.build_type),
                "generators",
            )
            self.folders.build = os.path.join(
                "out", "build", str(self.settings.os), str(self.settings.build_type)
            )
        else:
            # Linux: also distinguish architecture
            self.folders.generators = os.path.join(
                "out",
                "conan",
                str(self.settings.os),
                str(self.settings.arch),
                str(self.settings.build_type),
                "generators",
            )
            self.folders.build = os.path.join(
                "out",
                "build",
                str(self.settings.os),
                str(self.settings.arch),
                str(self.settings.build_type),
            )

    def generate(self):
        # https://docs.conan.io/2/reference/tools/cmake/cmaketoolchain.html
        tc = CMakeToolchain(self)
        # Do not generate CMakeUserPresets.json: If you use the generated preset,
        # clearing the CMake cache will delete the conan 'generators' directory.
        # This is not suitable for our Visual Studio based workflow.
        tc.user_presets_path = False
        tc.generate()
