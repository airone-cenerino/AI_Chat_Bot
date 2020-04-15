import MeCab
import re, os

inout_file_name = "ですよ！tweet2020-04-14"   # 読み込むファイル名
save_directory = "../Preprocessing/before_preprocessing_data/"   # 保存先directory

if not os.path.exists(save_directory):
    os.mkdir(save_directory)


with open("tweet/" + inout_file_name + ".txt", "r", encoding="utf-8") as seqFile, open(save_directory + inout_file_name + "_input.txt", "w", encoding="utf-8") as inFile, open(save_directory + inout_file_name + "_output.txt", "w", encoding="utf-8") as outFile:
    count = 0
    flg = True
    for line in seqFile:
        count += 1
        if "REQ:" in line:
            line = re.sub("REQ:", "", line)  # REQ:を消す。
            inFile.write(line)
            flg = False
        elif "RES:" in line:
            line = re.sub("RES:", "", line)  # RES:を消す。
            outFile.write(line)
            flg = True
        else:
            continue
            