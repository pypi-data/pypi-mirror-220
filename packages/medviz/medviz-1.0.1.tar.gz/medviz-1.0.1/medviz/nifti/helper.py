from pathlib import Path

import nibabel as nib
import numpy as np

from ..utils import path_in, save_path_dir, significant_slice_idx


# add save_path to save the image (Optional)
def to_hu(file_path: str or Path):
    """
    read the image and convert it to hu image
    :param file_path: file path
    :return: hu image
    """
    file_path = path_in(file_path)
    image = nib.load(file_path)
    image_data = image.get_fdata()

    slope = image.dataobj.slope
    intercept = image.dataobj.inter

    is_hu_format = (slope == 1) and (intercept <= 0)

    if is_hu_format:
        print("The NIfTI image is in HU format.")
        hu_image = image_data
    else:
        print("The NIfTI image is not in HU format.")
        hu_image = image_data * slope + intercept

    return hu_image


# def mask(mask_data_bool: np.ndarray, affine: np.ndarray, output_path: str):
#     """
#     Save mask as nii.gz file
#     :param mask_data_bool: mask data as boolean numpy array
#     :param affine: affine matrix
#     :param output_path: output path
#     :return: None
#     """
#     mask_data = np.zeros(mask_data_bool.shape, dtype=np.int16)
#     mask_data[mask_data_bool] = 1
#     mask_img = nib.Nifti1Image(mask_data, affine)
#     nib.save(mask_img, output_path)
#     print("Mask saved at", output_path)


def boolean_mask_to_nifti(mask_data_bool: np.ndarray, affine: np.ndarray, output_path: str):
    """
    Save mask as nii.gz file
    :param mask_data_bool: mask data as boolean numpy array
    :param affine: affine matrix
    :param output_path: output path
    :return: None
    """
    mask_data = np.zeros(mask_data_bool.shape, dtype=np.int16)
    mask_data[mask_data_bool == True] = 255
    mask_data[mask_data_bool == False] = 0

    mask_img = nib.Nifti1Image(mask_data, affine)
    nib.save(mask_img, output_path)
    print("Mask saved at", output_path)


if __name__ == "__main__":
    mask_data_bool = np.array([[True, False, True], [False, True, False]])
    affine = np.eye(4)
    output_path = "mask.nii.gz"
    mask(mask_data_bool, affine, output_path)


def arr_to_nifti(arr: np.ndarray, affine: np.ndarray, output_path: str):
    """
    Save numpy array as nii.gz file
    :param arr: numpy array
    :param affine: affine matrix
    :param output_path: output path
    :return: None
    """
    arr_img = nib.Nifti1Image(arr, affine)
    nib.save(arr_img, output_path)
    print("Numpy array saved at", output_path)


def nii3d_to_nii2d(path: str or Path, output_path: str or Path, slice: None or int):
    """
    Save 3D nii file as 2D nii file
    :param path: 3D nii file path
    :param output_path: output path
    :param slice: slice number
    :return: None
    """
    image = nib.load(path)
    image_data = image.get_fdata()
    slice = slice or image_data.shape[2] // 2
    affine = image.affine
    arr_img = nib.Nifti1Image(image_data[:, :, slice], affine)
    nib.save(arr_img, output_path)
    print("2D NIfTI image saved at", output_path)


def nii3d_to_annotated2d(
    image_path: str or Path,
    mask_path: str or Path,
    output_path: str or Path,
    limit: int = 50,
):
    image_path = Path(image_path)
    name = image_path.stem
    image = nib.load(image_path)
    image_data = image.get_fdata()
    affine = image.affine

    most_value_nonzero_slices, num_nonzero_slices = significant_slice_idx(mask_path)

    num_slices = min(num_nonzero_slices, limit)

    save_path_parent = save_path_dir(output_path)

    for i in range(num_slices):
        arr_img = nib.Nifti1Image(image_data[:, :, most_value_nonzero_slices[i]], affine)
        save_path = save_path_parent / f"{name}_slice_{i}.nii.gz"
        nib.save(arr_img, save_path)


def nii_mask3d_to_2d(
    mask_path: str or Path,
    output_path: str or Path,
    limit: int = 50,
):
    mask_path = Path(mask_path)
    name = mask_path.stem
    image = nib.load(mask_path)
    mask_data = image.get_fdata()
    affine = image.affine

    most_value_nonzero_slices, num_nonzero_slices = significant_slice_idx_data(mask_data)

    num_slices = min(num_nonzero_slices, limit)

    save_path_parent = save_path_dir(output_path)

    for i in range(num_slices):
        arr_img = nib.Nifti1Image(mask_data[:, :, most_value_nonzero_slices[i]], affine)
        save_path = save_path_parent / f"{name}_slice_{i}.nii.gz"
        nib.save(arr_img, save_path)
