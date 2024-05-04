import tkinter
import pathlib

# https://docs.python.org/3/library/tkinter.html#images

def LoadImages(master):
    print(tkinter.image_types())  # prints list of supported types
    # 'photo', 'bitmap' are your options. PNG and GIF are supported.
    # see the manpage (photo.tk3) for info on custom format-loaders. also see: image.tk3
    cwd = pathlib.Path.cwd()
    imagepath = cwd / "TeamLogos" / "testlogos"
    if not (imagepath.exists() and imagepath.is_dir()):
        print("image folder not found")
        return []
    pngs = list(imagepath.glob('*.png'))
    #alt = tkinter.Image(imgtype='photo', name="whatever", master=root, file=path)
    loaded = [tkinter.PhotoImage(master=master, file=path, name=path.stem, width=30) for path in pngs]
    # you can assign a loaded image to a widget by using it's name in the 'image=' argument!
    return loaded


if __name__ == "__main__":
    root = tkinter.Tk()
    images = LoadImages(root)
    print(f"names = {[img.name for img in images]}")

    # seems like assigning a photo to a widget overrides any text assigned to it??
    stupid = tkinter.Label(master=root, image=images[0])
    btn = tkinter.Button(master=root, image="stt")  # loading by name!
    stupid.grid()
    btn.grid(column=1, row=0)

    #print(something.config()) # none
    #print(stupid.config())
    #print(btn.config())

    root.mainloop()
    
