import os
import inspect


class PathObj(os.PathLike):
    """Relative Path Object for all path handlings"""
    def __init__(self, relative_path: str, root: str):
        """
        Path Object

        :param relative_path: Specify the relative path to be converted
        :param root: Specify the root location. possible values: ['f' - current file's dir, 'c' - current working dir]
        """

        self.relative_path = relative_path
        self.root_option = root
        self.absolute_path = self._frame_abs_path()

    def _frame_abs_path(self) -> str:
        root_path = ""

        if self.root_option == 'f':
            root_path = os.path.dirname(inspect.stack()[3].filename)  # current file's dir
        elif self.root_option == 'c':
            root_path = os.path.abspath(os.curdir)  # current working dir
        else:
            raise ValueError(f"Invalid root option [{self.root_option}]\nPossible options: "
                              "['f' - current file's dir, 'c' - current working dir]")

        abs_path = os.path.join(root_path, self.relative_path)
        return os.path.normcase(os.path.normpath(abs_path))

    def __repr__(self):
        return self.absolute_path

    def __str__(self):
        return self.absolute_path

    def __fspath__(self):
        return self.absolute_path

    def __eq__(self, other):
        return os.path.samefile(self.absolute_path, other)


def rel2abs(relative_path: str, root='f'):
    """
    Convert Relative Path to Absolute Path Object

    :param relative_path: Specify the relative path to be converted
    :param root: Specify the root location. possible values: ['f' - current file's dir, 'c' - current working dir]
    """

    return PathObj(relative_path=relative_path, root=root)
