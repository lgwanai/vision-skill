#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理工具类
支持 COS 上传和 BASE64 编码两种模式
"""

import os
import base64
import logging
from dotenv import load_dotenv
from cos_client import COSClient

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageProcessor:
    """图片处理工具类"""
    
    def __init__(self):
        """初始化处理器"""
        self.mode = os.getenv('IMAGE_UPLOAD_MODE', 'cos').lower()
        self.cos_client = None
        
        if self.mode == 'cos':
            self._init_cos_client()
    
    def _init_cos_client(self):
        """初始化 COS 客户端"""
        try:
            self.cos_client = COSClient()
            logger.info("COS 客户端初始化成功")
        except Exception as e:
            logger.warning(f"COS 客户端初始化失败: {e}，将回退到 BASE64 模式")
            self.mode = 'base64'
    
    def process_image(self, image_input):
        """
        处理图片输入
        
        Args:
            image_input: 图片路径或URL
            
        Returns:
            tuple: (image_data, is_base64)
                - cos 模式返回 (url, False)
                - base64 模式返回 (base64_string, True)
        """
        if image_input.startswith(('http://', 'https://')):
            return self._process_url(image_input)
        
        if os.path.exists(image_input):
            return self._process_local_file(image_input)
        
        raise ValueError(f"无效的图片输入: {image_input}")
    
    def _process_url(self, url):
        """处理 URL 图片"""
        if self.mode == 'cos':
            return (url, False)
        else:
            import requests
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            b64_data = base64.b64encode(response.content).decode('utf-8')
            return (b64_data, True)
    
    def _process_local_file(self, file_path):
        """处理本地文件"""
        if self.mode == 'cos':
            return self._upload_to_cos(file_path)
        else:
            return self._encode_to_base64(file_path)
    
    def _upload_to_cos(self, file_path):
        """上传到 COS"""
        if not self.cos_client:
            raise RuntimeError("COS 客户端未初始化")
        
        logger.info(f"上传图片到 COS: {file_path}")
        result = self.cos_client.upload_file(file_path)
        
        if not result['success']:
            raise RuntimeError(f"图片上传失败: {result.get('error')}")
        
        logger.info(f"图片上传成功: {result['url']}")
        return (result['url'], False)
    
    def _encode_to_base64(self, file_path):
        """编码为 BASE64"""
        logger.info(f"编码图片为 BASE64: {file_path}")
        
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        b64_data = base64.b64encode(image_data).decode('utf-8')
        logger.info(f"BASE64 编码完成，大小: {len(b64_data)} 字符")
        
        return (b64_data, True)
    
    def get_mode(self):
        """获取当前模式"""
        return self.mode


if __name__ == "__main__":
    processor = ImageProcessor()
    print(f"当前模式: {processor.get_mode()}")
