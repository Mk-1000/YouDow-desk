import os


class AllYouNeed:

    # create any file any time
    @classmethod
    def create_file(cls, dirName):
        # test if file exists
        if not os.path.exists(dirName):
            os.makedirs(dirName)
            print("Directory", dirName, "created.")
        else:
            print("Directory", dirName, "already exists.")

    # remove / ; ? : ... from name
    @classmethod
    def make_clean(cls, name):
        name = name.replace("/", "").replace("\\", "").replace(":", "").replace("*", "").replace("?", "").replace("\"",
                                                                                                                  "").replace(
            "<", "").replace(">", "").replace("|", "")
        return name

    # create any path
    @classmethod
    def create_path(cls, path, title):
        title = cls.make_clean(title)
        new_path = os.path.join(path, title)
        cls.create_file(new_path)
        return new_path

    # create any path
    @classmethod
    def youDowPath(cls, userhome):
        youdowPath = userhome + '\Desktop\YouDow'
        youDowPath = os.path.join(userhome, youdowPath)
        return youDowPath

    @classmethod
    def youDowPath(cls):
        userhome = os.path.expanduser('~')
        youdowPath = userhome + '\Desktop\YouDow'
        youDowPath = os.path.join(userhome, youdowPath)
        return youDowPath
