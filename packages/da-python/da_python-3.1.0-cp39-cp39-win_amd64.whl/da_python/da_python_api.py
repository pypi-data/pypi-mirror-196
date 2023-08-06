# from __future__ import absolute_import
# import sys
# import os
# import cv2
#
# import c_lib_wrap as da_python
#
# env_path = os.path.join(os.path.dirname(__file__), '')
# print(env_path)
# print(sys.path)
# if env_path not in sys.path:
#     sys.path.append(env_path)
#
#
# class DocumentAI:
#     def __init__(self, license, model):
#         self.license = license
#         da = da_python.create(license, model)
#
#         ocr = da.ocr("ch")
#         im = cv2.imread("/Users/yangjun/Documents/images/2.png")
#         result, result_code = ocr.infer(im)
#         print(result)
#
#
# def main():
#     DocumentAI("/Users/yangjun/jerome/work/DocumentAI/708096dd180b52e9.txt",
#                "/Users/yangjun/jerome/work/DocumentAI/cmake-build-mct/DocumentAI_Mct_Release_3.0.0/bin/708096dd180b52e9.model")
#     pass
#
#
# if __name__ == '__main__':
#     print(da_python.VERSION)
#
#     main()
