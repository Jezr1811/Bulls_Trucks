from cloudinary_storage.storage import MediaCloudinaryStorage


class DocumentoStorage(MediaCloudinaryStorage):
    folder = "documentos"