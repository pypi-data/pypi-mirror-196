import platform

def is_mac_os() -> bool:
    return "darwin" == platform.system().lower()

def is_linux() -> bool:
    return "linux" == platform.system().lower()

def is_windows() -> bool:
    return "windows" == platform.system().lower()

def get_arch() -> str:
    """
    Returns the current machine architecture
    :return: "amd64" when x86_64, "arm64" if aarch64, platform.machine() otherwise
    """
    arch = platform.machine().lower()
    if arch == "x86_64" or arch == "x64" :
        return "amd64"
    if arch == "aarch64":
        return "arm64"
    return arch

def get_os() -> str:
    if is_mac_os():
        return "darwin"
    if is_linux():
        return "linux"
    if is_windows():
        return "windows"
    raise ValueError("Unable to determine local operating system")