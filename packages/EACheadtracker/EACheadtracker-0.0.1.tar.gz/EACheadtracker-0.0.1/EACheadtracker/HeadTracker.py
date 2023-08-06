'''
Head tracker via face landmarks recognition (Google's MediaPipe - face_mesh)

'''
import sys
import socket
import cv2
import click
import numpy as np
import mediapipe as mp
from EACheadtracker.face_geometry import get_metric_landmarks, PCF, procrustes_landmark_basis


def start(input_id=0, port=5555, width=640, height=480, cam_rotation=0):
    """
    Head tracker via face landmarks recognition.
    ---------------------------------------------
    EAC-UFSM
    """
    # Initialize UDP server ---------------------------------------------------------
    global rotation_vector, translation_vector
    global s, IP, PORT
    IP = '127.0.0.1'  # Symbolic name meaning all available interfaces
    PORT = port       # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # OpenCV config -----------------------------------------------------------------
    frame_height, frame_width, _ = (height, width, 3)
    cap = cv2.VideoCapture(input_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    _, image = cap.read()
    frame_height, frame_width, _ = image.shape

    # cap.set(cv2.CAP_PROP_FPS, 120)
    # speed up initialization perception
    image = np.zeros((frame_height, frame_width))
    window_name = f'Head tracker -- [IP:{IP}, PORT:{PORT}]'  # Window name
    cv2.imshow(window_name, image)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    # Select the mechanism to quit the window according to the OS
    winOS = ['win32', 'cygwin']
    if sys.platform in winOS:
        kill_on_x = True  # add option to use mouse to quit (checks the current 'window state')
    else:
        kill_on_x = False  # only allow to quit using "Esc"

    # Tracking setup ---------------------------------------------------------------
    points_idx = [33, 263, 61, 291, 199]  # [k for k in range(0,468)]
    points_idx = points_idx + [key for (key, val) in procrustes_landmark_basis]
    points_idx = list(set(points_idx))
    points_idx.sort()
    # pseudo camera internals
    focal_length = frame_width
    center = (frame_width / 2, frame_height / 2)
    camera_matrix = np.array([[focal_length, 0, center[0]],
                              [0, focal_length, center[1]],
                              [0, 0, 1]], dtype="double")
    dist_coeff = np.zeros((4, 1))

    pcf = PCF(near=1, far=10000, frame_height=frame_height, frame_width=frame_width, fy=camera_matrix[1, 1])
    mp_face_mesh = mp.solutions.face_mesh
    # mp_drawing = mp.solutions.drawing_utils  # use mediapipe internal drawings

    # Live Tracking --------------------------------------------------------------------------
    with mp_face_mesh.FaceMesh(min_detection_confidence=0.5,
                               min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Flip image vertically if required
            if cam_rotation == 180:
                image = cv2.rotate(image, cv2.ROTATE_180)
            # Flip image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                landmarks = np.array([(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark])
                landmarks = landmarks.T

                metric_landmarks, pose_transform_mat = get_metric_landmarks(landmarks.copy(), pcf)
                model_points = metric_landmarks[0:3, points_idx].T
                image_points = landmarks[0:2, points_idx].T * np.array([frame_width, frame_height])[None, :]

                success, rotation_vector, translation_vector = cv2.solvePnP(model_points,
                                                                            image_points,
                                                                            camera_matrix,
                                                                            dist_coeff,
                                                                            flags=cv2.SOLVEPNP_ITERATIVE)

                (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 25.0)]),
                                                                 rotation_vector,
                                                                 translation_vector,
                                                                 camera_matrix,
                                                                 dist_coeff)

                for ii in points_idx:  # range(landmarks.shape[1]):
                    pos = np.array((frame_width * landmarks[0, ii],
                                    frame_height * landmarks[1, ii])).astype(np.int32)
                    image = cv2.circle(image, tuple(pos), 2, (0, 255, 0), -1)

                    p1 = (int(image_points[0][0]), int(image_points[0][1]))
                    p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

                    image = cv2.arrowedLine(image, p1, p2, (0, 0, 200), 2)

                # UDP Listening to ports
                coords = send_to_server()
                coords = np.round(coords)

                # Draw yaw, pitch and roll in the top left corner
                image = cv2.putText(image, str(coords[:3]), (00, 30), cv2.LINE_AA, 0.6,
                                    (255, 40, 0), 2, cv2.LINE_AA)

                image = cv2.putText(image, str(coords[3:]), (00, 90), cv2.LINE_AA, 0.6,
                                    (0, 100, 200), 2, cv2.LINE_AA)

            # Open window: show image
            cv2.imshow(window_name, image)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

            # Kill it when you press "Esc"
            if cv2.waitKey(5) & 0xFF == 27:
                break
            # Kill it when you mouse click 'quit window'
            if kill_on_x and cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
    print('Goodbye!')
    cv2.destroyAllWindows()
    cap.release()


def get_head_orientation():
    rvec = rotation_vector
    tvec = translation_vector
    rmat = cv2.Rodrigues(rvec)[0]
    P = np.hstack((rmat, tvec))  # projection matrix

    # find euler angles
    euler_angles = cv2.decomposeProjectionMatrix(P)[6]
    pitch = -euler_angles.item(0)
    yaw = -euler_angles.item(1)
    roll = euler_angles.item(2)

    # Ajust coordinate ranges
    if pitch < 0:
        pitch = 180 + pitch
    else:
        pitch = pitch - 180

    tx = tvec.item(0)
    ty = tvec.item(2)
    tz = tvec.item(1)
    txt = f'{yaw},{pitch},{roll},{tx},{ty},{tz}'
    data = [yaw, pitch, roll, tx, ty, tz]
    return txt, data


def send_to_server():
    try:
        coords, data = get_head_orientation()
        s.sendto(coords.encode(), (IP, PORT))
        return data
    except Exception:
        print('Sending UDP failed!')


@click.command()
@click.option('--input_id', '-i', default=0, help="Index of the camera input, (Default: 0)", multiple=False, type=int)
@click.option('--port', '-p', default=5555, help="UDP output port, (Default: 5555)", multiple=False, type=int)
@click.option('--width', '-w', default=640, help="Image width, (Default: 640)", multiple=False, type=int)
@click.option('--height', '-h', default=480, help="Image height, (Default: 480)", multiple=False, type=int)
@click.option('--cam_rotation', '-r', default=0, help="Camera rotation, either 0 or 180 (Default: 0)", multiple=False, type=int)
def cmd_start(input_id, port, height, width, cam_rotation):
    start(input_id, port, height, width, cam_rotation)


if __name__ == "__main__":
    try:
        cmd_start()
    except:
        start(0, 5555, 640, 420, 0)

