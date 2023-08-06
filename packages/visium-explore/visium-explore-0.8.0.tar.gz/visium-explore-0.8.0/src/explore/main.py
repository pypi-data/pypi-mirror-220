from streamlit.web.cli import main
import sys
from explore import app


def run_explore():
    sys.argv = ["streamlit", "run", app.__file__]
    print("Hello World")
    sys.exit(main())


if __name__ == "__main__":
    print("Hello World")
    run_explore()
