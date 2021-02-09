from apps.settings.common import env

# https://github.com/respondcreate/django-versatileimagefield
VERSATILEIMAGEFIELD_SETTINGS = {
    'cache_length': env('VERSATILE_IMAGE_CACHE_LENGTH', int, 2592000),  # 30 days
    'cache_name': env('VERSATILE_IMAGE_CACHE_NAME', str, 'default'),
    'jpeg_resize_quality': env('VERSATILE_IMAGE_JPEG_RESIZE_QUALITY', int, 70),
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': True,
    'image_key_post_processor': None,
    'progressive_jpeg': env('VERSATILE_IMAGE_PROGRESSIVE_JPEG', bool, True),
}
VERSATILEIMAGEFIELD_USE_PLACEHOLDIT = True
VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    # 'example': [
    #     ('full', 'url'),
    #     ('100', 'thumbnail__100x100'),
    #     ('480', 'thumbnail__480x480'),
    #     ('960', 'thumbnail__960x960'),
    #     ('1150', 'thumbnail_1150x1150'),
    # ],
}
