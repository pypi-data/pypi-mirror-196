from string import Template

class HostCommand():
    ADB_ROOT = "adb root"
    ADB_PULL = Template("adb pull $path")
    ADB_SNAPSHOT_SAVE = Template("adb emu avd snapshot save $name")