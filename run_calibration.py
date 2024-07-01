from Intrinsic_calibration import IntrinsicCalibration
from handeye_calibration import HandEyeCalibration
import cv2 as cv


def main(chessboardSize, size_of_chessboard_squares_m, eye_to_hand, frameSize=(480,640), save_dir = "handeye_img_pose"):
    # calibrate camera
    cam_calib = IntrinsicCalibration(save_dir=save_dir, 
                                     img_dir=save_dir+'/img', 
                                     chessboardSize=chessboardSize, 
                                     frameSize=frameSize, 
                                     size_of_chessboard_squares_m=size_of_chessboard_squares_m)
    cam_calib.calibrate()
    # calib.draw_pose()

    # calibrate handeye
    handeye_calib = HandEyeCalibration(save_dir=save_dir, 
                                       img_dir=save_dir + '/img', 
                                       posefile= save_dir + '/pose.npy', 
                                       eye_to_hand=eye_to_hand,
                                       chessboardSize=chessboardSize, 
                                       frameSize=frameSize, 
                                       size_of_chessboard_squares_m=size_of_chessboard_squares_m)
    handeye_calib.calibrate()
    handeye_calib.save(method=cv.CALIB_HAND_EYE_TSAI)


if __name__ == '__main__':
    #change the sizes according to your chess board
    chessboardSize=(6,9)
    size_of_chessboard_squares_m=0.04

    eye_to_hand=True

    main(chessboardSize, size_of_chessboard_squares_m, eye_to_hand)