import requests
import time
import csv
from models import Items

link1 = r'Scripts\Python space\\' #Укажите путь к папке, в которую вы хотите сохранить файл выходных данных "WB_data.csv", если вы оставите скобки пустыми, будет использоваться путь по умолчанию. (там же, где находится скрипт)
# пример пути: r'Scripts\Python space\\' в конце должны быть два слеша.
page = 3   # просто укажите число на странице, на которой вы хотите, чтобы скрипт перестал работать. 
# Если значение равно None или 0, скрипт будет работать бесконечно, пока вы не отключите его вручную.

class parseWB:

    def parse(self):
        i = 1
        self.__create_csv()
        while True:
            params = {
                'ab_comp_blend_by_prob_v2_2': '1',
                'ab_testid': 'pk0',
                'appType': '1',
                'curr': 'rub',
                'dest': '-1257786',
                'page': i,
                'query': '0',
                'resultset': 'catalog',
                'spp': '30',
                'suppressSpellcheck': 'false',
            }

            response = requests.get('https://recom.wb.ru/personal/ru/common/v5/search', params=params)
            time.sleep(0.2)
            
            items_info = Items.parse_obj(response.json()['data'])
            
            self.__save_csv(i,items_info)
            print(f'[+] Страница {i} сохранена.')
            
            if type(page) == int and page is not None and page > 0:
                if i == page:
                    break
                
            i += 1

    def __create_csv(self):
        with open(f'{link1}WB_data.csv', mode='w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['№', 'id', 'Название', 'Бренд', 'Цена(текущая)', 'Цена(старая)', 'Рейтинг', 'В наличии'])
                
    def __save_csv(self, num, items):
        with open(f'{link1}WB_data.csv', mode='a', newline="") as file:
            num -= 1
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.number + (num * 100),
                                product.id, 
                                product.name, 
                                product.brand, 
                                product.product_price, 
                                product.basic_price, 
                                product.reviewRating, 
                                product.volume])
        
if __name__ == "__main__":
    parser = parseWB()
    parser.parse() 