import os

def list_files(startpath, out_file='ls_R.txt'):
    with open(out_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = '│   ' * level + '├── '
            f.write(f"{indent}{os.path.basename(root)}\n")
            subindent = '│   ' * (level + 1)
            for file in files:
                f.write(f"{subindent}{file}\n")

if __name__ == '__main__':
    list_files(os.getcwd())
