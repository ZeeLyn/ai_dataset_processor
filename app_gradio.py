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

def run(input_path,output_path,video_skip_frame,remove_bg,extract_main,size_handle_type,output_width,output_height,output_max_size,file_exts,extract_main_clses,create_caption,caption_text,start_index=0):
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
    if size_handle_type is None:
        gr.Warning("请选择图片尺寸处理方式💥!", duration=5)
        return

    main(input_path,output_path,size_handle_type,output_width,output_height,output_max_size,video_skip_frame,remove_bg,extract_main,file_exts,extract_main_clses,create_caption,caption_text,start_index=start_index)

    


            

with gr.Blocks() as app:
    gr.Markdown("# 图片批量处理工具", elem_id="title")
   
    with gr.Group():    
        with gr.Row():
            input_path = gr.Textbox(label="选择需要处理的目录",  interactive=True,scale=8)
            input_browse_btn = gr.Button("选择",variant='primary')
            input_browse_btn.click(choose_folder,outputs=input_path,show_progress=False)

        file_exts= gr.Dropdown(choices=[".jpg",".jpeg", ".png",".webp",".mp4",".avi",'.mov'],multiselect=True,label="选择需要处理的文件类型")
        
    with gr.Row():
        output_path = gr.Textbox(label="选择输出目录",  interactive=True,scale=8)
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
        size_handle_type= gr.Dropdown(choices=["固定尺寸，不够的地方填充黑色", "固定宽度，高度自动缩放","固定高度，宽度自动缩放","设置最大值，按最大边缩放"],type='index',interactive=True,label="图像尺寸处理方式",value=0) 
        output_width = gr.Number(label="输出图片宽度",value=1024,interactive=True,visible=False,minimum=1) 
        output_height = gr.Number(label="输出图片高度",value=768,interactive=True,visible=False,minimum=1)
        output_max_size = gr.Number(label="输出图片长边的最大尺寸",value=1024,interactive=True,visible=False,minimum=1)
        
        print(size_handle_type.value)
        
        def on_changed_size_handle_type(size_handle_type):
            match size_handle_type:
                case 0:
                    return [gr.update(output_width.elem_id,visible=True), gr.update(output_height.elem_id,visible=True), gr.update(output_max_size.elem_id,visible=False)]
                case 1:
                    return [gr.update(output_width.elem_id,visible=True), gr.update(output_height.elem_id,visible=False), gr.update(output_max_size.elem_id,visible=False)]
                case 2:
                    return [gr.update(output_width.elem_id,visible=False), gr.update(output_height.elem_id,visible=True), gr.update(output_max_size.elem_id,visible=False)]
                case 3:
                     return [gr.update(output_width.elem_id,visible=False), gr.update(output_height.elem_id,visible=False), gr.update(output_max_size.elem_id,visible=True)]
                case _:
                    pass
                
        size_handle_type.change(fn=on_changed_size_handle_type,inputs=[size_handle_type],outputs=[output_width,output_height,output_max_size]);  
        
        # output_width = gr.Number(label="输出图片宽度",value=1024,interactive=True)
        
        print(type(output_width),output_width)
       
                
    with gr.Row():
        create_caption = gr.Checkbox(label="创建图片描述文件")
        caption_text = gr.Textbox(label="图片描述",  interactive=True,scale=8)
    with gr.Row():
        run_button=gr.Button(value='开始处理',variant='primary')
        
    with gr.Row():
        start_index= gr.Number(label="文件开始编号",value=0,interactive=True)
        
        
    with gr.Row():
        result= gr.Textbox(label="处理结果")
        
        run_button.click(run,inputs=[input_path,output_path,video_skip_frame,remove_bg,extract_main,size_handle_type,output_width,output_height,output_max_size,file_exts,extract_main_clses,create_caption,caption_text,start_index],show_progress='full',show_progress_on=[result,run_button]).success(lambda:"处理完成",None,result)

        
app.launch(show_error=True,inbrowser=True,debug=True)