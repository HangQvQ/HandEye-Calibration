"""
Usage:
(calibration)$ python capture_img_pose.py

Save commands:
Click the opencv window (make sure it's in focus).

Press "s" to save one image and one pose.
Press "q" to finish data acquisition.
"""

import pyrealsense2 as rs
import numpy as np
import cv2
import DianaApi as DianaApi

def main(save_dir='handeye_img_pose'):

    def errorCallback(e):
        print("error code" + str(e))
    fnError = DianaApi.FNCERRORCALLBACK(errorCallback)
    netInfo = ('192.168.10.75', 0, 0, 0,0,0)
    DianaApi.initSrv(netInfo)
    DianaApi.releaseBrake()

    pipeline = rs.pipeline()
    config = rs.config()
    pc = rs.pointcloud()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)

    num = 0
    pose_matrix = []

    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            align_to = rs.stream.color
            align = rs.align(align_to)

            # Align the depth frame to color frame
            aligned_frames = align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()

            # Get data of depth and color are most time-consuming part -> roughly 400ms
            depth_image = np.asanyarray(aligned_depth_frame.get_data()) # (480,640)
            color_image = np.asanyarray(color_frame.get_data()) # (480,640,3)

            depth_image = np.expand_dims(depth_image, axis=2)
            depth_image = np.array(depth_image * 255, dtype=np.uint8)
            depth_image = np.concatenate((depth_image, depth_image, depth_image), axis=2)
            cv2.imshow('depth', depth_image)
            cv2.imshow('rgb', color_image)

            k = cv2.waitKey(5)

            # Press 'q' to exit the loop
            if k == ord('q'):
                break
            # wait for 's' key to save and exit
            elif k == ord('s'): 
                num += 1
                # save the image
                cv2.imwrite(save_dir + '/img' + str(num) + '.png', color_image)
                
                # get robot pose
                ipAddress='192.168.10.75'
                poses = [0.0] * 6
                DianaApi.getTcpPos(poses, ipAddress)
                pose_matrix.append(poses)

                print("saved img and pose")
            
    finally:
        # save the pose matrix
        np.save(save_dir + "/pose.npy", np.array(pose_matrix))
        pipeline.stop()

if __name__ == '__main__':
    main()