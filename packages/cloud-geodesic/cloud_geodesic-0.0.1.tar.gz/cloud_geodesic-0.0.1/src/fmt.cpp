#include "fmt.hpp"
#include "Eigen/src/Core/Matrix.h"
#include <algorithm>
#include <limits>
#include <matplot/matplot.h>
#include <optional>

using namespace matplot;

FastMarchingTree::FastMarchingTree(const std::vector<Eigen::VectorXd> &points,
                                   double radius)
    : radius_(radius), max_cost_(0) {

  size_t n = points.size();
  points_ = points;
  parents_ = std::vector<std::optional<size_t>>(n, std::nullopt);
  unvisited_ = std::vector<bool>(n, true);
  opend_ = std::vector<bool>(n, false);
  closed_ = std::vector<bool>(n, false);
  costs_ = std::vector<double>(n, std::numeric_limits<double>::infinity());

  // set the start node info
  parents_.at(0) = std::nullopt;
  unvisited_.at(0) = false;
  opend_.at(0) = true;
  costs_.at(0) = 0.0;
}

std::optional<size_t> FastMarchingTree::find_lowest_cost_open_node() {
  size_t n = points_.size();
  double min_cost_z = std::numeric_limits<double>::infinity();
  std::optional<size_t> z_idx = std::nullopt;
  for (size_t i = 0; i < n; ++i) {
    if (!opend_[i])
      continue;

    if (costs_[i] < min_cost_z) {
      min_cost_z = costs_[i];
      z_idx = i;
    }
  }
  return z_idx;
}

bool FastMarchingTree::extend() {
  size_t n = points_.size();

  auto ret = this->find_lowest_cost_open_node();
  if (ret == std::nullopt) {
    return false;
  }
  size_t z_idx = *ret;

  for (size_t x_idx = 0; x_idx < n; ++x_idx) {
    if (!unvisited_[x_idx])
      continue;

    bool is_x_close_to_z = (points_[x_idx] - points_[z_idx]).norm() < radius_;
    if (is_x_close_to_z) {

      // find an best connection from y(close to x and unvisited) to x
      double min_cost_x = std::numeric_limits<double>::infinity();
      std::optional<size_t> best_parent_idx = std::nullopt;

      for (size_t y_idx = 0; y_idx < n; ++y_idx) {
        if (!opend_[y_idx])
          continue;

        double dist_x_y = (points_[y_idx] - points_[x_idx]).norm();
        bool is_y_close_to_x = (dist_x_y < radius_);

        if (is_y_close_to_x) {

          double min_cost_x_cand = costs_[y_idx] + dist_x_y;
          if (min_cost_x_cand < min_cost_x) {
            min_cost_x = min_cost_x_cand;
            best_parent_idx = y_idx;
          }
        }
      }
      parents_[x_idx] = best_parent_idx;
      costs_[x_idx] = min_cost_x;
      opend_[x_idx] = true;
      unvisited_[x_idx] = false;

      // update the maximum cost of the tree
      max_cost_ = std::max(max_cost_, min_cost_x);
    }
  }
  opend_[z_idx] = false;
  closed_[z_idx] = true;
  return true;
}

void FastMarchingTree::span_tree(std::optional<double> radius) {
  while (this->extend()) {
    if (radius != std::nullopt && max_cost_ > radius) {
      break;
    }
  }
}

std::vector<Eigen::VectorXd> FastMarchingTree::get_geodesic_path(size_t idx) {
  std::vector<Eigen::VectorXd> path;
  std::optional<size_t> idx_current = idx;
  while (idx_current != std::nullopt) {
    path.push_back(points_[*idx_current]);
    idx_current = parents_[*idx_current];
  }
  return path;
}

void FastMarchingTree::visualize() {
  auto f = figure(true);
  f->width(f->width() * 2);
  f->height(f->height() * 2);
  f->x_position(200);
  f->y_position(100);
  f->quiet_mode(true);
  std::vector<double> x_frontier, y_frontier;
  for (size_t i = 0; i < costs_.size(); ++i) {
    if (opend_[i]) {
      x_frontier.push_back(points_[i][0]);
      y_frontier.push_back(points_[i][1]);
    }
  }
  auto scat = scatter(x_frontier, y_frontier);
  scat->color("red");
  hold(on);

  std::vector<double> x_closed, y_closed;
  for (size_t i = 0; i < costs_.size(); ++i) {
    if (closed_[i]) {
      x_closed.push_back(points_[i][0]);
      y_closed.push_back(points_[i][1]);
    }
  }
  auto scat2 = scatter(x_closed, y_closed);
  scat2->color("g");
  hold(on);

  std::vector<double> x_unvisited, y_unvisited;
  for (size_t i = 0; i < costs_.size(); ++i) {
    if (unvisited_[i]) {
      x_unvisited.push_back(points_[i][0]);
      y_unvisited.push_back(points_[i][1]);
    }
  }
  auto scat3 = scatter(x_unvisited, y_unvisited);
  scat3->color("b");
  hold(on);

  // plot edges
  for (size_t i = 0; i < costs_.size(); ++i) {
    if (parents_[i] == std::nullopt)
      continue;
    size_t parent_idx = *parents_[i];
    std::vector<double> x{points_[i][0], points_[parent_idx][0]};
    std::vector<double> y{points_[i][1], points_[parent_idx][1]};
    const auto l = plot(x, y, "-");
    l->color("black");
    hold(on);
  }

  title("Scatter plot");
  f->draw();
  show();
}
