#!/usr/bin/env python3
import re
import csv
from collections import Counter

def extract_syscalls(log_file):
    counts = Counter()
    with open(log_file, 'r', errors='ignore') as f:
        for line in f:
            if match := re.search(r'^\d+\s+([a-zA-Z0-9_]+)(\(|\s|$)', line):
                counts[match.group(1)] += 1
    return counts

def save_to_csv(counts, output_file):
    total = sum(counts.values())
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['syscall', 'count', 'percentage'])
        for call, count in counts.most_common():
            writer.writerow([call, count, f"{count/total:.3%}"])

if __name__ == '__main__':
    log_file = "build_logs/sqlite_make_strace.log"
    output_csv = "syscall_stats.csv"
    
    counts = extract_syscalls(log_file)
    save_to_csv(counts, output_csv)
    
    print(f"生成文件: {output_csv}")
    print(f"总系统调用: {sum(counts.values())} 次")
    print(f"唯一调用类型: {len(counts)} 种")