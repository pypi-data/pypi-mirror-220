


class pyqtclass_init(AppTester):

    def __init__(self): super().__init__()
    def run(self): self.testNo(1)

    def test01(self):
        class JobObject(QObject):
            finished = pyqtSignal()
            @ctracer
            def __init__(self): super().__init__()
            @ctracer
            @pyqtSlot()
            def do(self):
                for i in range(5):
                    logger.info(i)
                    sleep(1)
                self.finished.emit()

        @ctracer
        @pyqtSlot(str)
        def __report__(s):
            sleep(1)
            print(vars(self.w))
        self.w = ThreadGenerator(JobObject, 'do')
        self.w.set_workerId('JOB')
        self.w.terminated.connect(__report__)
        self.w.start()
