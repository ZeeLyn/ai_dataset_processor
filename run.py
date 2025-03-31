import cv2
from dataset_process import dataset_process
import os
import argparse
import numpy as np
dataset_process=dataset_process()

image_extensions = ['.jpg','.jpeg', '.png']
video_extensions = [".mp4",".avi",'.mov']

# 用于列出指定文件夹中的图片和视频文件
def list_images_and_videos(folder,file_exts):
   
    # 遍历指定文件夹中的所有文件
    for root,dirs,files in os.walk(folder):
        for file in files:
            # 打印文件路径、文件夹和文件名
            # print(root,dirs,file)
            # 获取文件扩展名
            _,file_ext=os.path.splitext(file)
            # 如果文件扩展名在图片和视频文件的扩展名中，则返回文件路径
            if file_ext.lower() in file_exts:
                yield os.path.join(root,file),file_ext.lower()

def process(image:np.ndarray,output_width:int,output_height:int,remove_bg:bool,extract_main:bool,extract_main_clses:list):
   
    # 如果需要提取主体，则调用extract_main函数
    if extract_main:
        image= dataset_process.extract_main(image,extract_main_clses)
     # 如果需要移除背景，则调用remove_background函数
    if remove_bg:
        image=dataset_process.remove_background(image)
        
    # 调用resize_image函数，将图像调整为指定的大小
    return dataset_process.resize_image(image,output_width,output_height)

def main(input_folder,output_folder,output_width,output_height,skip_frame,remove_bg,extract_main,file_exts,extract_main_clses,create_caption,caption_text,start_index=0):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        
    counter=start_index
    for file,ext in list_images_and_videos(input_folder,file_exts):
        print('处理：{0}'.format(file))
        if ext in video_extensions:
            cap= cv2.VideoCapture(file)
            frame_index=0
            while True:
                ret,frame=cap.read()
                if not ret:
                    cap.release()
                    break
                
                frame_index+=1
                if frame_index%skip_frame!=0:
                    continue
                counter+=1
                # cv2.imwrite(os.path.join(output_folder,f'{counter:06}.org.jpg'),frame)
                img= process(frame,output_width,output_height,remove_bg,extract_main,extract_main_clses)
                cv2.imwrite(os.path.join(output_folder,f'{counter:06}.jpg'),img)
                if create_caption:
                    with open(os.path.join(output_folder,f'{counter:06}.txt'),'w', encoding='utf-8') as f:
                        f.write(caption_text)
                
        else:
            counter+=1
            # cv2.imwrite(os.path.join(output_folder,f'{counter:06}.org.jpg'),cv2.imread(file))
            img= process(cv2.imread(file),output_width,output_height,remove_bg,extract_main,extract_main_clses)
            cv2.imwrite(os.path.join(output_folder,f'{counter:06}.jpg'),img)
        if create_caption:
            with open(os.path.join(output_folder,f'{counter:06}.txt'),'w', encoding='utf-8') as f:
                    f.write(caption_text)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder',type=str,required=True, help='输入目录')
    parser.add_argument('--output',type=str,default="output", help='输出目录')
    parser.add_argument('--skip_frame',type=int,default=1,help='每几帧抽取一帧')
    parser.add_argument('--remove_bg',type=bool,default=True,help='是否移除背景')
    parser.add_argument('--extract_main',type=bool,default=True,help='是否提取主体部分，删除图片多余部分')
    parser.add_argument('--output_width',type=int,default=1024,help='输出宽度')
    parser.add_argument('--output_height',type=int,default=576,help='输出高度')
    args= parser.parse_args()
    
    main(args.input_folder,args.output,args.output_width,args.output_height,args.skip_frame,args.remove_bg,args.extract_main)