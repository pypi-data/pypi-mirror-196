import numpy as np
from scipy.stats import entropy as scipy_entropy
from skimage.color import gray2rgb, rgb2gray
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import sobel
from scipy import ndimage as ndi
from scipy.signal import convolve2d
from skimage.morphology import binary_dilation, binary_erosion
from scipy.ndimage import binary_fill_holes
from scipy import ndimage
from skimage.morphology import binary_dilation, dilation, square
import os
import urllib.request
from PIL import Image
import os
import matplotlib.pyplot as plt
from urllib.request import urlopen
from io import BytesIO
import numpy as np
from PIL import Image




#------------------------------------------------ BASIC---------------------------------
def imread(fname, as_gray=False):
    """Load an image from file.

    Parameters
    ----------
    fname : str or pathlib.Path
        Image file name, e.g. ``test.jpg`` or URL.
    as_gray : bool, optional
        If True, convert color images to gray-scale (64-bit floats).
        Images that are already in gray-scale format are not converted.

    Returns
    -------
    img_array : ndarray
        The different color bands/channels are stored in the
        third dimension, such that a gray-image is MxN, an
        RGB-image MxNx3 and an RGBA-image MxNx4.

    """
    if os.path.isfile(fname):
        img = Image.open(fname)
    else:
        with urllib.request.urlopen(fname) as url:
            img = Image.open(url)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if as_gray:
        img = img.convert('L')
    return np.array(img)




def imshow(arr):
    """Display an image.

    Parameters
    ----------
    arr : ndarray or str
        Image data or name of image file.

    """
    if isinstance(arr, str):
        if os.path.isfile(arr):
            with Image.open(arr) as img:
                arr = np.array(img)
        else:
            with urlopen(arr) as url:
                with Image.open(BytesIO(url.read())) as img:
                    arr = np.array(img)
    plt.imshow(arr)
    plt.show()



def imsave(fname, arr, check_contrast=True):
    """Save an image to file using OpenCV.

    Parameters
    ----------
    fname : str or pathlib.Path
        Target filename.
    arr : ndarray of shape (M,N) or (M,N,3) or (M,N,4)
        Image data.
    check_contrast : bool, optional
        Check for low contrast and print warning (default: True).

    Notes
    -----
    When saving a JPEG, the compression ratio may be controlled using the
    ``quality`` keyword argument which is an integer with values in [1, 100]
    where 1 is worst quality and smallest file size, and 100 is best quality
    and largest file size (default 75). This is only available when using
    the PIL and imageio plugins.
    """
    if isinstance(fname, pathlib.Path):
        fname = str(fname.resolve())

    if arr.dtype == bool:
        warn(f'{fname} is a boolean image: setting True to 255 and False to 0. '
             'To silence this warning, please convert the image using '
             'img_as_ubyte.', stacklevel=2)
        arr = arr.astype('uint8') * 255

    if check_contrast and is_low_contrast(arr):
        warn(f'{fname} is a low contrast image')

    cv2.imwrite(fname, arr)


#-----------------------------------------------------------------MAIN-------------------------------------------

def entropy(I):
    # convert input to uint8 if it's not already
    if I.dtype != 'uint8':
        I = np.uint8(I)
    # calculate histogram counts
    p, _ = np.histogram(I, bins=np.arange(257))
    # remove zero entries in p
    p = p[p != 0]
    # normalize p so that sum(p) is one
    p = p / np.sum(p)
    # calculate entropy using scipy.stats.entropy
    E = scipy_entropy(p, base=2)
    return E

def gray2ind(I, n=64):
    """
    Convert intensity image to indexed image with colormap GRAY(n).
    """
    # Check input image
    if not np.issubdtype(I.dtype, np.floating) and not np.issubdtype(I.dtype, np.integer):
        raise ValueError("Input image must be a floating point or integer array.")

    # Check colormap size
    if n < 1 or n > 65536:
        raise ValueError("Colormap size must be an integer between 1 and 65536.")

    # Convert input image to grayscale
    if I.ndim == 3:
        I = rgb2gray(I)

    # Scale image to [0, 1] range
    I = (I - np.min(I)) / (np.max(I) - np.min(I))

    # Convert to indexed image
    X = np.round((n - 1) * I).astype(np.uint16)

    # Create grayscale colormap
    map = np.linspace(0, 1, n)[:, np.newaxis] * np.ones((1, 3))

    return X, map


def imgradient(*args):
    '''
    Note that this code uses NumPy and SciPy libraries for array manipulation and convolution operations.
    The code first checks the number of input arguments and determines if the input is an image or directional gradients. 
    It then checks the method and applies the appropriate convolution kernel to compute the directional gradients. 
    Finally, it calculates the gradient magnitude and direction using the hypot and arctan2 functions, respectively.
    '''
    method_list = ["sobel", "prewitt", "central", "intermediate", "roberts"]
    num_inputs = len(args)
    if num_inputs == 1:
        img = np.array(args[0])
        if img.ndim == 3:
            img = np.mean(img, axis=2)
        method = "sobel"
    elif num_inputs == 2:
        Gx = np.array(args[0])
        Gy = np.array(args[1])
        img = None
        method = "custom"
    else:
        raise ValueError("Incorrect number of inputs.")

    if num_inputs == 2 or (num_inputs == 1 and isinstance(args[0], str)):
        method = args[-1].lower()
        if method not in method_list:
            raise ValueError("Invalid method.")

    if method == "roberts":
        if img is not None:
            img = img.astype(float)
            Gx = ndimage.convolve(img, np.array([[1, 0], [0, -1]]), mode="nearest")
            Gy = ndimage.convolve(img, np.array([[0, 1], [-1, 0]]), mode="nearest")
        Gdir = np.zeros_like(Gx)
        xy_nonzero = np.logical_or(Gx != 0, Gy != 0)
        Gdir[xy_nonzero] = np.arctan2(Gy[xy_nonzero], -Gx[xy_nonzero]) - np.pi / 4
        Gdir[Gdir < -np.pi] += 2 * np.pi
        Gdir[Gdir > np.pi] -= 2 * np.pi
    else:
        if img is not None:
            img = img.astype(float)
            Gx, Gy = np.gradient(img)
        if method == "sobel":
            kernel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        elif method == "prewitt":
            kernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
        elif method == "central":
            kernel = np.array([[-0.5, 0, 0.5]])
        elif method == "intermediate":
            kernel = np.array([[-1, 1]])
        Gx = ndimage.convolve(Gx, kernel.T, mode="nearest")
        Gy = ndimage.convolve(Gy, kernel, mode="nearest")
        Gmag = np.hypot(Gx, Gy)
        Gdir = np.arctan2(Gy, Gx)

    return Gmag, np.rad2deg(Gdir)


def gradientweight(I, sigma=1.5, rolloffFactor=3, weightCutoff=0.25):
    """
    Calculate weights for image pixels based on image gradient.

    Args:
        I (ndarray): Input image.
        sigma (float): Standard deviation for the derivative of Gaussian kernel.
                       Default value is 1.5.
        rolloffFactor (float): Positive scalar that controls how fast the output
                               weight falls as the function of gradient magnitude.
                               High value of this parameter means that the output
                               weight values will fall off sharply at the edges of
                               smooth regions, whereas low value of this parameter
                               would allow a more gradual falloff at the edges.
                               Value in the range [0.5 4] are useful for this
                               parameter. Default value is 3.
        weightCutoff (float): Positive scalar in the range [1e-3 1]. This
                              parameter puts a hard threshold on the weight values,
                              and strongly suppresses any weight values less than K
                              by setting them to a small constant value (1e-3).
                              When the output weight array W is used for Fast
                              Marching Method based segmentation (as input to
                              IMSEGFMM), this parameter can be useful in improving
                              the accuracy of the segmentation output. Default
                              value is 0.25.

    Returns:
        ndarray: Output weight array W.

    Raises:
        ValueError: If input image I is not of one of the following classes:
                    uint8, int8, uint16, int16, uint32, int32, single, or double.

    Notes:
        Double-precision floating point operations are used for internal computations for all
        classes of I, except when I is of class single in which case single-precision floating
        point operations are used internally.
    """
    if not isinstance(I, (np.uint8, np.int8, np.uint16, np.int16, np.uint32, np.int32, np.single, np.double)):
        raise ValueError("Input image must be of one of the following classes: uint8, int8, uint16, int16, uint32, int32, single, or double.")

    if I.ndim == 2:
        I = I[..., np.newaxis]
    
    if I.dtype == np.uint8:
        I = I.astype(np.double)/255
    elif I.dtype == np.single:
        I = I.astype(np.float32)
    else:
        I = I.astype(np.double)
    
    smoothed = gaussian_filter(I, sigma=sigma, mode='constant')
    gradient = sobel(smoothed, axis=-1, mode='constant')
    magnitude = np.sqrt(np.sum(gradient**2, axis=-1))
    
    minW, maxW = np.min(magnitude), np.max(magnitude)
    
    if np.isclose(maxW - minW, 0):
        # Constant intensity
        W = np.ones_like(magnitude)
    else:
        W = magnitude**(1/rolloffFactor)
        W = np.clip(W, weightCutoff, 1)
        W = (W - weightCutoff) / (1 - weightCutoff)
        W = W * (maxW - minW) + minW
    
    return W



def watershed(image, connectivity=None):
    if connectivity is None:
        if image.ndim == 2:
            connectivity = 8
        else:
            connectivity = ndi.generate_binary_structure(image.ndim, 1)

    distance = ndi.distance_transform_edt(image)
    local_maxi = ndi.maximum_filter(image, footprint=connectivity)==image
    markers = ndi.label(local_maxi)[0]
    labels = ndi.watershed(-distance, markers, mask=image)

    return labels



def std2(a):
    # validate that our input is valid for the IMHIST optimization
    fast_data_type = isinstance(a, (np.bool_, np.int8, np.uint8, np.int16, np.uint16))

    # only use IMHIST for images of sufficient size
    big_enough = {
        np.bool_: 2e4,
        np.int8: 2e5,
        np.uint8: 2e5,
        np.int16: 5e5,
        np.uint16: 4e5
    }

    if fast_data_type and not isinstance(a, np.ndarray) and a.size > big_enough[type(a)]:
        # compute histogram
        if isinstance(a, np.bool_):
            num_bins = 2
        else:
            data_type = a.dtype
            num_bins = np.int64(np.iinfo(data_type).max) - np.int64(np.iinfo(data_type).min) + 1

        bin_counts, bin_values = np.histogram(a, bins=num_bins)

        # compute standard deviation
        total_pixels = a.size

        sum_of_pixels = np.sum(bin_counts * bin_values)
        mean_pixel = sum_of_pixels / total_pixels

        bin_value_offsets = bin_values - mean_pixel
        bin_value_offsets_sqrd = bin_value_offsets ** 2

        offset_summation = np.sum(bin_counts * bin_value_offsets_sqrd)
        s = np.sqrt(offset_summation / total_pixels)

    else:
        # use simple implementation
        if a.dtype != np.float32 and a.dtype != np.float64:
            a = a.astype(np.float64)
        s = np.std(a.flatten())

    return s


def ellipse(r, c, r_radius, c_radius, shape=None, rotation=0.):
    center = np.array([r, c])
    radii = np.array([r_radius, c_radius])
    rotation = rotation % np.pi

    r_radius_rot = abs(r_radius * np.cos(rotation)) + c_radius * np.sin(rotation)
    c_radius_rot = abs(c_radius * np.cos(rotation)) + r_radius * np.sin(rotation)

    if shape is None:
        r_min = np.floor(r - r_radius_rot)
        r_max = np.ceil(r + r_radius_rot)
        c_min = np.floor(c - c_radius_rot)
        c_max = np.ceil(c + c_radius_rot)
    else:
        r_min = 0
        r_max = shape[0]
        c_min = 0
        c_max = shape[1]

    rr, cc = np.meshgrid(np.arange(r_min, r_max), np.arange(c_min, c_max), indexing='ij')
    ellipse_mask = ((rr - r)**2 / r_radius_rot**2 + (cc - c)**2 / c_radius_rot**2) <= 1

    rr = rr[ellipse_mask].astype(np.int64)
    cc = cc[ellipse_mask].astype(np.int64)

    return rr, cc

def _ellipse_in_shape(shape, center, radii, rotation=0.):
    """Generate coordinates of points within ellipse bounded by shape.

    Parameters
    ----------
    shape :  iterable of ints
        Shape of the input image.  Must be at least length 2. Only the first
        two values are used to determine the extent of the input image.
    center : iterable of floats
        (row, column) position of center inside the given shape.
    radii : iterable of floats
        Size of two half axes (for row and column)
    rotation : float, optional
        Rotation of the ellipse defined by the above, in radians
        in range (-PI, PI), in contra clockwise direction,
        with respect to the column-axis.

    Returns
    -------
    rows : iterable of ints
        Row coordinates representing values within the ellipse.
    cols : iterable of ints
        Corresponding column coordinates representing values within the ellipse.
    """
    r_lim, c_lim = np.ogrid[0:float(shape[0]), 0:float(shape[1])]
    r_org, c_org = center
    r_rad, c_rad = radii
    rotation %= np.pi
    sin_alpha, cos_alpha = np.sin(rotation), np.cos(rotation)
    r, c = (r_lim - r_org), (c_lim - c_org)
    distances = ((r * cos_alpha + c * sin_alpha) / r_rad) ** 2 \
                + ((r * sin_alpha - c * cos_alpha) / c_rad) ** 2
    rr, cc = np.where(distances < 1)
    return rr, cc
import numpy as np

def ellipsoid_stats(a, b, c):
    """
    Calculates analytical surface area and volume for ellipsoid with
    semimajor axes aligned with grid dimensions of specified `spacing`.

    Parameters
    ----------
    a : float
        Length of semimajor axis aligned with x-axis.
    b : float
        Length of semimajor axis aligned with y-axis.
    c : float
        Length of semimajor axis aligned with z-axis.

    Returns
    -------
    vol : float
        Calculated volume of ellipsoid.
    surf : float
        Calculated surface area of ellipsoid.

    """
    if any(axis <= 0 for axis in (a, b, c)):
        raise ValueError('Parameters a, b, and c must all be > 0')

    # Calculate volume & surface area
    # Surface calculation requires a >= b >= c and a != c.
    a, b, c = sorted((a, b, c), reverse=True)
    if a == c:
        raise ValueError('Parameters a and c must be different')

    # Volume
    vol = 4 / 3. * np.pi * a * b * c

    # Analytical ellipsoid surface area
    phi = np.arcsin(np.sqrt(1 - c**2 / a**2))
    d = np.sqrt(a**2 - c**2)
    m = a**2 * (b**2 - c**2) / (b**2 * (a**2 - c**2))
    F = ellip_F(phi, m)
    E = ellip_E(phi, m)

    surf = 2 * np.pi * (c**2 +
                        b * c**2 / d * F +
                        b * d * E)

    return vol, surf



def stdfilt(I, h=np.ones((3, 3))):
    """
    Local standard deviation of an image.

    Parameters
    ----------
    I : array_like
        Input image.
    h : array_like, optional
        Neighborhood of the filter. The default is a 3-by-3 neighborhood.

    Returns
    -------
    J : ndarray
        Output image containing the standard deviation value of the
        neighborhood around each pixel in the input image.

    Notes
    -----
    For pixels on the borders of the input image, symmetric padding is used.
    In symmetric padding, the values of padding pixels are a mirror reflection
    of the border pixels in the input image.

    If the input image contains NaNs or infinite values, the behavior of
    stdfilt is undefined. Propagation of NaNs or infinite values may not be
    localized to the neighborhood around the NaN/infinite value pixel.

    Examples
    --------
    >>> from scipy import misc
    >>> I = misc.imread('circuit.tif')
    >>> J = stdfilt(I)
    >>> plt.imshow(I, cmap='gray')
    >>> plt.show()
    >>> plt.imshow(J, cmap='gray', vmin=0, vmax=255)
    >>> plt.show()
    """

    # Check input arguments
    if not isinstance(I, (np.ndarray, np.generic)) or I.dtype.char not in np.typecodes['AllFloat'] + np.typecodes['AllInteger']:
        raise TypeError('I must be a real-valued numeric or logical array.')
    if not isinstance(h, (np.ndarray, np.generic)) or h.dtype.char not in np.typecodes['AllFloat'] + np.typecodes['AllInteger']:
        raise TypeError('h must be a numeric or logical array.')
    if I.ndim < h.ndim:
        raise ValueError('h has too many dimensions.')

    # Pad input image symmetrically
    pad_width = [(1, 1) if i < I.ndim else (0, 0) for i in range(h.ndim)]
    I_padded = np.pad(I, pad_width, 'symmetric')

    # Compute local standard deviation using convolution
    J = np.sqrt(convolve2d(I_padded**2, h, mode='valid') -
                convolve2d(I_padded, h, mode='valid')**2 / h.size)
    
    return J



def boundarymask(L, conn=8):
    """
    Find region boundaries of segmentation
    
    Args:
    - L: ndarray, input label matrix or binary image
    - conn: int, connectivity of pixels. 4 or 8
    
    Returns:
    - BW: ndarray, logical mask which is true at boundary locations and false at non-boundary locations
    """
    
    # Validate input
    assert L.ndim == 2, "Input must be a 2D matrix"
    assert conn in [4, 8], "Invalid connectivity. Must be 4 or 8."
    
    # Define structuring element
    if conn == 4:
        se = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]], dtype=bool)
    else:
        se = np.ones((3, 3), dtype=bool)
        
    # Dilate and erode input matrix
    dilated = binary_dilation(L, selem=se)
    eroded = binary_erosion(L, selem=se)
    
    # Find boundaries
    BW = (dilated > L) | (eroded < L)
    
    return BW.astype(bool)



def imfill(input_image, locations=None, conn=None):
    if locations is not None:
        # Starting from the points specified in locations
        if isinstance(locations, np.ndarray) and locations.ndim == 2:
            seed_coords = tuple(locations.T.tolist())
        else:
            seed_coords = np.unravel_index(locations, input_image.shape)
        filled_image = np.zeros_like(input_image)
        for coord in seed_coords:
            filled_image |= binary_fill_holes(input_image == input_image[coord], conn)
    else:
        # Fill holes or regions based on input image type
        if np.issubdtype(input_image.dtype, np.floating):
            filled_image = np.where(input_image > 0, 1, 0)
        else:
            filled_image = binary_fill_holes(input_image, conn)
    return filled_image


def imdilate(A, se, *args):
    if isinstance(se, np.ndarray):
        se = square(se)
    if A.dtype == bool:
        B = binary_dilation(A, se)
    else:
        B = dilation(A, se)
    return B



def imerode(A, se, *args):
    """
    Erode image.

    IM2 = IMERODE(IM,SE) erodes the grayscale, binary, or packed binary image
    IM, returning the eroded image, IM2. SE is a structuring element
    object, or array of structuring element objects, returned by the
    STREL or OFFSETSTREL functions.

    If IM is logical and the structuring element is flat, IMERODE
    performs binary erosion; otherwise it performs grayscale erosion.  If
    SE is an array of structuring element objects, IMERODE performs
    multiple erosions of the input image, using each structuring element
    in succession.

    IM2 = IMERODE(IM,NHOOD) erodes the image IM, where NHOOD is an array
    of 0s and 1s that specifies the structuring element.  This is
    equivalent to the syntax IMERODE(IM,STREL(NHOOD)).  IMERODE uses this
    calculation to determine the center element, or origin, of the
    neighborhood:  FLOOR((SIZE(NHOOD) + 1)/2).

    IM2 = IMERODE(IM,SE,PACKOPT,M) or IMERODE(IM,NHOOD,PACKOPT,M) specifies
    whether IM is a packed binary image and, if it is, provides the row
    dimension, M, of the original unpacked image.  PACKOPT can have
    either of these values:

        'ispacked'    IM is treated as a packed binary image as produced
                      by BWPACK.  IM must be a 2-D uint32 array and SE
                      must be a flat 2-D structuring element.  If the
                      value of PACKOPT is 'ispacked', SHAPE must be
                      'same'.

        'notpacked'   IM is treated as a normal array.  This is the
                      default value.

    If PACKOPT is 'ispacked', you must specify a value for M.

    IM2 = IMERODE(...,SHAPE) determines the size of the output image.
    SHAPE can have either of these values:

        'same'        Make the output image the same size as the input
                      image.  This is the default value.  If the value of
                      PACKOPT is 'ispacked', SHAPE must be 'same'.

        'full'        Compute the full erosion.

    Class Support
    -------------
    IM can be numeric or logical and it can be of any dimension.  If IM is
    logical and the structuring element is flat, then output will be
    logical; otherwise the output will have the same class as the input. If
    the input is packed binary, then the output is also packed binary.
    """

    if len(args) == 0:
        return ndimage.morphology.binary_erosion(A, se)
    elif len(args) == 1:
        packopt = args[0]
        return ndimage.morphology.binary_erosion(A, se, packopt=packopt)
    elif len(args) == 2:
        packopt, M = args
        return ndimage.morphology.binary_erosion(A, se, packopt=packopt, M=M)
    elif len(args) == 3:
        packopt, M, shape = args
        return ndimage.morphology.binary_erosion(A, se, packopt=packopt

                                                 

def imfindcircles(image, radius, **kwargs):
    if isinstance(radius, (int, float)):
        radius = (radius, radius)
    method = kwargs.get('Method', 'PhaseCode')
    sensitivity = kwargs.get('Sensitivity', 0.85)
    edge_threshold = kwargs.get('EdgeThreshold', None)
    object_polarity = kwargs.get('ObjectPolarity', 'bright')
    if object_polarity == 'bright':
        threshold_type = cv2.THRESH_BINARY_INV
    else:
        threshold_type = cv2.THRESH_BINARY
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if image.dtype == np.uint8:
        image = image.astype(np.float32) / 255
    elif image.dtype == np.uint16:
        image = image.astype(np.float32) / 65535
    elif image.dtype == np.int16:
        image = image.astype(np.float32) / 32767
    if edge_threshold is None:
        _, image = cv2.threshold(image, 0, 1, cv2.THRESH_OTSU)
        edge_threshold = 0.4 * np.max(image)
    else:
        _, image = cv2.threshold(image, 0, 1, threshold_type)
    dp = 1
    minDist = 1
    param1 = edge_threshold
    param2 = sensitivity
    minRadius = int(round(radius[0]))
    maxRadius = int(round(radius[1]))
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp, minDist,
                               param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)
    if circles is None:
        return np.empty((0, 2)), np.empty((0, 1)), np.empty((0, 1))
    centers = np.round(circles[0, :, :2]).astype(np.int32)
    radii = np.round(circles[0, :, 2]).astype(np.int32)
    metric = circles[0, :, 3]
    sort_idx = np.argsort(metric)[::-1]
    centers = centers[sort_idx, :]
    radii = radii[sort_idx]
    metric = metric[sort_idx]
    return centers, radii, metric


def imopen(A, se):
    # Convert the input image to a numpy array
    A = np.asarray(A)

    # Validate input arguments
    if not np.issubdtype(A.dtype, np.integer) and not np.issubdtype(A.dtype, np.bool):
        raise ValueError('Input image must be of integer or boolean type')
    if len(A.shape) < 2:
        raise ValueError('Input image must have at least two dimensions')
    if not isinstance(se, np.ndarray) or se.ndim != 2:
        raise ValueError('Structuring element must be a 2D numpy array')

    # Perform morphological opening
    eroded = ndimage.morphology.binary_erosion(A, se)
    opened = ndimage.morphology.binary_dilation(eroded, se)

    # Return the output image with the same type as the input image
    if np.issubdtype(A.dtype, np.integer):
        return np.asarray(opened, dtype=A.dtype)
    else:
        return opened

                                                 


def imnoise(a, code, p3=None, p4=None):
    # Convert input to floating point image
    a = a.astype(np.float)

    # Check the noise type and add noise accordingly
    if code == 'gaussian':
        mean = 0 if p3 is None else p3
        var = 0.01 if p4 is None else p4
        a = random_noise(a, mode='gaussian', mean=mean, var=var)
    elif code == 'localvar':
        if p4 is None:
            a = random_noise(a, mode='localvar', local_vars=p3)
        else:
            a = random_noise(a, mode='localvar', local_vars=p4, clip=False)
    elif code == 'poisson':
        a = np.random.poisson(a * 1e12) / 1e12
    elif code == 'salt & pepper':
        d = 0.05 if p3 is None else p3
        a = random_noise(a, mode='s&p', amount=d)
    elif code == 'speckle':
        var = 0.05 if p3 is None else p3
        noise = np.random.normal(loc=0.0, scale=var**0.5, size=a.shape)
        a = a + a * noise

    # Convert back to the original data type and return the noisy image
    a = np.clip(a, 0, 1)
    return (a * np.iinfo(a.dtype).max).astype(a.dtype)

                                                 
                                                 

def imreconstruct(marker, mask, conn=None):
    if conn is None:
        conn = ndimage.generate_binary_structure(marker.ndim, 1)
    if np.any(np.isnan(marker)) or np.any(np.isnan(mask)):
        raise ValueError("Input images must not contain NaN values.")
    if not np.all(np.isfinite(marker)) or not np.all(np.isfinite(mask)):
        raise ValueError("Input images must not contain infinite values.")
    if not np.issubdtype(marker.dtype, np.integer) and not np.issubdtype(marker.dtype, np.bool_) and not np.issubdtype(marker.dtype, np.floating):
        raise ValueError("Input images must be nonsparse numeric (including uint64 or int64) or logical arrays with the same class and any dimension.")
    if not np.issubdtype(mask.dtype, np.integer) and not np.issubdtype(mask.dtype, np.bool_) and not np.issubdtype(mask.dtype, np.floating):
        raise ValueError("Input images must be nonsparse numeric (including uint64 or int64) or logical arrays with the same class and any dimension.")
    if marker.shape != mask.shape:
        raise ValueError("Marker and mask must be the same size.")
    if not np.all(marker <= mask):
        raise ValueError("All elements in marker must be less than or equal to the corresponding elements in mask.")
    if np.issubdtype(marker.dtype, np.floating) or np.issubdtype(mask.dtype, np.floating):
        out_dtype = np.promote_types(marker.dtype, mask.dtype)
    else:
        out_dtype = np.result_type(marker.dtype, mask.dtype)
    return ndimage.morphology.reconstruction(marker.astype(out_dtype), mask.astype(out_dtype), conn)

                                                 
                                                 

def imregister(moving, fixed, transformtype, optimizer, metric, *args, **kwargs):
    if len(args) > 0 or len(kwargs) > 0:
        raise NotImplementedError('Optional input arguments are not implemented.')
    
    # Check input arguments
    if transformtype not in ['translation', 'rigid', 'similarity', 'affine']:
        raise ValueError('Invalid transformtype.')
    
    # Get the dimensionality of the input images
    ndim = len(moving.shape)
    
    # Initialize the transformation object
    if transformtype == 'translation':
        tform = transform.SimilarityTransform(translation=np.zeros(ndim))
    elif transformtype == 'rigid':
        tform = transform.SimilarityTransform(rotation=0, translation=np.zeros(ndim))
    elif transformtype == 'similarity':
        tform = transform.SimilarityTransform(scale=1, rotation=0, translation=np.zeros(ndim))
    elif transformtype == 'affine':
        tform = transform.AffineTransform(scale=(1,)*ndim, rotation=0, shear=0, translation=np.zeros(ndim))
    
    # Perform registration
    tform = transform.match_histograms(moving, fixed, multichannel=False, inverse=True) + tform
    tform = transform.optimize(tform, moving, fixed, optimizer, metric)
    moving_reg = transform.warp(moving, tform.inverse)
    
    # Get the spatial referencing objects
    r_fixed = None
    r_moving = None
    if isinstance(fixed, np.ndarray):
        if ndim == 2:
            r_fixed = transform.SimilarityTransform(scale=1, rotation=0, translation=(0, 0))
        elif ndim == 3:
            r_fixed = transform.AffineTransform(scale=(1, 1, 1), rotation=np.zeros(3), shear=np.zeros((3, 3)), translation=(0, 0, 0))
    else:
        r_fixed = fixed
    
    if isinstance(moving, np.ndarray):
        if ndim == 2:
            r_moving = transform.SimilarityTransform(scale=1, rotation=0, translation=(0, 0))
        elif ndim == 3:
            r_moving = transform.AffineTransform(scale=(1, 1, 1), rotation=np.zeros(3), shear=np.zeros((3, 3)), translation=(0, 0, 0))
    else:
        r_moving = moving
    
    r_reg = transform.warp(r_moving, tform.inverse, order=0, output_shape=r_fixed.shape)
    
    return moving_reg, r_reg


def imsplit(I):
    """
    Split an N-channel image into its individual channels

    Parameters:
    -----------
    I : ndarray
        Input image, of shape (M, N, P) representing an image.

    Returns:
    --------
    tuple of ndarrays
        Individual channels by splitting an N-channel image I.

    Class Support:
    -------------- 
    The input image can be of the class single, double, int8, int16, int32,
    int64, uint8, uint16, uint32, uint64, bool. The output images have
    the same class as the input image.
    """
    assert isinstance(I, np.ndarray) and I.ndim == 3 and not np.iscomplexobj(I), \
        "Input image must be a 3D real array."
    
    numChannels = I.shape[2]
    assert numChannels > 0, "Input image must have at least one channel."
    
    return tuple(I[:,:,idx] for idx in range(numChannels))

# Example 1: Split an image into its RGB channels
#I = plt.imread('peppers.png')
#r, g, b = imsplit(I)                                                 



def immultiply(X, Y):
    """
    Multiply two images or multiply image by constant.

    Parameters
    ----------
    X : array_like
        Input array to be multiplied with Y.
    Y : array_like
        Input array to be multiplied with X.

    Returns
    -------
    Z : ndarray
        The product of X and Y.

    """
    X = np.asarray(X)
    Y = np.asarray(Y)
    if X.dtype == bool or Y.dtype == bool:
        Z = do_logical_multiplication(X, Y)
    elif Y.size == 1 and Y.dtype == float:
        Z = X * Y
    else:
        check_for_same_size_and_class(X, Y)
        if Y.size == 0:
            Z = np.zeros(Y.shape, dtype=Y.dtype)
        else:
            Z = X * Y
    return Z


def check_for_same_size_and_class(X, Y):
    """
    Check if two arrays have the same size and class.

    Parameters
    ----------
    X : array_like
        Input array.
    Y : array_like
        Input array.

    Raises
    ------
    ValueError
        If the arrays don't have the same size and class.

    """
    if X.shape != Y.shape or X.dtype != Y.dtype:
        raise ValueError("Arrays must have the same size and class")


def do_logical_multiplication(X, Y):
    """
    Perform logical multiplication of two arrays.

    Parameters
    ----------
    X : array_like
        Logical input array.
    Y : array_like
        Input array.

    Returns
    -------
    Z : ndarray
        The product of X and Y.

    Raises
    ------
    ValueError
        If the arrays don't have the same size.

    """
    if X.shape != Y.shape:
        raise ValueError("Arrays must have the same size")
    if X.dtype == bool and Y.dtype == bool:
        Z = np.logical_and(X, Y)
    elif X.dtype == bool and np.issubdtype(Y.dtype, np.number):
        Z = Y.copy()
        Z[~X] = 0
    else:
        # X is numeric and Y is logical
        Z = X.copy()
        Z[~Y] = 0
    return Z
                                                 
                                                 
                                                
                                                 
                                                 
                                                 