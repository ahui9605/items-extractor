import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import tempfile
import os
import re
import pydirectinput
import time

from PPOCR_api import GetOcrApi


def items_extract(quantity, position):
    for _ in range(position - 1):
        pydirectinput.keyDown("down")
        pydirectinput.keyUp("down")
        time.sleep(0.1)

    for _ in range(quantity):
        pydirectinput.keyDown("space")
        pydirectinput.keyUp("space")
        time.sleep(0.1)

    pydirectinput.keyDown("tab")
    pydirectinput.keyUp("tab")
    time.sleep(0.1)
    pydirectinput.keyDown("r")
    pydirectinput.keyUp("r")


def convert_text_list_to_dict(text_list):
    converted_dict = {"name": text_list[0]}

    items_dict = {}
    for text in text_list[1:]:
        processed_text = text.replace("（", "(").replace("）", ")")
        match = re.match(r"(.*?)\(([^)]+)\)", processed_text)
        if match:
            main_text, number = match.groups()
            items_dict[main_text] = int(number) if number.isdigit() else 1
        else:
            items_dict[processed_text] = 1
    converted_dict["items"] = items_dict
    return converted_dict


def main_loop(header, items):
    target_list = header
    target_items = items

    # target_list = "斯洛克姆·乔咖啡机"
    # target_items = ["纯水"]

    # target_list = "复古饮水机"

    # target_list = "核子可乐收集工作站"
    # target_items = ["核子可乐荒野口味"]

    ocr = GetOcrApi(r"PaddleOCR-json_v.1.3.1\PaddleOCR-json.exe")
    ocr_interval = 1.5
    last_ocr_time = time.time()

    WINDOW_NAME = "Game Viewer"
    GAME_WINDOW_TITLE = "Fallout76"
    window_width, window_height = 700, 700
    scale_factor = 0.35
    crop_top, crop_bottom, crop_left, crop_right = 0.15, 0.20, 0, 0
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, window_width, window_height)

    try:
        game_window = gw.getWindowsWithTitle(GAME_WINDOW_TITLE)[0]
    except IndexError:
        print(f"Error: Could not find a window with the title '{GAME_WINDOW_TITLE}'.")
        exit()

    while True:
        if game_window.isActive:
            x, y, width, height = (
                game_window.left,
                game_window.top,
                game_window.width,
                game_window.height,
            )
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = frame[
                int(height * crop_top) : int(height * (1 - crop_bottom)),
                int(width * crop_left) : int(width * (1 - crop_right)),
            ]

            right_part = frame[:, -int(frame.shape[1] * scale_factor) :]
            right_part_resized = cv2.resize(right_part, (window_width, window_height))
            cv2.imshow(WINDOW_NAME, right_part_resized)

            if time.time() - last_ocr_time > ocr_interval:
                last_ocr_time = time.time()
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".jpg"
                ) as temp_image:
                    cv2.imwrite(temp_image.name, right_part_resized)
                temp_image.close()
                time.sleep(0.3)

                res = ocr.run(temp_image.name)
                os.unlink(temp_image.name)

                if res["code"] != 100:
                    continue

                text_blocks = res["data"]
                detected_text = [block["text"] for block in text_blocks]
                filtered_text = convert_text_list_to_dict(detected_text)
                print(filtered_text)

                if "name" not in filtered_text or filtered_text["name"] != target_list:
                    continue

                # 复制一份字典用于操作
                items_to_extract = filtered_text.get("items", {}).copy()

                # 从字典中移除target_items里的物品
                for target_item in target_items:
                    if target_item in items_to_extract:
                        del items_to_extract[target_item]

                print("要移除的物品: ", items_to_extract)

                # for target_item in target_items:
                #     if target_item in filtered_text.get("items", {}):
                #         item_quantity = filtered_text["items"][target_item]
                #         item_position = (
                #             list(filtered_text["items"].keys()).index(target_item) + 1
                #         )
                #         print(
                #             f"物品: {target_item}, 数量: {item_quantity}, 位置: {item_position}"
                #         )
                #         items_extract(item_quantity, item_position)
                #         time.sleep(0.5)

                # 对要进行操作的物品进行提取操作
                for item, quantity in items_to_extract.items():
                    if quantity >= 5:
                        print(f"物品: {item}, 数量: {quantity} 超过5, 跳过操作")
                        continue
                    # 计算物品在原始文本列表中的位置
                    item_position = list(filtered_text["items"].keys()).index(item) + 1
                    print(f"物品: {item}, 数量: {quantity}, 位置: {item_position}")

                    # 调用items_extract函数进行提取操作
                    items_extract(quantity, item_position)
                    time.sleep(0.5)
                    break
        else:
            cv2.imshow(
                WINDOW_NAME, np.zeros((window_height, window_width, 3), dtype=np.uint8)
            )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    ocr.exit()


if __name__ == "__main__":
    main_loop()
