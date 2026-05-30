#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用视觉模型客户端
支持多种模型提供商，兼容 OpenAI 格式 API
"""

import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()


class VisionClient:
    """通用视觉模型客户端类"""
    
    def __init__(self):
        """初始化客户端"""
        self.vision_base_url = os.getenv('VISION_API_BASE_URL', '').rstrip('/')
        self.vision_api_key = os.getenv('VISION_API_KEY', '')
        self.vision_model = os.getenv('VISION_MODEL', '')
        self.vision_fallback = os.getenv('VISION_FALLBACK_MODEL', '')
        
        self.image_base_url = os.getenv('IMAGE_API_BASE_URL', '').rstrip('/')
        self.image_api_key = os.getenv('IMAGE_API_KEY', '')
        self.image_model = os.getenv('IMAGE_MODEL', '')
        self.image_fallback = os.getenv('IMAGE_FALLBACK_MODEL', '')
        
        self._validate_config()
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _validate_config(self):
        """验证配置"""
        if not self.vision_api_key:
            raise ValueError("VISION_API_KEY 环境变量未设置")
        if not self.vision_model:
            raise ValueError("VISION_MODEL 环境变量未设置")
        if not self.vision_base_url:
            raise ValueError("VISION_API_BASE_URL 环境变量未设置")
        
        if not self.image_api_key:
            self.image_api_key = self.vision_api_key
        if not self.image_model:
            self.logger.warning("IMAGE_MODEL 未设置，图像生成功能可能不可用")
        if not self.image_base_url:
            self.image_base_url = self.vision_base_url
    
    def vision_recognition(self, image_data, text="你看见了什么？", model_override=None, is_base64=False):
        """
        视觉识别
        
        Args:
            image_data: 图片URL 或 base64 字符串
            text: 提示词
            model_override: 覆盖默认模型
            is_base64: 是否为 base64 格式
        
        Returns:
            dict: API响应结果
        """
        url = f"{self.vision_base_url}/chat/completions"
        model = model_override or self.vision_model
        
        if is_base64:
            image_content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }
            }
        else:
            image_content = {
                "type": "image_url",
                "image_url": {
                    "url": image_data
                }
            }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        image_content,
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {self.vision_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            self.logger.info(f"开始视觉识别: model={model}, base64={is_base64}")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"视觉识别失败: {str(e)}")
            return {"error": str(e)}
    
    def generate_image(self, prompt, image_urls=None, sequential_options=None, model_override=None):
        """
        图像生成 (文生图/图生图)
        
        Args:
            prompt: 提示词
            image_urls: 参考图URL列表或单个URL
            sequential_options: 连续生成选项，如 {"max_images": 4}
            model_override: 覆盖默认模型
            
        Returns:
            dict: API响应结果
        """
        url = f"{self.image_base_url}/images/generations"
        model = model_override or self.image_model
        
        if not model:
            return {"error": "IMAGE_MODEL 未配置"}
        
        payload = {
            "model": model,
            "prompt": prompt,
            "response_format": "url",
            "size": "2K",
            "stream": False,
            "watermark": True
        }
        
        if image_urls:
            payload["image"] = image_urls
            
        if sequential_options:
            payload["sequential_image_generation"] = "auto"
            payload["sequential_image_generation_options"] = sequential_options
            payload["stream"] = True
        else:
            payload["sequential_image_generation"] = "disabled"
            
        headers = {
            "Authorization": f"Bearer {self.image_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            self.logger.info(f"开始图像生成: {prompt[:30]}...")
            
            if payload.get("stream"):
                response = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
                response.raise_for_status()
                
                results = []
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data: '):
                            data_str = decoded_line[6:]
                            if data_str != '[DONE]':
                                try:
                                    data_json = json.loads(data_str)
                                    results.append(data_json)
                                except:
                                    pass
                return {"results": results, "is_stream": True}
            else:
                response = requests.post(url, headers=headers, json=payload, timeout=120)
                response.raise_for_status()
                return response.json()
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"图像生成失败: {str(e)}")
            return {"error": str(e)}
    
    def get_vision_model(self):
        """获取当前视觉模型"""
        return self.vision_model
    
    def get_vision_fallback(self):
        """获取备用视觉模型"""
        return self.vision_fallback
    
    def get_image_model(self):
        """获取当前图像生成模型"""
        return self.image_model
    
    def get_image_fallback(self):
        """获取备用图像生成模型"""
        return self.image_fallback


if __name__ == "__main__":
    client = VisionClient()
    print(f"Vision Model: {client.get_vision_model()}")
    print(f"Image Model: {client.get_image_model()}")
