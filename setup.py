from setuptools import setup, find_packages

setup(
    name="face_attendance",
    version="0.1.0",
    author="Siddhartha Ganguli",
    author_email="siddharthaganguli0093@gmail.com",
    description="Smart Attendance System Using Face Recognition",
    long_description="Smart Attendance System using Face Recognition with Python and OpenCV",
    long_description_content_type="text/markdown",
    license="MIT",

    package_dir={"": "src"},
    packages=find_packages(where="src"),

    include_package_data=True,
    python_requires=">=3.8",
)
