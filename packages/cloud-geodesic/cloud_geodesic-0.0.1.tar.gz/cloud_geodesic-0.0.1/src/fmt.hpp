#include <Eigen/Core>
#include <optional>

class FastMarchingTree {
public:
  FastMarchingTree(const std::vector<Eigen::VectorXd> &points, double radius);
  bool extend();
  void span_tree(std::optional<double> radius);
  std::vector<Eigen::VectorXd> get_geodesic_path(size_t idx);
  void visualize();

  std::vector<double> get_costs() { return costs_; }

private:
  std::optional<size_t> find_lowest_cost_open_node();
  std::vector<Eigen::VectorXd> points_;
  std::vector<std::optional<size_t>> parents_;
  std::vector<bool> unvisited_;
  std::vector<bool> opend_;
  std::vector<bool> closed_;
  std::vector<double> costs_;
  double radius_;
  double max_cost_;
};
