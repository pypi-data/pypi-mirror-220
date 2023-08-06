#!python3
from eyes_soatra import eyes
import json

a = eyes.view_page(
    'https://www.city.sumida.lg.jp/sangyo_jigyosya/sangyo/yuusi/sonotanoyusi.html',
    show_header=True
)


print(json.dumps(a, ensure_ascii=False, indent=4))
