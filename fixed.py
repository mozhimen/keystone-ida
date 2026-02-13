import os
import re

root_dir = '/Users/taiyou/Documents/GitHub/keystone-ida'  # 需替换为实际路径
patterns = {
    'cmake_version': re.compile(r'^\s*cmake_minimum_required\s*\(\s*VERSION\s*2\.8(\.\d+)?\s*\)', re.IGNORECASE),
    'cmp0051_start': re.compile(r'^\s*if\s*\(\s*POLICY\s+CMP0051\s*\)', re.IGNORECASE),
    'endif': re.compile(r'^\s*endif\s*\(?\)?', re.IGNORECASE)
}

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == 'CMakeLists.txt':
            filepath = os.path.join(dirpath, filename)
            lines = []
            skip_block = False
            with open(filepath, 'r') as f:
                for line in f:
                    if patterns['cmake_version'].match(line):
                        lines.append('cmake_minimum_required(VERSION 3.5)\n')
                        continue
                    if patterns['cmp0051_start'].match(line):
                        skip_block = True
                        lines.append('# ' + line)
                        continue
                    if skip_block:
                        lines.append('# ' + line)
                        if patterns['endif'].match(line):
                            skip_block = False
                        continue
                    lines.append(line)
            with open(filepath, 'w') as f:
                f.writelines(lines)
print("✅ CMake配置修复完成")
