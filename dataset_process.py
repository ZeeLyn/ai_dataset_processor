from rembg import remove,new_session
from ultralytics import YOLO
import cv2
import numpy as np


class dataset_process:
    def __init__(self,remove_bg_model='u2netp.onnx',yolo_model='yolo11x.pt'):
        self.remove_bg_sesssion= new_session(remove_bg_model)
        self.yolo = YOLO(yolo_model)  # load an official model

    # 移除背景
    def remove_background(self,image:np.ndarray):
        # 调用remove函数，传入image和self.remove_bg_sesssion参数，将返回值赋给output
        output= remove(image,session=self.remove_bg_sesssion)
        # 将output从BGRA格式转换为BGR格式
        output=cv2.cvtColor(output, cv2.COLOR_BGRA2BGR)
        # 返回output
        return output

    # 检测图片的里最大的主体目标，并返回该主体目标的图像区域
    def extract_main(self,image:np.ndarray,detect_cls:list=[2]):
        
        # Predict with the model
        results = self.yolo(image)  # predict on an image

        # Access the results
        max_box=None
        max_area=0
        for result in results:
            # print(result.boxes)
            for box in result.boxes:
                xywh = box.xywh[0]  # center-x, center-y, width, height
                # print(xywh)
                type=int(box.cls[0])
                
                # 如果type在detect_cls中，并且width大于max_width，则更新max_width_box
                if type in detect_cls and xywh[2]*xywh[3]>max_area:
                    max_area=xywh[2]*xywh[3]
                    max_box=box

                
            # xywhn = result.boxes.xywhn  # normalized
            # xyxy = result.boxes.xyxy  # top-left-x, top-left-y, bottom-right-x, bottom-right-y
            # xyxyn = result.boxes.xyxyn  # normalized
            # result=results[max_width_idx]
            # names = [result.names[cls.item()] for cls in result.boxes.cls.int()]  # class name of each box
            # confs = result.boxes.conf  # confidence score of each box
            # print(names,confs)
        # 如果max_width_box不为空，则返回该box对应的图像区域
        if max_box is not None:
            xywh = max_box.xywh[0]
            w=int(xywh[2])
            h=int(xywh[3])
            x=int(xywh[0]-w/2)
            y=int(xywh[1]-h/2)
            return image[y:y+h,x:x+w]
        else:
            return image
        
    # 缩放图片到固定大小
    def resize_image(self,image:np.ndarray,size_handle_type:int, new_width:int, new_height:int,output_max_size:int):
        h, w = image.shape[:2]
        new_image=image
        # 固定尺寸，不够的地方填充黑色
        if size_handle_type==0:
            # 计算缩放比例
            scale_width = new_width / w
            scale_height = new_height / h
            scale = min(scale_width, scale_height)  # 选择较小的比例以保持宽高比
            
            # 计算新尺寸，使用较小的比例
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            # 创建新的图像，背景色设置为黑色
            new_image = np.full((new_height, new_width, 3), 0, dtype=np.uint8)
            
            # 将原始图像粘贴到新图像上，居中显示
            x = (new_width - new_w) // 2
            y = (new_height - new_h) // 2
            new_image[y:y+new_h, x:x+new_w] = cv2.resize(image, (new_w, new_h))
        # 固定宽度，高度自动缩放
        elif size_handle_type==1:
            new_image=cv2.resize(image,(new_width,int(new_width*h/w)))
        # 固定高度，宽度自动缩放
        elif size_handle_type==2:
            new_image=cv2.resize(image,(int(new_height*w/h),new_height))
        elif size_handle_type==3:
            if h>w:
                new_image=cv2.resize(image,(int(output_max_size*w/h),output_max_size))
            else:
                new_image=cv2.resize(image,(output_max_size,int(output_max_size*h/w)))
        else:
            pass
        
        return new_image
