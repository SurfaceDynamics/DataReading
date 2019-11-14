class PathSplitter:
    def __init__(self):
        self.Path = ""
    def _pathCleaner(self, Path):
        self.Path = ""
        for i in range(len(Path)):
            if Path[i] != "":
                self.Path += Path[i]
                if i < len(Path) - 1:
                    self.Path += "/"

    def SplitPath(self, Path):
        path = str(Path)
        path = path.replace("[", "")
        path = path.replace("]", "")
        path = path.replace("'", "")
        path = path.split("\\")
        self._pathCleaner(path)
        pathLen = len(path) - 1
        return path[pathLen]