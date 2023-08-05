#!/usr/bin/env python
import glob
import SimpleITK as sitk
import numpy as np
import vtk
import os


def load_nifti(nifti_file, load_image=True, load_info=True):
    img_itk = sitk.ReadImage(nifti_file)
    origin, spacing, direction = img_itk.GetOrigin(), img_itk.GetSpacing(), img_itk.GetDirection()
    img_npy = None
    if load_image:
        img_npy = sitk.GetArrayFromImage(img_itk)
    if load_info:
        if img_npy is not None:
            return img_npy, origin, spacing, direction
        else:
            return origin, spacing, direction
    else:
        return img_npy


def np2nifti(nifti_file, npy, dst_file=None, mode=None):
    """

    Args:
        mode:
        nifti_file:
        numpy: could be npy file or array
        dst_file:

    Returns:

    """
    if nifti_file.endswith('.nii.gz'):
        origin, spacing, direction = load_nifti(nifti_file, False)
        if not isinstance(npy, np.ndarray):
            npy = np.load(npy)
        if len(npy.shape) == 5 or len(npy.shape) == 4:
            npy = np.squeeze(npy)
        new_itk = sitk.GetImageFromArray(npy, isVector=False)
        new_itk.SetOrigin(origin)
        if mode == 'homogeneous':
            new_itk.SetSpacing(np.array([1.0, 1.0, 1.0]))
        else:
            new_itk.SetSpacing(spacing)
        new_itk.SetDirection(direction)
        if dst_file is None:
            dst_file = nifti_file.replace('.nii.gz', '_process.nii.gz')
        sitk.WriteImage(new_itk, dst_file)


def nifti2mesh(nifti_file, label, dst_file=None):
    """
    Read a nifti file including a binary map of a segmented organ with label id = label.
    Convert it to a smoothed mesh of type stl.
    filename_nii     : Input nifti binary map
    filename_stl     : Output mesh name in stl format
    label            : segmented label id
    """

    # read the file
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(filename_nii)
    reader.Update()

    # apply marching cube surface generation
    surf = vtk.vtkDiscreteMarchingCubes()
    surf.SetInputConnection(reader.GetOutputPort())
    surf.SetValue(0, label)  # use surf.GenerateValues function if more than one contour is available in the file
    surf.Update()

    # smoothing the mesh
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    if vtk.VTK_MAJOR_VERSION <= 5:
        smoother.SetInput(surf.GetOutput())
    else:
        smoother.SetInputConnection(surf.GetOutputPort())
    smoother.SetNumberOfIterations(30)
    smoother.NonManifoldSmoothingOn()
    # The positions can be translated and scaled
    # such that they fit within a range of [-1, 1] prior to the smoothing computation
    smoother.NormalizeCoordinatesOn()
    smoother.GenerateErrorScalarsOn()
    smoother.Update()

    # save the output
    writer = vtk.vtkSTLWriter()
    writer.SetInputConnection(smoother.GetOutputPort())
    writer.SetFileTypeToASCII()
    if dst_file is None:
        dst_file = nifti_file.replace('.nii.gz', '.stl')
    writer.SetFileName(dst_file)
    writer.Write()


if __name__ == '__main__':
    
    pass