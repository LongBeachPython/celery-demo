import numpy as np
from PIL import Image

from proj.celery import celery
from proj.models import AsciiTask

GRAY_SCALE = '@%#*+=-:. '

# modified version of code from Python Playground (No Starch Press)

def image_to_ascii(filename, column_count, scale=0.43):
    # load the image and calculate dimensions
    image = Image.open(filename).convert('L')
    image_width, image_height = image.size
    output_width = image_width / column_count
    output_height = output_width / scale
    row_count = int(image_height / output_height)    
    if column_count > image_width or row_count > image_height:
        raise Exception("Image too small for specified cols!")

    # create the ascii image
    ascii_image = []
    for row_counter in range(row_count):
        y1 = int(row_counter * output_height)
        y2 = int((row_counter + 1) * output_height)
        if row_counter == row_count - 1:
            y2 = image_height
        ascii_image.append("")
        for i in range(column_count):
            # crop image to extract tile
            x1 = int(i * output_width)
            x2 = int((i + 1) * output_width)
            if i == column_count - 1:
                x2 = image_width
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            im = np.array(img)
            im_width, im_height = im.shape
            avg = np.average(im.reshape(im_width * im_height))

            # look up ascii char
            gray_scale_value = GRAY_SCALE[int((avg * 9) / 255)]

            # append ascii char to string
            ascii_image[row_counter] += gray_scale_value
            
    return ascii_image


@celery.task(bind=True)
def image_to_ascii_task(self, filename, column_count):
    ascii_image = image_to_ascii(filename, column_count)
    return {'status': 'COMPLETE', 'result': ascii_image}


@celery.task(bind=True)
def image_to_ascii_task_improved(self, filename, column_count):
    ascii_task = AsciiTask(self.request.id, ascii_text='')
    ascii_task.save()

    ascii_image = image_to_ascii(filename, column_count)
    ascii_task.ascii_text = '\n'.join(line for line in ascii_image)
    ascii_task.save()

    return {'status': 'COMPLETE'}