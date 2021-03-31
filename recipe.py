import scrape_schema_recipe
import pendulum
from bs4 import BeautifulSoup
import requests
import json
page=requests.get('https://www.indianhealthyrecipes.com/?s=chicken')
bsoupobj=BeautifulSoup(page.text,'html.parser')
link=bsoupobj.select('h2 > a')
print(bsoupobj.title.text)
recipe_no=1
temp_dict={}
for links in link:
   instructions=""
   ingredients=""
   preparation_time=""
   i=1
   j=1
   url=links.get("href")
   recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)
   #print("Recipe No is: "+str(recipe_no))
   recipe=recipe_list[0]
   rec_inst=recipe['recipeInstructions']
   rec_ing=recipe['recipeIngredient']
   rec_prep_time=recipe["prepTime"]
   str1=""
   image_url=recipe['image']
   image=image_url[0]
   for value in rec_inst:
      if('itemListElement' in value.keys()):
         for value1 in value['itemListElement']:
            if('text' in value1.keys()):
               instructions+=" "+str(i)+") "+value1['text']+"\n"
            else:
               print("yes from else")
            i=i+1
      elif('text' in value.keys()):
         instructions+=" "+str(i)+") "+value['text']+"\n"
         i=i+1
      else:
         print("Loop is broke")
         break
   
   
   for value in rec_ing:
      ingredients+=" "+str(j)+") "+value+"\n"
      j=j+1
   print(ingredients)
   if('totalTime' not in recipe.keys()):
       d={"Prepare Time":str(pendulum.Duration(seconds=recipe['prepTime'].total_seconds())),"Cook Time":str(pendulum.Duration(seconds=recipe['cookTime'].total_seconds())),"Image URL":image,"Ingredients":ingredients.lstrip().replace("\n","chr(10)"),"Instruction":instructions.lstrip().replace("\n","chr(10)")}
   else:
       d={"Prepare Time":str(pendulum.Duration(seconds=recipe['prepTime'].total_seconds())),"Cook Time":str(pendulum.Duration(seconds=recipe['cookTime'].total_seconds())),"Total Time":str(pendulum.Duration(seconds=recipe['totalTime'].total_seconds())),"Image URL":image,"Ingredients":ingredients.lstrip().replace("\n","chr(10)"),"Instruction":instructions.lstrip().replace("\n","chr(10)")}
   temp_dict[recipe['name']]=d
   recipe_no+=1
print("////////////End Of Recipe"+str(recipe_no)+"///////////")
print(temp_dict)

with open("recipe.json","a+",encoding='utf8') as rect:
   json.dump(temp_dict,rect,ensure_ascii=False,indent=2)
   rect.close()


