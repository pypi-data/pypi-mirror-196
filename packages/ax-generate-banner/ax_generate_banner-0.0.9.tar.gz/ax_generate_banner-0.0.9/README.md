# AX Banner Generator


### Usage
```shell
pip install ax-generate-banner
```

Then: 
```python
from core.generate import Generate

if __name__ == '__main__':
    generate = Generate(
        left_image='image-left.jpg',
        right_image=['img1.png', 'image-right.png'],
        text_header=["BEDS", "FLOORS", "SQ.FT"],
        text_data=["3", "43", "4863"],
        residence_title='Rukan Residences',
        font='alethiapro-regular.otf'
    )
    generate.save('result.jpg')
```

![alt text](fonts/img.png "AX Generated Image Banner")