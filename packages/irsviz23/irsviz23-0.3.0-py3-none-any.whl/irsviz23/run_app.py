import pathlib
import os
import sys



def main():
    app_path = pathlib.Path(__file__).parent
    cmd = f"python -m bokeh serve --dev --show {app_path}"
    args = " ".join(sys.argv[1:])
    if len(sys.argv) > 1:
        cmd = f"{cmd} --args {args}"
    os.system(cmd)

if __name__ == "__main__":
    main()

