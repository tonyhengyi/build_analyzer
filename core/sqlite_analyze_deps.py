#!/usr/bin/env python3
import re
import json
from collections import defaultdict

def extract_dependencies(log_file):
    deps = defaultdict(list)
    current_target = None
    
    with open(log_file, 'r', errors='ignore') as f:
        for line in f:
            # 捕获编译目标（gcc命令）
            if 'execve' in line and ('gcc' in line or 'clang' in line):
                if match := re.search(r'\"([^\"]+\.c)\"', line):
                    current_target = match.group(1).split('/')[-1]
            
            # 捕获头文件依赖
            elif 'openat' in line and ('.h' in line or '.inc' in line):
                if current_target and (match := re.search(r'\"([^\"]+\.(h|inc))\"', line)):
                    header = match.group(1).split('/')[-1]
                    if header not in deps[current_target]:
                        deps[current_target].append(header)
    
    return dict(deps)

if __name__ == '__main__':
    deps = extract_dependencies("build_logs/sqlite_make_strace.log")
    with open('sqlite_dependencies.json', 'w') as f:
        json.dump(deps, f, indent=2)
    print("依赖关系已保存到 sqlite_dependencies.json")
