#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hugo博客Tag标准化脚本

该脚本用于帮助标准化Hugo博客文章中的tag，包括：
1. 将tag转换为小写
2. 合并同义tag
3. 限制tag数量
4. 移除不必要的tag
"""

import os
import re
from pathlib import Path

# Tag映射表（将非标准tag映射到标准tag）
TAG_MAPPING = {
    # 同义词统一
    'AI': 'ai',
    '人工智能': 'ai',
    'Agent': 'agent',
    'AI Agent': 'agent',
    '智能体': 'agent',
    'LLM': 'llm',
    '大语言模型': 'llm',
    'RAG': 'rag',
    '检索增强': 'rag',
    'MCP': 'mcp',
    'DevOps': 'devops',
    'Kubernetes': 'kubernetes',
    'Docker': 'docker',
    'Database': 'database',
    'Java': 'java',
    'Python': 'python',
    'JavaScript': 'javascript',
    'Git': 'git',
    'Linux': 'linux',
    'MacOS': 'linux',
    'Windows': 'linux',  # 简化处理，归类到操作系统
    'Best Practices': 'best-practices',
    'Best-Practices': 'best-practices',
    'best-practices': 'best-practices',
    'Troubleshooting': 'troubleshooting',
    'Performance': 'performance',
    'Security': 'security',
    'Architecture': 'architecture',
    'Development': 'development',
    'Coding': 'development',
    'Programming': 'development',
    'Tooling': 'tooling',
    'Tool Engineering': 'tooling',
    'Tools': 'tooling',
    'Cursor': 'cursor',
    'GitHub': 'github',
    'GitLab': 'gitlab',
    'VSCode': 'vscode',
    'Visual Studio Code': 'vscode',
    'Zookeeper': 'zookeeper',
    'MySQL': 'database',
    'PostgreSQL': 'database',
    'MongoDB': 'database',
    'Redis': 'database',
}

# 需要删除的tag（这些tag信息可以通过文章内容体现，不需要专门标记）
TAGS_TO_REMOVE = {
    'Reliability', 'Cost', 'Human-in-the-loop', 'AI Hype', 'Agent Lifecycle',
    'AgentOps', 'ChatOps', 'ai-tool', 'android', 'bootloader', 'root',
    'monitoring', 'RBAC', 'faiss', 'library', '技术趋势', 'apm',
    'apache-httpclient', 'mns', 'template-engine', 'benchmark', 'thymeleaf',
    'freemarker', 'velocity', 'rocker', 'migration', 'upgrade', 'chinese',
    'cli', 'markdown', 'ppt', 'marp', 'presentation', 'tradecraft', 'vm',
    'virtualbox', 'design', 'ux', 'sensory design', 'Agentic Systems',
    'Shopify', '企业应用', '知识库', '自动化', 'cot', 'react', 'cluster',
    'distributed-systems', '树莓派', 'microSD', '存储可靠性', '硬件选购',
    '高耐久度', '闪存', '单板计算机', 'visual-programming', 'yarnpkg',
    'hadoop', 'yarn', 'command-line', 'path', 'conflict', '性能调优',
    '参数配置', 'innodb', '游戏产业', 'Valve', 'Steam', '半条命', '创新',
    '科技人物', '游戏开发', '数字发行', 'ai tool', 'animation', 'video',
    '人物', 'data-security'
}

# 保留的核心tag词表
CORE_TAGS = {
    'ai', 'llm', 'agent', 'rag', 'mcp', 'devops', 'kubernetes', 'docker',
    'database', 'java', 'python', 'javascript', 'git', 'linux', 'best-practices',
    'troubleshooting', 'performance', 'security', 'architecture', 'development',
    'tooling', 'cursor', 'github', 'gitlab', 'vscode', 'zookeeper'
}

def standardize_tags(tags):
    """
    标准化tag列表

    Args:
        tags: 原始tag列表

    Returns:
        标准化后的tag列表
    """
    standardized = []

    for tag in tags:
        # 去除引号和空格
        tag = tag.strip().strip('"\'')

        # 应用映射表
        if tag in TAG_MAPPING:
            standardized_tag = TAG_MAPPING[tag]
        else:
            # 转换为小写
            standardized_tag = tag.lower()

        # 如果映射后的tag不在删除列表中，且是核心tag或可以接受的tag
        if (standardized_tag not in TAGS_TO_REMOVE and
            (standardized_tag in CORE_TAGS or len(standardized_tag) > 1)):
            standardized.append(standardized_tag)

    # 去重并限制数量（最多5个）
    unique_tags = list(dict.fromkeys(standardized))  # 保持顺序的去重
    return unique_tags[:5]

def process_front_matter(content):
    """
    处理文章前言部分的tag

    Args:
        content: 文章内容

    Returns:
        处理后的文章内容
    """
    # 匹配前言部分
    front_matter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(front_matter_pattern, content, re.DOTALL)

    if not match:
        return content

    front_matter = match.group(1)
    lines = front_matter.split('\n')

    # 查找tags行
    for i, line in enumerate(lines):
        if line.strip().startswith('tags:'):
            # 提取tag列表
            tags_match = re.search(r'tags:\s*(\[.*?\])', line)
            if tags_match:
                try:
                    # 安全地评估tag列表
                    tags_str = tags_match.group(1)
                    # 手动解析tag列表
                    tags = []
                    # 去除方括号并分割
                    tags_content = tags_str.strip('[]')
                    if tags_content.strip():
                        # 分割tag（考虑引号）
                        current_tag = ''
                        in_quotes = False
                        for char in tags_content + ',':
                            if char == '"' or char == "'":
                                in_quotes = not in_quotes
                            elif char == ',' and not in_quotes:
                                if current_tag.strip():
                                    tags.append(current_tag.strip().strip('"\''))
                                current_tag = ''
                            else:
                                current_tag += char

                    # 标准化tag
                    standardized_tags = standardize_tags(tags)

                    # 重新构建tags行
                    if standardized_tags:
                        new_tags_str = '[' + ', '.join([f'"{tag}"' if ' ' in tag else tag for tag in standardized_tags]) + ']'
                    else:
                        new_tags_str = '[]'

                    lines[i] = f'tags: {new_tags_str}'
                    break
                except:
                    # 如果解析失败，跳过该行
                    continue

    # 重新构建前言部分
    new_front_matter = '\n'.join(lines)
    return content.replace(front_matter, new_front_matter)

def process_file(file_path):
    """
    处理单个文件

    Args:
        file_path: 文件路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 处理前言部分
        new_content = process_front_matter(content)

        # 如果内容有变化，写回文件
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已处理: {file_path}")
        else:
            print(f"无变化: {file_path}")

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def main():
    """
    主函数
    """
    # 获取当前目录
    current_dir = Path('.')

    # 查找所有markdown文件
    md_files = list(current_dir.rglob('content/posts/*.md'))

    print(f"找到 {len(md_files)} 个markdown文件")

    # 处理每个文件
    for md_file in md_files:
        process_file(md_file)

    print("处理完成！")

if __name__ == '__main__':
    main()