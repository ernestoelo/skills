# Robotics Applications for Recursive Context

## ZedBox and Jetson Nano Orin NX
- **SLAM/Odometría Visual**: Process logs of 10M+ tokens by chunking timestamps, extracting depth variances >3m for air/water calibration.
- **SDK Unitree/Cyber Dog**: Analyze WebRTC streams logs, recommend focus on latency anomalies.

## Underwater Robotics (Salmon Cage Repair)
- **Arm Manipulation**: Chunk codebases by functions, extract topics on IK solvers, recommend focus on joint limits.
- **Stereo Vision (Zed 2i)**: Process video data logs, evidence full coverage of depth maps.

## Example Workflow
1. Load Zed log with `context_loader.py`.
2. Extract odometry topics with `topic_extractor.py`.
3. Recommend focus on errors <2cm with evidence.
4. Iterate for calibration factor K.

Ensures transparent, hallucination-free processing.