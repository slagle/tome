from tome.artifacts import file

class TestFile(file.File):
    path = 'testfile'
    contents = 'testcontents'

class TargetCliTxt(file.HttpFile):
    path = 'targetcli.txt'
    contents = 'http://file.rdu.redhat.com/~jslagle/targetcli.txt'
