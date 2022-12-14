from core.template.moduleTemplate import ModuleTemplate
from module.sample.input.uniInput import UniInput
from module.sample.run import sampleRun as runFunc


class Module(ModuleTemplate):

    def __init__(self):
        super(Module, self).__init__("sample")
        self.input.append(UniInput())
        for inp in self.input:
            inp.init()

    def run(self):
        runFunc(self.input[0].get())
        pass


if __name__ == "__main__":
    m = Module()
    m.run()