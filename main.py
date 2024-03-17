import argparse
import json
import os

from tqdm import tqdm

from html2image import JSInjection
from html2image.html2image import Html2Image


def load_data(path):
    data_list = []
    # 获取文件扩展名
    _, file_extension = os.path.splitext(path)
    with open(path, 'r') as json_file:
        if file_extension.lower() == '.json':
            # 如果是 JSON 文件
            data = json.load(json_file)
            data_list.append(data)
        elif file_extension.lower() == '.jsonl':
            # 如果是 JSON Lines 文件
            for line in json_file:
                data = json.loads(line)
                data_list.append(data)
        else:
            # 未知文件类型
            raise ValueError(f"Unsupported file extension: {file_extension}")

    return data_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file_path", type=str, default='/Users/meisen/Desktop/Web-ScreenshotMaker/data/en0001-01.jsonl')
    parser.add_argument("--output_path", type=str, default='/Users/meisen/Desktop/Web-ScreenshotMaker/image')
    args = parser.parse_args()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    input_data = load_data(args.input_file_path)

    for data in tqdm(input_data):
        clueweb_id = data['id']
        file = clueweb_id + '.png'
        clueweb_url = data['url']
        h2i = Html2Image(clueweb_url, JSInjection.Scroll2Bottom())
        file_path = os.path.join(args.output_path, file)
        h2i.save_image(filename=file_path)

    print('finish!')






if __name__ == "__main__":
    main()