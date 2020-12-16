from conans import ConanFile, tools


class TestPackageConan(ConanFile):
    def build(self):
        pass

    def test(self):
        with tools.pythonpath(self):
            import mbuild
            env = mbuild.env.env_t()
            env.version()
            print("Success!")
