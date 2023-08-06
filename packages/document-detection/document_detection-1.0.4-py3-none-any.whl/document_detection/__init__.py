# import os,sys
# os.chdir(sys.path[0])
from document_detection.detection import Detection

det = Detection()
catalog_check = det.catalog_check
extract_standard_device = det.extract_standard_device
invalid_reference_check = det.invalid_reference_check
#similar_expression = det.similar_expression
abnormal_number_check = det.abnormal_number_check
detection_check = det.detection_check


