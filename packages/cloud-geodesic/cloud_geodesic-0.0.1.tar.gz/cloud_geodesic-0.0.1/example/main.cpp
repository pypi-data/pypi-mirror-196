#include <fmt.hpp>

#include <matplot/matplot.h>
using namespace matplot;

int main() {
  size_t n = 1000;
  std::vector<double> x_tmp = randn(n, 0., 1.);
  std::vector<double> y_tmp = randn(n, 0., 1.);
  std::vector<Eigen::VectorXd> points;
  for (size_t i = 0; i < n; ++i) {
    Eigen::VectorXd vec(2);
    vec << x_tmp[i], y_tmp[i];
    points.push_back(vec);
  }

  auto tree = FastMarchingTree(points, 0.4);
  tree.span_tree(0.8); // extend the tree in r-neighbour
  tree.visualize();
}
