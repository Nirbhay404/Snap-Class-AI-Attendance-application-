import sys
import os

# Ensure pkg_resources compatibility for legacy packages (face_recognition_models, webrtcvad) on Python 3.13+
try:
    import pkg_resources
except ModuleNotFoundError:
    import importlib.metadata as _im
    import importlib.resources as _ir

    class _PkgResourcesStub:
        @staticmethod
        def resource_filename(package_name, path):
            return str(_ir.files(package_name).joinpath(path))

        @staticmethod
        def get_distribution(dist_name):
            class _Dist:
                try:
                    version = _im.version(dist_name)
                except Exception:
                    version = "1.0.0"
            return _Dist()

    sys.modules["pkg_resources"] = _PkgResourcesStub()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen


def main():
    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    match st.session_state["login_type"]:
        case "teacher":
            teacher_screen()

        case "student":
            student_screen()

        case None:
            home_screen()


if __name__ == "__main__":
    main()