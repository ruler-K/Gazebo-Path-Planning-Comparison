# 基于 ROS & Gazebo 的智能小车路径规划性能评测系统
# (Performance Benchmarking of Path Planning Algorithms for Mobile Robots)

[![ROS Version](https://img.shields.io/badge/ROS-Noetic-blue)](http://wiki.ros.org/noetic)
[![Gazebo Version](https://img.shields.io/badge/Gazebo-11-orange)](https://gazebosim.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 1. 项目简介
本项目是一个基于 ROS (Robot Operating System) 和 Gazebo 物理仿真引擎的闭环导航验证平台。
项目针对智能小车在复杂室内拓扑环境（窄道、U型弯）下的自主寻径问题，对 Dijkstra和 A* 算法进行了深度的性能量化对比。

### 核心亮点：
- **实战背景**：基于第26届中国机器人及人工智能大赛全国一等奖项目经验开发。
- **深度分析**：通过实验揭示了 A* 算法在强约束环境下的“启发式陷阱”现象。
- **客观度量**：利用 Rosbag 录制底层数据，并通过 PlotJuggler 进行高频采样分析。

## 2. 效果展示
| Dijkstra 搜索范围 (圆形扩散) | A* 搜索范围 (目标导向) |
| :---: | :---: |
| ![Dijkstra](./images/dijkstra_search.png) | ![Astar](./images/astar_search.png) |

| 实际运行轨迹 (红线为平滑后的路径) | 线速度响应曲线 (PlotJuggler 导出) |
| :---: | :---: |
| ![Trajectory](./images/path_smooth.png) | ![Velocity](./images/velocity_curve.png) |

## 3. 技术架构
- **物理引擎**: Gazebo 11 (高保真室内实验室场景模型)
- **机器人模型**: TurtleBot3 - Burger (差速驱动)
- **环境感知**: Gmapping SLAM (5cm 分辨率占据栅格地图)
- **全局规划**: Dijkstra / A* (基于 8 邻域拓扑模型)
- **局部规划**: DWA (Dynamic Window Approach) 动力学平滑处理
- **数据分析**: Rosbag + PlotJuggler + rqt_reconfigure

## 4. 核心实验结论 (重要)
在复杂室内窄道环境下，实验结果打破了 A* 算法优于 Dijkstra 的传统认知：

| 指标 | Dijkstra 算法 | A* 算法 | 差异分析 |
| **平均任务耗时** | **55.4 s** | 126.1 s | A* 产生大量回溯计算 |
| **路径几何长度** | 8.35 m | 8.41 m | 基本持平 |
| **控制稳定性** | 平稳 | 剧烈震荡 | A* 贪婪路径诱发避障补偿 |

**现象分析**：A* 算法在窄道中易受到启发函数 h(n)的误导（试图撞墙寻短径），导致频繁的路径重规划和速度波动。

## 5. 快速启动

### 环境依赖
- Ubuntu 20.04
- ROS Noetic
- TurtleBot3 Packages

### 运行步骤
1. **克隆仓库**
   ```bash
   git clone https://github.com/你的用户名/Gazebo-Path-Planning-Comparison.git

（1）启动仿真世界
export TURTLEBOT3_MODEL=burger
roslaunch my_robot_nav simulation.launch
（2）启动导航系统
roslaunch my_robot_nav navigation.launch
（3）运行数据监测脚本
python3 scripts/trace_recorder.py
6. 项目结构
.
├── my_robot_nav/
│   ├── launch/      # 启动文件
│   ├── maps/        # SLAM 生成的 .yaml 和 .pgm 地图
│   ├── param/       # Dijkstra/A* 及 DWA 核心配置文件
│   ├── scripts/     # 自定义 Python 测量与轨迹记录脚本
│   └── worlds/      # Gazebo 实验室场景模型文件
└── images/          # README 引用图片





















   
