#!python3
from eyes_soatra import eyes
import json

a = eyes.view_page(
    url='https://www.city.daito.lg.jp/soshiki/27/1298.html',
    show_header=True,
)

print(json.dumps(a, ensure_ascii=False, indent=4))