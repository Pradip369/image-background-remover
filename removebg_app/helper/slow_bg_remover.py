from pixellib.tune_bg import alter_bg
import cv2
import numpy as np
from PIL import Image as im
import io

class BaseRemoveBG(alter_bg):

    def change_bg_img(self, f_image_path,b_image_path=None, output_image_name = None, verbose = None, detect = None):
        if verbose is not None:
            ...

        ori_img = cv2.imdecode(np.fromstring(f_image_path.read(), np.uint8), cv2.IMREAD_COLOR)
        seg_image = self.segmentAsPascalvoc(ori_img,process_frame=True)[1]

        if detect is not None:
            target_class = self.target_obj(detect)
            seg_image[seg_image != target_class] = 0
            
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2BGRA)

        mask = np.where((seg_image==(0,0,0)).all(axis=2), 0, 255).astype(np.uint8)
        bg_mask = seg_image.copy()
        bg_mask = cv2.cvtColor(bg_mask, cv2.COLOR_BGR2BGRA)
        bg_mask[:, :, 3] = mask
        result = cv2.bitwise_and(ori_img, bg_mask)
        if output_image_name is not None:
            cv2.imwrite(output_image_name, result)
        return result

    def blur_bg(self, image_path,low = False, moderate = False, extreme = False, output_image_name = None, verbose = None, detect = None):
        if verbose is not None:
            print("processing image......")

        ori_img = cv2.imdecode(np.fromstring(image_path.read(), np.uint8), cv2.IMREAD_COLOR)

        seg_image = self.segmentAsPascalvoc(ori_img,process_frame=True)

        if detect is not None:
            target_class = self.target_obj(detect)
            seg_image[1][seg_image[1] != target_class] = 0

        if low == True:
            blur_img = cv2.blur(ori_img, (21,21), 0)

        if moderate == True:
            blur_img = cv2.blur(ori_img, (39,39), 0)

        if extreme == True:
            blur_img = cv2.blur(ori_img, (81,81), 0)

        out = np.where(seg_image[1], ori_img, blur_img)
        
        if output_image_name is not None:
            cv2.imwrite(output_image_name, out)

        return out

    def gray_bg(self, image_path, output_image_name = None, verbose = None, detect = None):
        if verbose is not None:
            print("processing image......")
        
        ori_img = cv2.imdecode(np.fromstring(image_path.read(), np.uint8), cv2.IMREAD_COLOR)
        seg_image = self.segmentAsPascalvoc(ori_img,process_frame=True)

        if detect is not None:
            target_class = self.target_obj(detect)
            seg_image[1][seg_image[1] != target_class] = 0
        
        gray_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
        result = np.where(seg_image[1], ori_img, gray_img)
        
        if output_image_name is not None:
            cv2.imwrite(output_image_name, result)

        return result

def slow_remover(my_image,is_blur=False,is_grey=False,blur_type='moderate',detect=None):
    change_bg = BaseRemoveBG(model_type="pb")
    change_bg.load_pascalvoc_model("removebg_app/model/xception_pascalvoc.pb")

    if is_blur:
        if blur_type == 'low':
            img = change_bg.blur_bg(my_image,detect = detect,low = True)
        elif blur_type == 'extreme':
            img = change_bg.blur_bg(my_image,detect = detect,extreme = True)
        else:
            img = change_bg.blur_bg(my_image,detect = detect,moderate = True)
    elif is_grey:
        img = change_bg.gray_bg(my_image,detect = detect)
    else:
        img = change_bg.change_bg_img(f_image_path=my_image,detect=detect)

    ''' Convert arr into binary image '''
    _, buffer = cv2.imencode(".png", img)
    io_buf = io.BytesIO(buffer)

    return io_buf.read()