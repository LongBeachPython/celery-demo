from IPython.display import display, HTML
# Helper function for printing ASCII in Jupyter notebook
def print_ascii_html(ascii_text, font_size_pct=60, line_height_pct=80):
    ascii_html = ('<pre style="font-size:{font_size_pct}%; line-height:{line_height_pct}%;">'
                  '{ascii_text}</pre>'.format(font_size_pct=font_size_pct, 
                                              line_height_pct=line_height_pct, 
                                              ascii_text=ascii_text))
    chart = HTML(ascii_html)
    display(chart)

def display_progress_bar_until_completed(task):
    import time
    filler = ''
    while task.state != 'SUCCESS':
        prefix = 'Running'
        filler_char = '.'
        filler = filler_char + filler
        print('\r{}{}'.format(prefix, filler), end='')
        time.sleep(0.5)
    print('Completed')

def queue_and_return_ascii_task(filename, columns):
    task = image_to_ascii_task.apply_async(args=[filename, columns])
    return image_to_ascii_task.AsyncResult(task.id)    

def print_task_result(task):
    ascii_image = task.info.get('result')
    ascii_image_text = '\n'.join(line for line in ascii_image)
    print_ascii_html(ascii_image_text, font_size_pct=15, line_height_pct=100)    