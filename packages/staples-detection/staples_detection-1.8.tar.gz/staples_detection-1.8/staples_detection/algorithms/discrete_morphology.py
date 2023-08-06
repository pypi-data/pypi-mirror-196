import cv2
import numpy
import time


from discrete_fuzzy_operators.base.operators.binary_operators.discrete.suboperators.fuzzy_discrete_aggregation_suboperators.tnorm import Tnorm
from discrete_fuzzy_operators.builtin_operators.discrete.tnorms import TnormExamples
from discrete_morphology.base.structuring_element import StructuringElement
from discrete_morphology.operators.erosion_dilation.discrete_dilation import discrete_dilation
from typing import Tuple

from staples_detection.algorithms.utils import draw_mask_over_image

from staples_detection.base.result.discrete_morphology_detection_result import DiscreteMorphologyStapleDetectionResult


def generate_morphology_mask(image: numpy.ndarray,
                             restricted_region: numpy.ndarray,
                             ground_truth_mask: numpy.ndarray = None,
                             **kwargs) -> DiscreteMorphologyStapleDetectionResult:
    # PARAMETER EXTRACTION
    threshold_binary: int = kwargs.get("threshold_binary", 50)
    morphological_kernel: numpy.ndarray = kwargs.get("morphological_kernel", numpy.array([[219, 219, 219], [219, 255, 219], [219, 219, 219]]))
    morphological_kernel_center: Tuple[int, int] = kwargs.get("morphological_kernel_center", (1, 1))
    dilation_iterations: int = kwargs.get("dilation_iterations", 5)
    tnorm: Tnorm = kwargs.get("dilation_tnorm", TnormExamples.get_tnorm(TnormExamples.LUKASIEWICZ, n=255))
    # END
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    elapsed_time = time.time()
    se = StructuringElement(morphological_kernel, morphological_kernel_center)

    dilation = discrete_dilation(image=image_gray, structuring_element=se, iterations=dilation_iterations,
                                 conjunction=tnorm)
    _, binary_image = cv2.threshold(dilation, numpy.amax(dilation)-threshold_binary, 255, cv2.THRESH_BINARY)
    final_mask = restricted_region & ((binary_image/255).astype(bool))

    elapsed_time = time.time() - elapsed_time

    return DiscreteMorphologyStapleDetectionResult(final_mask=final_mask,
                                                   colormask=draw_mask_over_image(image, final_mask),
                                                   elapsed_time=elapsed_time,
                                                   ground_truth_mask=ground_truth_mask)