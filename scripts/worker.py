#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后台任务执行器
"""

import sys
import os
import json
import logging
from task_utils import get_task, update_task
from cos_client import COSClient
from doubao_client import DoubaoClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tasks/worker.log')
)
logger = logging.getLogger(__name__)

def handle_vision_task(params):
    """处理视觉识别任务"""
    image_input = params.get('image')
    prompt = params.get('prompt', '你看见了什么？')
    
    if not image_input:
        raise ValueError("缺少 image 参数")
        
    # 如果是本地文件，先上传COS
    if os.path.exists(image_input):
        logger.info(f"上传图片到COS: {image_input}")
        cos_client = COSClient()
        upload_result = cos_client.upload_file(image_input)
        
        if not upload_result['success']:
            raise Exception(f"图片上传失败: {upload_result.get('error')}")
            
        image_url = upload_result['url']
        logger.info(f"图片上传成功: {image_url}")
    else:
        # 假设是URL
        image_url = image_input
        
    # 调用豆包API
    logger.info("调用豆包视觉识别API")
    client = DoubaoClient()
    result = client.vision_recognition(image_url, prompt)
    
    return {
        "image_url": image_url,
        "recognition_result": result
    }

def handle_generation_task(params):
    """处理图像生成任务"""
    prompt = params.get('prompt')
    ref_images = params.get('ref_images') # 列表或单个路径/URL
    sequential_options = params.get('sequential_options')
    
    if not prompt:
        raise ValueError("缺少 prompt 参数")
        
    processed_ref_images = []
    
    # 处理参考图
    if ref_images:
        if isinstance(ref_images, str):
            ref_images = [ref_images]
            
        cos_client = COSClient()
        
        for img in ref_images:
            if os.path.exists(img):
                logger.info(f"上传参考图到COS: {img}")
                upload_result = cos_client.upload_file(img)
                if not upload_result['success']:
                    raise Exception(f"参考图上传失败: {upload_result.get('error')}")
                processed_ref_images.append(upload_result['url'])
            else:
                processed_ref_images.append(img)
    
    # 调用豆包API
    logger.info("调用豆包图像生成API")
    client = DoubaoClient()
    
    # 如果只有一个参考图，传递单个URL；如果有多个，传递列表
    ref_input = processed_ref_images if processed_ref_images else None
    if ref_input and len(ref_input) == 1:
        ref_input = ref_input[0]
        
    result = client.generate_image(prompt, image_urls=ref_input, sequential_options=sequential_options)
    
    return {
        "prompt": prompt,
        "ref_images": processed_ref_images,
        "generation_result": result
    }

def main():
    if len(sys.argv) < 2:
        logger.error("缺少任务ID参数")
        return
        
    task_id = sys.argv[1]
    logger.info(f"开始处理任务: {task_id}")
    
    try:
        # 更新状态为处理中
        update_task(task_id, {"status": "processing"})
        
        task = get_task(task_id)
        if not task:
            logger.error(f"找不到任务: {task_id}")
            return
            
        task_type = task.get('type')
        params = task.get('params', {})
        
        result = None
        
        if task_type == 'vision_recognition':
            result = handle_vision_task(params)
        elif task_type == 'image_generation':
            result = handle_generation_task(params)
        else:
            raise ValueError(f"未知任务类型: {task_type}")
            
        # 更新状态为完成
        update_task(task_id, {
            "status": "completed",
            "result": result
        })
        logger.info(f"任务完成: {task_id}")
        
    except Exception as e:
        logger.error(f"任务失败: {task_id}, 错误: {str(e)}", exc_info=True)
        update_task(task_id, {
            "status": "failed",
            "error": str(e)
        })

if __name__ == "__main__":
    main()
