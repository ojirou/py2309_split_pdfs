import os
import glob
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import shutil
def split_files_in_folder(base_folder, sep_folder, MAX_SIZE):
    for pdf_file in Path(base_folder).glob("*.pdf"):
        if os.path.getsize(pdf_file) > MAX_SIZE:
            r = PyPDF2.PdfReader(str(pdf_file))
            lastpage = len(r.pages)
            if lastpage == 1:
                continue
            split = lastpage // 2
            f1 = sep_folder / f'{pdf_file.stem}_1.pdf'
            f2 = sep_folder / f'{pdf_file.stem}_2.pdf'
            w = PyPDF2.PdfWriter()
            for i in range(lastpage):
                w.add_page(r.pages[i])
                if i == split:
                    with open(f1, 'wb') as f:
                        w.write(f)
                        del w
                        w = PyPDF2.PdfWriter()
            with open(f2, 'wb') as f:
                w.write(f)
                del w
            if os.path.getsize(f1) > MAX_SIZE:
                split_files_in_folder(f1, sep_folder, MAX_SIZE)
            if os.path.getsize(f2) > MAX_SIZE:
                split_files_in_folder(f2, sep_folder, MAX_SIZE)
            pdf_file.unlink()
if __name__ == "__main__":
    base_folder = input("ベースフォルダのパスを入力してください: ")
    max_size_mb = input("ファイルの上限サイズ [MB]を入力してください: ")
    MAX_SIZE = float(max_size_mb)*1e6
    # 新しいフォルダを作成
    bak_folder = Path(base_folder).parent / f"bak_{Path(base_folder).name}"
    bak_folder.mkdir(parents=True, exist_ok=True)
    sep_folder = Path(base_folder).parent / f"sep_{Path(base_folder).name}"
    sep_folder.mkdir(parents=True, exist_ok=True)
    # ベースフォルダ内のファイルを新しいフォルダにコピー
    for item in Path(base_folder).glob("*"):
        if item.is_file():
            shutil.copy2(item, bak_folder)
    split_files_in_folder(base_folder, sep_folder, MAX_SIZE)