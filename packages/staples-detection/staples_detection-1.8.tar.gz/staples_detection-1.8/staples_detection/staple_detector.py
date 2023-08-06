import cv2
import numpy

from staples_detection.base.result.mask_detection_result import MaskDetectionResult
from staples_detection.base.staple_detection_methods import StapleDetectionMethod
from staples_detection.algorithms import gradient, canny, discrete_morphology


class StapleDetector:

    def __init__(self, image: numpy.ndarray):
        """
        Initializes the object that detects the staples in a given image.

        Args:
            image: A numpy array, representing the BGR image of the staples.
        """
        self.__image = image

    def detect_staples(self,
                       method: StapleDetectionMethod = StapleDetectionMethod.COMBINED_GRADIENT,
                       ground_truth_mask: numpy.ndarray = None,
                       restricted_region: numpy.ndarray = None,
                       **kwargs) -> MaskDetectionResult:
        """
        Detects the staples in an image.

        Args:
            method: A StapleDetectionMethod value, representing the method to be used.
            ground_truth_mask: Represents the ground truth mask. If it is passed, the results contains the performance
                               metrics.
            restricted_region: A boolean numpy array, with the same size as the image, representing the region where the staples
                               want to be detected. The final mask will be the intersection (element-wise and operation) of the
                               generated mask and this mask. If None, all the staples will be detected.
            **kwargs: The parameters of the different methods.

        Returns:
            A GradientStapleDetectionResult, containing the partial results of each process and the global elapsed time.
        """
        if restricted_region is None:
            restricted_region = numpy.ones_like(ground_truth_mask)

        if method == StapleDetectionMethod.CANNY:
            return canny.generate_canny_mask(self.__image, restricted_region, ground_truth_mask, **kwargs)
        elif method == StapleDetectionMethod.HORIZONTAL_GRADIENT or method == StapleDetectionMethod.VERTICAL_GRADIENT or method == StapleDetectionMethod.COMBINED_GRADIENT:
            return gradient.generate_gradient_mask(self.__image, method, restricted_region, ground_truth_mask, **kwargs)
        elif method == StapleDetectionMethod.DISCRETE_MORPHOLOGY:
            return discrete_morphology.generate_morphology_mask(self.__image, restricted_region, ground_truth_mask, **kwargs)
        else:
            raise Exception("--> NotAvailableMethod. The selected algorithm is not implemented.")
