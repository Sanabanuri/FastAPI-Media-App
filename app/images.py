
from imagekitio import ImageKit

import os
from dotenv import load_dotenv

load_dotenv()
imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),

)
