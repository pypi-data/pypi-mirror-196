#include <Eigen/Core>
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

#include "fmt.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_cloud_geodesic, m) {
  m.doc() = "compute geodesic inside point cloud";

  py::class_<FastMarchingTree>(m, "_FastMarchingTree")
      .def(py::init<std::vector<Eigen::VectorXd>, double>())
      .def("get_geodesic_path", &FastMarchingTree::get_geodesic_path)
      .def("get_costs", &FastMarchingTree::get_costs)
      .def("span_tree", &FastMarchingTree::span_tree);
}
