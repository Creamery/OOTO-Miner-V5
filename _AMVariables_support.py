
class _Singleton:
    _instance = None
    llistSSFs = []

    def updateSSFsList(self, input):
        self.llistSSFs.append(input)

    def getLlSSFs(self):
        return self.llistSSFs


def getSingleton():
    if _Singleton._instance is None:
        _Singleton._instance = _Singleton()
    return _Singleton._instance


