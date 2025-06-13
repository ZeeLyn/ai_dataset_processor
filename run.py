import cv2
from dataset_process import dataset_process
import os,sys,io
import argparse
import numpy as np
dataset_process=dataset_process()
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
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

def process(image:np.ndarray,size_handle_type:int,output_width:int,output_height:int,output_max_size:int,remove_bg:bool,extract_main:bool,extract_main_clses:list):
   
    # 如果需要提取主体，则调用extract_main函数
    if extract_main:
        image= dataset_process.extract_main(image,extract_main_clses)
     # 如果需要移除背景，则调用remove_background函数
    if remove_bg:
        image=dataset_process.remove_background(image)
        
    # 调用resize_image函数，将图像调整为指定的大小
    return dataset_process.resize_image(image,size_handle_type,output_width,output_height,output_max_size)

def main(input_folder,output_folder,size_handle_type,output_width,output_height,output_max_size,skip_frame,remove_bg,extract_main,file_exts,extract_main_clses,create_caption,caption_text,start_index=0):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    print('extract_main_clses',extract_main_clses)
    counter=start_index
    for file,ext in list_images_and_videos(input_folder,file_exts):
        # print('处理：{0}'.format(file))
        sys.stdout.writelines('处理：{0}'.format(file))
        sys.stdout.flush()
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
                sys.stdout.writelines('处理：第{0}帧'.format(frame_index+1))
                sys.stdout.flush()
                counter+=1
                # cv2.imwrite(os.path.join(output_folder,f'{counter:06}.org.jpg'),frame)
                img= process(frame,size_handle_type,output_width,output_height,output_max_size,remove_bg,extract_main,extract_main_clses)
                cv2.imwrite(os.path.join(output_folder,f'{counter:06}.jpg'),img,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
                if create_caption:
                    with open(os.path.join(output_folder,f'{counter:06}.txt'),'w', encoding='utf-8') as f:
                        f.write(caption_text)
                
        else:
            counter+=1
            # cv2.imwrite(os.path.join(output_folder,f'{counter:06}.org.jpg'),cv2.imread(file))
            img= process(cv2.imread(file),size_handle_type,output_width,output_height,output_max_size,remove_bg,extract_main,extract_main_clses)
            cv2.imwrite(os.path.join(output_folder,f'{counter:06}.jpg'),img,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
        if create_caption:
            with open(os.path.join(output_folder,f'{counter:06}.txt'),'w', encoding='utf-8') as f:
                    f.write(caption_text)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder',type=str,required=True, help='输入目录')
    parser.add_argument('--output_folder',type=str,default="output",required=True, help='输出目录')
    parser.add_argument('--size_handle_type',type=int,default=1,help='尺寸处理方式，0:"固定尺寸，不够的地方填充黑色", 1:"固定宽度，高度自动缩放",2:"固定高度，宽度自动缩放",3:"设置最大值，按最大边缩放"')
    parser.add_argument('--output_width',type=int,default=1024,help='输出宽度')
    parser.add_argument('--output_height',type=int,default=576,help='输出高度')
    parser.add_argument('--output_max_size',type=int,default=1024,help='输出最大尺寸')
    parser.add_argument('--skip_frame',type=int,default=1,help='每几帧抽取一帧')
    parser.add_argument('--remove_bg', action='store_true',help='是否移除背景')
    parser.add_argument('--extract_main', action='store_true',help='是否提取主体部分，删除图片多余部分')
    parser.add_argument('--file_exts',action='append' ,default=[],help='处理文件的类型有哪些')
    parser.add_argument('--extract_main_clses',action='append',type=int,default=[],help='提取主体部分时，只保留哪些类别')
    parser.add_argument('--create_caption',type=bool,default=False,help='是否创建反推提示词')
    parser.add_argument('--caption_text',type=str,default='',help='反推提示词内容')
    parser.add_argument('--start_index',type=int,default=0,help='开始计数索引')
    
    
    
    args= parser.parse_args()
    
    # print('args:',args)
    
    main(args.input_folder,args.output_folder,args.size_handle_type,args.output_width,args.output_height,args.output_max_size,args.skip_frame,args.remove_bg,args.extract_main,args.file_exts,args.extract_main_clses,args.create_caption,args.caption_text,args.start_index)