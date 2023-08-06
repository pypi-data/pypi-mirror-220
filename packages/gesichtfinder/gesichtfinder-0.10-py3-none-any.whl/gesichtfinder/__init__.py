from deepface import DeepFace
from a_cv_imwrite_imread_plus import open_image_in_cv
import pandas as pd


def cropimage(img, coords):
    return img[coords[1] : coords[3], coords[0] : coords[2]]


def get_faces(img, cut_out_faces=True, backends=("opencv", "retinaface"), **kwargs):
    r"""
    Extract faces from an image using different backend detectors and save the results in a DataFrame.

    This function utilizes the deepface library for face detection, allowing you to choose from various backend detectors
    for detecting faces in an image. The detected face regions can be optionally cropped and stored in the DataFrame.

    Parameters:
        img (str or ndarray): The path to the input image or the image's numpy array representation (RGB format).
        cut_out_faces (bool, optional): If True, the detected face regions will be cropped and stored in the DataFrame.
                                        If False, only face coordinates and attributes will be included. Default is True.
        backends (tuple, optional): A tuple containing the names of the backend detectors to use for face detection.
                                    Available backends include 'opencv' and 'retinaface'.
                                    Default is ('opencv', 'retinaface').
        **kwargs: Additional keyword arguments to be passed to the deepface.extract_faces function.
                  You can specify options like min_face_size, model, enforce_detection, and more.

    Returns:
        pandas.DataFrame: A DataFrame containing details of the detected faces and their attributes, including:
            - 'x': X-coordinate of the top-left corner of the detected face bounding box.
            - 'y': Y-coordinate of the top-left corner of the detected face bounding box.
            - 'w': Width of the detected face bounding box.
            - 'h': Height of the detected face bounding box.
            - 'end_x': X-coordinate of the bottom-right corner of the detected face bounding box.
            - 'end_y': Y-coordinate of the bottom-right corner of the detected face bounding box.
            - 'confidence': Confidence score of the face detection.
            - 'backend': The backend detector used for the detection.
            - 'faces' (optional): Cropped face regions if 'cut_out_faces' is True.

    Example:
        # Import the required libraries
        # Example usage:
        from gesichtfinder import get_faces
        df = get_faces(img=r"c:\asy.jpg", cut_out_faces=True, backends=('opencv', 'retinaface'))
        print(df)
    """
    results1 = []
    img = open_image_in_cv(img, channels_in_output=3, bgr_to_rgb=False)
    for backend in backends:
        try:
            face = DeepFace.extract_faces(
                img_path=img,
                target_size=img.shape[:2],
                detector_backend=backend,
                **kwargs,
            )

            results1.extend(
                [
                    y[1]
                    for y in [
                        [
                            fa["facial_area"],
                            {"confidence": fa["confidence"], "backend": backend},
                        ]
                        for fa in face
                    ]
                    if not y[1].update(y[0])
                ]
            )
        except Exception as fe:
            print(f"{backend}: {fe}")
    df = pd.DataFrame(results1)
    df["end_x"] = df["x"] + df["w"]
    df["end_y"] = df["y"] + df["h"]
    if cut_out_faces:
        df["faces"] = df.apply(
            lambda x: cropimage(img, coords=(x.x, x.y, x.end_x, x.end_y)), axis=1
        )
    return df
