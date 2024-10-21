import nltk
nltk.download('punkt')

print(nltk.data.path)

import os

paths = ['C:\\Users\\sonia/nltk_data', 'C:\\Users\\sonia\\miniconda3\\nltk_data', 
         'C:\\Users\\sonia\\miniconda3\\share\\nltk_data', 'C:\\Users\\sonia\\miniconda3\\lib\\nltk_data', 
         'C:\\Users\\sonia\\AppData\\Roaming\\nltk_data', 'C:\\nltk_data', 'D:\\nltk_data', 'E:\\nltk_data']

for path in paths:
    punkt_path = os.path.join(path, 'tokenizers', 'punkt')
    if os.path.exists(punkt_path):
        print(f"Found 'punkt' at {punkt_path}")
    else:
        print(f"'punkt' not found in {path}")
