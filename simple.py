from PIL import Image

def reduce_image_by_factor(fin:str, fout:str, factor:int) -> None:
    print("reducing image by",factor)
    try:
        img = Image.open(fin)
        img = img.reduce(factor)
        img = img.save(fout, quality=95, optimize=True)
    except Image.DecompressionBombError as ex1:
        print(ex1)
    except Exception as ex2:
        raise ex2 