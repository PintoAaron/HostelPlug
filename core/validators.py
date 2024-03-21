from django.core.exceptions import ValidationError



def validate_file_size(file):
    max_size_kb = 3000
    
    if file.size > max_size_kb * 1024:
        file_size  =  format(file.size/1024/1024, '.2f')
        raise ValidationError(f"File size cannot be larger than 3MB. Current file size is {file_size}MB!")