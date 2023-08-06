from skbuild import setup

install_requires = [
    "numpy",
]

setup(
    name="cloud_geodesic",
    version="0.0.1",
    description="python interface to cloud geodesic",
    author="Hirokazu Ishida",
    license="MIT",
    packages=["cloud_geodesic"],
    package_dir={"": "python"},
    cmake_install_dir="python/cloud_geodesic/",
    install_requires=install_requires,
    package_data={"cloud_geodesic": ["py.typed"]},
)
