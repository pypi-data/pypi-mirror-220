import filetype
import os

LIST_OF_IMAGE_MIME = ['image/bmp','image/jpeg','image/x-png','image/png','image/gif']




def check_file_type(file_path):
    # mime = magic.Magic(mime=True)
    try:
        mime_check = filetype.guess(file_path)
        file_mime_check = mime_check.mime
        file_type_checked = file_mime_check not in  LIST_OF_IMAGE_MIME
        if file_type_checked:
            return "The image file is not valid."
        return True
    except AttributeError as e:
        return "Invalid file type"
  
            



# imagecheck = ImageValidator("./hello.txt",2014)
# rr1 = imagecheck.check_file_size("./hello.txt",2014)
# rr2 = imagecheck.check_file_mime_type("./hello.txt")
# print(rr1)
# print(rr2)
        