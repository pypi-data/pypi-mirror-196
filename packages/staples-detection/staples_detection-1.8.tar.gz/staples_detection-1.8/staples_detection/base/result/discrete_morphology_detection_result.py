import numpy

from staples_detection.base.result.mask_detection_result import MaskDetectionResult


class DiscreteMorphologyStapleDetectionResult(MaskDetectionResult):
    """
    Object that stores the results of the Discrete Morphology algorithm for staples detection. Furthermore, contains the performance metrics
    of the classification.
    """

    def __init__(self,
                 final_mask: numpy.ndarray,
                 colormask: numpy.ndarray,
                 elapsed_time: float,
                 ground_truth_mask: numpy.ndarray):

        super(DiscreteMorphologyStapleDetectionResult, self).__init__(final_mask, colormask, elapsed_time, ground_truth_mask)
