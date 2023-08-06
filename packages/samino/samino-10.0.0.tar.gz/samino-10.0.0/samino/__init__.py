from httpx import get
from os import system, name
from time import sleep
from .acm import Acm
from .client import Client
from .local import Local

version = "10.0.0"
newest = get("https://pypi.org/pypi/samino/json").json()["info"]["version"]

def will():
    print("\n\n")
    print("أنعي اليكم اخونا احمد الفوزات محمد العبد الله(سيرلز) أثر الزلزال الحاصل في عنتاب...لاكلمات تعبر عن عمق الجراح على الفراق ، لا كلمات تصف العجز والألم على فراقه ،إلا أن الله اصطفاك لتكون مع الشهداء والصديقين..أسأل الله أن يلهمنا الصبر على فراقك ، وأسال الله أن يلهم أهله الصبر والسلوان..البقاء لله وحده  لله ما أعطى ولله ما أخذ إِنَّا لِلَّهِ وَإِنَّا إِلَيْهِ رَاجِعُونَ ولا حول ولا قوة إلا بالله العلي العظيم", end = "\n\n")
    print("We mourn the loss of our brother Ahmed Al-Fawzat Mohammed Abdullah (SirLez), who passed away due to the earthquake that occurred in Gaziantep. There are no words that can express the depth of our grief over their departure, nor can any words describe the helplessness and pain that we feel upon their loss. However, Allah has chosen you to be among the martyrs and the righteous. We ask Allah to grant us patience in the face of their loss, and we ask Him to grant their families patience and solace.\"To Allah we belong and to Him we shall return. There is no power or strength except with Allah, the Most High, the Almighty.\"")
    print("\n\n")
    exit()

def initOs():
    system("pip install -U samino")
    if name == "nt":
        system("cls")
    else:
        system("clear")

if version != newest:
    initOs()
    sleep(1)
    will()