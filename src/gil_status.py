import sys
import sysconfig


def main():
    # Check version
    print(f"Python version: {sys.version.split()[0]}")
    
    # Check GIL Status
    status = sysconfig.get_config_var("Py_GIL_DISABLED")
    if status is None:
        print("GIL disabling is not supported in this Python version.")
    elif status == 0:
        print("GIL is activ")
    else:
        print("GIL is disabled")


if __name__ == "__main__":
    main()