class Application(object): ...
class AppBox(object):
    def __init__(self) -> None:
        self.app: Application = None

    def setApp(self, app: Application) -> None:
        try:
            self.app = app
        except RuntimeError as e:
            raise e

    def delApp(self) -> None:
        self.app = None

    def __bool__(self) -> bool:
        return bool(self.app)


def cleanApp(appBox: AppBox, isAuto: bool=False):
    if appBox:
        try:
            if not isAuto or (isAuto and not appBox.app.isAvailable):
                print("Application {} is {}removed.".format(appBox.app.getName(), "automatically " if isAuto else ""))
                appBox.delApp()
        except RuntimeError as e:
            try:
                appName = appBox.app.getName()
            except:
                appName = ""
            print("Application {} is removed due to exceptions: {}.".format(appName, e))
            appBox.delApp()