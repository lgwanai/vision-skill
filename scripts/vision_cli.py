#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vision Skill CLI
主入口脚本，用于接收命令并启动后台任务
"""

import sys
import os
import argparse
import subprocess
import json
from task_utils import create_task, get_task

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKER_SCRIPT = os.path.join(SCRIPT_DIR, 'worker.py')

def run_worker(task_id):
    """启动后台工作进程"""
    # 使用 subprocess.Popen 启动新进程，不等待其结束
    # 确保在后台运行
    env = os.environ.copy()
    # 确保 PYTHONPATH 包含当前脚本目录，以便 worker 能导入模块
    env['PYTHONPATH'] = SCRIPT_DIR + os.pathsep + env.get('PYTHONPATH', '')
    
    subprocess.Popen(
        [sys.executable, WORKER_SCRIPT, task_id],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True
    )

def handle_recognize(args):
    """处理识别命令"""
    if not os.path.exists(args.image_path) and not args.image_path.startswith(('http://', 'https://')):
        print(json.dumps({"error": "图片文件不存在或无效URL"}))
        return
        
    params = {
        "image": args.image_path,
        "prompt": args.prompt
    }
    
    task_id = create_task("vision_recognition", params)
    run_worker(task_id)
    
    print(json.dumps({
        "task_id": task_id,
        "status": "pending",
        "message": "视觉识别任务已提交"
    }, ensure_ascii=False))

def handle_generate(args):
    """处理生成命令"""
    params = {
        "prompt": args.prompt,
        "ref_images": args.ref_images,
        "sequential_options": None
    }
    
    if args.seq_count:
        params["sequential_options"] = {"max_images": args.seq_count}
        
    task_id = create_task("image_generation", params)
    run_worker(task_id)
    
    print(json.dumps({
        "task_id": task_id,
        "status": "pending",
        "message": "图像生成任务已提交"
    }, ensure_ascii=False))

def handle_status(args):
    """处理状态查询命令"""
    task = get_task(args.task_id)
    if not task:
        print(json.dumps({"error": "任务不存在"}, ensure_ascii=False))
        return
        
    print(json.dumps(task, ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Vision Skill CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Recognize command
    recognize_parser = subparsers.add_parser("recognize", help="Perform vision recognition")
    recognize_parser.add_argument("image_path", help="Path or URL to the image")
    recognize_parser.add_argument("--prompt", default="你看见了什么？", help="Prompt for recognition")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate images")
    generate_parser.add_argument("prompt", help="Prompt for generation")
    generate_parser.add_argument("--ref", dest="ref_images", nargs="+", help="Reference image paths or URLs")
    generate_parser.add_argument("--seq", dest="seq_count", type=int, help="Number of sequential images to generate")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check task status")
    status_parser.add_argument("task_id", help="Task ID")
    
    args = parser.parse_args()
    
    if args.command == "recognize":
        handle_recognize(args)
    elif args.command == "generate":
        handle_generate(args)
    elif args.command == "status":
        handle_status(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
