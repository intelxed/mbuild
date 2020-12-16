from conans import ConanFile


class MBuildConan(ConanFile):
    name = "mbuild"
    description = "A simple portable dependence-based build-system written in Python."
    url = "https://gitlab.devtools.intel.com/xed-group/xed"
    homepage = "https://intelxed.github.io/"
    license = "Apache License 2.0"
    topics = ("intel", "mbuild", "build")

    exports_sources = (
        "LICENSE",
        "mbuild/*",
    )
    no_copy_source = True

    def build(self):
        pass

    def package(self):
        self.copy("mbuild/*", src=self.source_folder)
        self.copy("LICENSE", src=self.source_folder, dst="licenses")

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
