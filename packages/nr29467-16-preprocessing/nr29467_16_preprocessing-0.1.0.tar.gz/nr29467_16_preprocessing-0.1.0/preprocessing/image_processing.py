
from pathlib import Path


import numpy as np
import scipy
import scipy.ndimage
import matplotlib.pyplot as plt
from skimage import exposure

from preprocessing.files import NPYHandler, TiffHandler, H5Handler

def adaptive_histogram_equalization(
    data: np.ndarray,
    kernel_size: np.ndarray = np.array([32, 32, 32]),
    clip_limit: float = 0.9
) -> np.ndarray:
    data = exposure.equalize_adapthist(data, kernel_size=kernel_size, clip_limit=clip_limit)
    return data

def denoise(
    data: np.ndarray,
    output_path: Path,
    sigma: float = 1.5,
):
    sample = data[data.shape[0]//2, :, :]
    fix, axs = plt.subplots(1, 2, figsize=(5, 10))
    axs[0].imshow(sample, cmap='gray')
    axs[0].set_title('original')
    # sigma_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # # create subplots
    # fig, axs = plt.subplots(1, len(sigma_vals), figsize=(1.5*len(sigma_vals),3))
    # for i, sigma in enumerate(sigma_vals):
    #     x = scipy.ndimage.gaussian_filter(
    #         sample,
    #         sigma=sigma,
    #     )
    #     axs[i].imshow(x, cmap='gray')
    #     axs[i].set_title(f'sigma={sigma}')
    #     axs[i].axis('off')
    # # save the image
    # plt.savefig('denoise_gaussian.png')
    # plt.close()
    data = scipy.ndimage.gaussian_filter(
        data,
        sigma=sigma,
    )
    after_sample = data[data.shape[0]//2, :, :]
    axs[1].imshow(after_sample, cmap='gray')
    axs[1].set_title('after')
    plt.savefig(output_path / 'denoise_gaussian.png')
    return data