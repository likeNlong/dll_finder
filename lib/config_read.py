import yaml

# 读取 YAML 文件
with open('config.yaml', 'r',encoding='utf-8') as file:
    data = yaml.safe_load(file)

dll_names_paths = data['dll_names_paths']
destination_dir = data['destination_dir']
exe_name = data['exe_name']
delay = data['delay']


