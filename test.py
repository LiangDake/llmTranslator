
import os

def get_files_with_absolute_paths(directory):
    # 获取文件夹中的所有项，并且过滤掉子文件夹，仅保留文件
    return [os.path.abspath(os.path.join(directory, f)) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# 使用示例
directory_path = '/Users/liangdake/localbin/localbin/users_space/liangke'
files_with_paths = get_files_with_absolute_paths(directory_path)
print(files_with_paths)
