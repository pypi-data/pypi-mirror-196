from typing import Tuple
import numpy as np
import cv2
import os

def compute3dPoint(A):
    _, _, V = np.linalg.svd(A)
    X = V[:, -1]
    X = X/X[-1]
    point3d = X[0:3]
    return point3d


def projectPoints(points3d, P):
    points3dHomog = np.vstack([points3d.T, np.ones((points3d.shape[0], 1), dtype=points3d.dtype)]).T
    points2dHomog = P @ points3dHomog.T
    isInFrontOfCamera = points2dHomog[2, :] > 0
    points2d = points2dHomog[0:2, :] / points2dHomog[2, :]
    return points2d.T, isInFrontOfCamera


def parseCameraMatrices(*args) -> Tuple[np.ndarray, np.ndarray]:
    if len(args) == 1:
        stereoParams = args[0]
        assert isinstance(stereoParams, cv2.StereoSGBM), "Invalid input stereoParams"
        cameraMatrix1 = cv2.vision.constructCameraMatrix(np.eye(3), np.array([0, 0, 0]), stereoParams.cameraMatrix1)
        cameraMatrix2 = cv2.vision.constructCameraMatrix(stereoParams.rotation, stereoParams.translation, stereoParams.cameraMatrix2)
    else:
        assert len(args) == 2, "Invalid number of input arguments"
        cameraMatrix1, cameraMatrix2 = args
        validateCameraMatrix(cameraMatrix1, 'cameraMatrix1')
        validateCameraMatrix(cameraMatrix2, 'cameraMatrix2')
    return cameraMatrix1, cameraMatrix2


def validateCameraMatrix(M, varName):
    assert M.shape == (4, 3), "Invalid shape for camera matrix."
    assert np.all(np.isfinite(M)), "Camera matrix should contain only finite values."
    assert np.all(np.isreal(M)), "Camera matrix should contain only real values."
    assert np.all(M), "Camera matrix should not contain any zero values."


def triangulate(matchedPoints1, matchedPoints2, *varargin):
    points1, points2, camMatrix1, camMatrix2 = parseInputs(matchedPoints1, matchedPoints2, *varargin)
    numPoints = points1.shape[1]
    if xyzPoints is None:
        xyzPoints = np.zeros((numPoints, 3), dtype=points1.dtype)
    scaleMatrix = np.vstack((np.tile(camMatrix1[2], (2, 1)), np.tile(camMatrix2[2], (2, 1))))
    subtractMatrix = np.vstack((camMatrix1[:2], camMatrix2[:2]))
    inputPoints = np.vstack((points1, points2))
    inputPoints = np.repeat(inputPoints.ravel(), 4).reshape(numPoints, 4, 2)
    inputPoints = (inputPoints * np.tile(scaleMatrix, (numPoints, 1))) - np.tile(subtractMatrix, (numPoints, 1))
    for i in range(numPoints):
        xyzPoints[i] = compute3dPoint(inputPoints[i])
    if len(varargin) > 0:
        if varargin[0] == 'ReprojectionErrors':
            points1proj, isInFrontOfCam1 = projectPoints(xyzPoints, camMatrix1)
            points2proj, isInFrontOfCam2 = projectPoints(xyzPoints, camMatrix2)
            errors1 = np.hypot(points1[0,:] - points1proj[0,:], points1[1,:] - points1proj[1,:])
            errors2 = np.hypot(points2[0,:] - points2proj[0,:], points2[1,:] - points2proj[1,:])
            reprojectionErrors = np.mean(np.vstack((errors1, errors2)), axis=0)
            validIndex = isInFrontOfCam1 & isInFrontOfCam2
            return xyzPoints, reprojectionErrors, validIndex
    return xyzPoints



def checker_board(P=10, N=10):
    """
    RGB test image using a checker-board pattern.

    Parameters:
        P (int): PxP pixel checkers.
        N (int): Checkers per side of image.

    Returns:
        ndarray: The checker-board image.
    """
    N = round(N)
    P = round(P)
    if P < 1:
        raise ValueError("Pixel value must be greater than 0.")

    if N == 1:
        x = np.ones((P, P))
    elif N % 2 == 1:  # odd
        block1 = np.concatenate((np.ones((P, P)), np.zeros((P, P))), axis=1)
        block2 = np.concatenate((np.zeros((P, P)), np.ones((P, P))), axis=1)
        blocks = np.concatenate((block1, block2), axis=0)
        x = np.tile(blocks, ((N-1)//2, (N-1)//2))
        x = np.concatenate((x, np.tile(np.concatenate((np.ones((P, 1)), np.zeros((P, 1))), axis=1), ((N-1)//2, 1))), axis=1)
        x = np.concatenate((x, x[0:P, :]))
    else:  # even
        block1 = np.concatenate((np.ones((P, P)), np.zeros((P, P))), axis=1)
        block2 = np.concatenate((np.zeros((P, P)), np.ones((P, P))), axis=1)
        blocks = np.concatenate((block1, block2), axis=0)
        x = np.tile(blocks, (N//2, N//2))

    D = N*P
    r = x  # Red checkers
    b = 1 - x  # Blue checkers
    g = np.arange(D)/(D-1)  # Green ramp
    g = np.repeat(g[:, np.newaxis], D, axis=1)
    return np.dstack((r, g, b))




def parse_inputs(I1, I2, **kwargs):
    r = lambda x, default: kwargs[x] if x in kwargs else default
    class Data: pass
    opt = Data()
    opt.DisparityRange = r('DisparityRange', [0, 128])
    opt.UniquenessThreshold = r('UniquenessThreshold', 15)
    return opt

def disparitySGM(I1, I2, **kwargs):
    r = parse_inputs(I1, I2, **kwargs)
    optSGM = {
        'MinDisparity': r['DisparityRange'][0],
        'NumberOfDisparities': r['DisparityRange'][1] - r['DisparityRange'][0],
        'UniquenessThreshold': r['UniquenessThreshold'],
        'Directions': 5,
        'Penalty1': 15,
        'Penalty2': 200
    }
    I1U8 = cv2.normalize(I1, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    I2U8 = cv2.normalize(I2, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    disparityMap = cv2.StereoSGBM_create(**optSGM).compute(I1U8, I2U8)
    disparityMap = disparityMap.astype(np.float32) / 16.0
    disparityMap[disparityMap == 0] = np.nan
    return disparityMap



def detectSURFFeatures(I, MetricThreshold=1000.0, NumOctaves=3, NumScaleLevels=4, ROI=None):
    gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    detector = cv2.xfeatures2d.SURF_create(hessianThreshold=MetricThreshold, nOctaves=NumOctaves, nOctaveLayers=NumScaleLevels, upright=False, extended=False)
    keypoints = detector.detect(gray, mask=None)
    
    if ROI is not None:
        x, y, w, h = ROI
        keypoints = [kp for kp in keypoints if x <= kp.pt[0] < x + w and y <= kp.pt[1] < y + h]
    pts = cv2.KeyPoint_convert(keypoints)
    return pts
#I = cv2.imread('cameraman.tif')
#pts = detectSURFFeatures(I)
#img = cv2.drawKeypoints(I, pts, None, color=(0, 255, 0), flags=cv2.DrawMatchesFlags_DEFAULT)


def epipolarLine(f, pts):
    """
    Compute epipolar lines for stereo images.

    Assuming that the fundamental matrix, F, maps points in image I1 to
    epipolar lines in image I2,

    LINES = epipolarLine(F,PTS) computes the epipolar lines in I2
    corresponding to the points, PTS, in I1.

    LINES = epipolarLine(F.T,PTS) computes the epipolar lines in I1
    corresponding to the points, PTS, in I2.

    PTS is a M-by-2 matrix, where each row contains the x and y
    coordinates of a point. M is the number of points.

    F is a 3-by-3 fundamental matrix. If P1, a point in I1, corresponds
    to P2, a point in I2, then [P2,1] * F * [P1,1]' = 0.

    LINES is a M-by-3 matrix where each row has the format [A,B,C]
    which defines a line as A * x + B * y + C = 0.

    :param f: A 3-by-3 fundamental matrix, can be double or single.
    :type f: numpy.ndarray
    :param pts: A M-by-2 matrix where each row contains the x and y coordinates of a point.
    :type pts: numpy.ndarray
    :return: A M-by-3 matrix where each row has the format [A,B,C] which defines a line as A * x + B * y + C = 0.
    :rtype: numpy.ndarray
    """

    output_dtype = pts.dtype
    check_inputs(f, pts)
    n_pts = pts.shape[0]
    lines = np.hstack((pts, np.ones((n_pts, 1), dtype=output_dtype))) @ f.T
    return lines


def check_inputs(f, pts):
    """
    Check inputs for the epipolarLine function.

    :param f: A 3-by-3 fundamental matrix, can be double or single.
    :type f: numpy.ndarray
    :param pts: A M-by-2 matrix where each row contains the x and y coordinates of a point.
    :type pts: numpy.ndarray
    """

    # Check F
    np.testing.assert_allclose(f.shape, (3, 3))
    np.testing.assert_(np.isrealobj(f))
    np.testing.assert_(np.ndim(f) == 2)

    # Check PTS
    np.testing.assert_allclose(pts.shape[1], 2)
    np.testing.assert_(np.isrealobj(pts))
    np.testing.assert_(np.ndim(pts) == 2)



def stereoCameraCalibrator(*args):
    # Check if app is running in Jupyter Notebook or not
    try:
        from IPython import get_ipython
        get_ipython().run_line_magic('gui', 'osx')
    except:
        pass

    shouldAddImages = False
    shouldOpenSession = False

    # Check the input arguments
    if len(args) == 1:
        if isinstance(args[0], str):
            # Load a saved stereo calibration session
            sessionFileName = args[0]
            sessionPath, sessionFileName = os.path.split(sessionFileName)
            sessionFileName, _ = os.path.splitext(sessionFileName)
            shouldOpenSession = True
        else:
            raise ValueError("Expected a string as the input argument for loading a saved stereo calibration session.")
    elif len(args) == 3 or len(args) == 4:
        if all(isinstance(arg, str) for arg in args[0:2]) and isinstance(args[2], (int, float)):
            # Adding images from folders
            fileNames1 = [os.path.join(args[0], f) for f in os.listdir(args[0]) if os.path.isfile(os.path.join(args[0], f))]
            fileNames2 = [os.path.join(args[1], f) for f in os.listdir(args[1]) if os.path.isfile(os.path.join(args[1], f))]

            # Check that there are the same number of files in each folder
            if len(fileNames1) != len(fileNames2):
                raise ValueError("There must be the same number of images in both folders.")
            
            fileNames = []
            for i in range(len(fileNames1)):
                fileNames.append(fileNames1[i])
                fileNames.append(fileNames2[i])
            
            squareSize = args[2]
            units = "mm" if len(args) == 3 else args[3]
            shouldAddImages = True
        else:
            raise ValueError("Invalid input arguments.")
    else:
        raise ValueError("Invalid number of input arguments.")

    # Create a new Stereo Calibrator
    tool = cv2.stereo_calib.CalibrationTool_create(True)

    if shouldAddImages:
        # Set up checkerboard detector
        detector = cv2.aruco.GridBoard_create(7, 5, squareSize, 2.5, cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250))

        # Add images to a new session
        for fileName in fileNames:
            img = cv2.imread(fileName)
            tool.addImage(detector, img)
        
        # Estimate the intrinsic and extrinsic parameters of each camera
        rms = tool.calibrate()
        
        # Display the reprojection error
        print("Reprojection error: {}".format(rms))

        # Show the extrinsic parameters
        extrinsics = tool.getExtrinsics()
        for i in range(len(extrinsics)):
            print("Rotation matrix for camera pair {}:\n{}".format(i, extrinsics[i][0]))
            print("Translation vector for camera pair {}:\n{}".format(i, extrinsics[i][1]))
        
        # Undistort the images
        stereoParams = tool.getStereoParams()
        for fileName in fileNames:
            img = cv2.imread(fileName)
            imgUndistorted = cv2.undistort(img, stereoParams[0], stereoParams[1])
            cv2.imshow(fileName, imgUndistorted)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            
