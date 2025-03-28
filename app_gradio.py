import gradio as gr
import os
from tkinter import Tk, filedialog
from run import main


detect_clses=[
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush"
]

def choose_folder():
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filename = filedialog.askdirectory()
    if filename:
        if os.path.isdir(filename):
            root.destroy()
            return str(filename)
        else:
            root.destroy()
            return str(filename)
    else:
        filename = ""
        root.destroy()
        return str(filename)

def run(input_path,output_path,video_skip_frame,remove_bg,extract_main,output_width,output_height,file_exts,extract_main_clses,create_caption,caption_text):
    if input_path == "" or input_path is None or len(input_path)==0:
        gr.Warning("请选择需要处理的目录💥!", duration=5)
        return
    
    if output_path == "" or output_path is None or len(output_path)==0:
        gr.Warning("请选择输出目录💥!", duration=5)
        return
    
    if file_exts is None or len(file_exts)==0:
        gr.Warning("请选需要处理的文件类型💥!", duration=5)
        return

    if extract_main and (extract_main_clses is None or len(extract_main_clses)==0):
        gr.Warning("请选择需要保留的主体类别💥!", duration=5)
        return

    main(input_path,output_path,output_width,output_height,video_skip_frame,remove_bg,extract_main,file_exts,extract_main_clses,create_caption,caption_text)

    

with gr.Blocks() as demo:
    gr.Markdown("# 图片批量处理工具", elem_id="title")
   
    with gr.Group():    
        with gr.Row():
            input_path = gr.Textbox(label="选择需要处理的目录",  interactive=False,scale=8)
            input_browse_btn = gr.Button("选择",variant='primary')
            input_browse_btn.click(choose_folder,outputs=input_path,show_progress=False)

        file_exts= gr.Dropdown(choices=[".jpg",".jpeg", ".png",".mp4",".avi",'.mov'],multiselect=True,label="选择需要处理的文件类型")
        
    with gr.Row():
        output_path = gr.Textbox(label="选择输出目录",  interactive=False,scale=8)
        output_browse_btn = gr.Button("选择",variant='primary')
        output_browse_btn.click(choose_folder,outputs=output_path,show_progress=False)
    with gr.Row():
        video_skip_frame = gr.Number(label="视频抽帧每几帧抽1帧",minimum=1,value=1,interactive=True)
        
    
    with gr.Group():    
        with gr.Row():
            extract_main = gr.Checkbox(label="裁去图片非主体部分，保留主体部分")
            extract_main_clses= gr.Dropdown(choices=detect_clses,type='index',multiselect=True,label="请选择要保留的主体类型，可以多选")
        
        remove_bg = gr.Checkbox(label="移除背景,保留主体")
            
        
    with gr.Row():
        output_width = gr.Number(label="输出图片宽度",value=1024,interactive=True)
        output_height = gr.Number(label="输出图片高度",value=768,interactive=True)
    with gr.Row():
        create_caption = gr.Checkbox(label="创建图片描述文件")
        caption_text = gr.Textbox(label="图片描述",  interactive=True,scale=8)
    with gr.Row():
        run_button=gr.Button(value='开始处理',variant='primary')
        
        
    with gr.Row():
        result= gr.Textbox(label="处理结果")
        run_button.click(run,inputs=[input_path,output_path,video_skip_frame,remove_bg,extract_main,output_width,output_height,file_exts,extract_main_clses,create_caption,caption_text],show_progress='full',show_progress_on=[result,run_button]).success(lambda:"处理完成",None,result)

        
demo.launch(show_error=True,inbrowser=True)