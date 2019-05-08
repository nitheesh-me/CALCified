import os

class uploadfile():
    def __init__(self, name, type=None, size=None, not_allowed_msg='',folder=""):
        self.name = name
        self.type = type
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.url = "data/%s/%s" % (folder,name)
        self.thumbnail_url = "thumbnail/%s/%s" % (folder,name)
        self.delete_url = "delete/%s/%s" % (folder,name)
        self.delete_type = "DELETE"


    def is_image(self):
        fileName, fileExtension = os.path.splitext(self.name.lower())

        if fileExtension in ['.jpg', '.png', '.jpeg', '.bmp']:
            return True

        return False


    def get_file(self):
        if self.type != None:
            # POST an image
            if self.type.startswith('image'):
                return {"name": self.name,
                        "type": self.type,
                        "size": str(self.size), 
                        "url": 'https://localhost:5000/' + self.url, 
                        "thumbnailUrl": 'https://localhost:5000/' + self.thumbnail_url,
                        "deleteUrl": 'https://localhost:5000/' + self.delete_url, 
                        "deleteType": self.delete_type,}

            # POST an normal file
            elif self.not_allowed_msg == '':
                return {"name": self.name,
                        "type": self.type,
                        "size": str(self.size), 
                        "url": 'https://localhost:5000/' + self.url, 
                        "deleteUrl": 'https://localhost:5000/' + self.delete_url, 
                        "deleteType": self.delete_type,}

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "type": self.type,
                        "size": str(self.size),}

        # GET image from disk
        elif self.is_image():
            return {"name": self.name,
                    "size": str(self.size), 
                    "url": 'https://localhost:5000/' + self.url, 
                    "thumbnailUrl": 'https://localhost:5000/' + self.thumbnail_url,
                    "deleteUrl": 'https://localhost:5000/' + self.delete_url, 
                    "deleteType": self.delete_type,}

        # GET normal file from disk
        else:
            return {"name": self.name,
                    "size": str(self.size), 
                    "url": 'https://localhost:5000/' + self.url, 
                    "deleteUrl": 'https://localhost:5000/' + self.delete_url, 
                    "deleteType": self.delete_type,}
