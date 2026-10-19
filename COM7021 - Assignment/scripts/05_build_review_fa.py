#!/usr/bin/env python3
"""Step 5-FA: Build a self-contained Persian (Farsi) review HTML draft with high-fidelity RTL styling,
fluent, simple, crystal-clear Persian prose, authentic first-person reflections,
and a subtle minimal footer language link.
"""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_CSV = BASE_DIR / "data" / "ecomove_cleaned.csv"
TABLES_DIR = BASE_DIR / "output" / "tables"
FIG_DIR = BASE_DIR / "output" / "figures"
OUT_HTML_FA = BASE_DIR / "COM7021_Draft_Review_25199053_fa.html"
ROOT_INDEX_FA = BASE_DIR.parent / "index_fa.html"


def b64_img(filename: str) -> str:
    path = FIG_DIR / filename
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def count_words(html_fragment: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html_fragment)
    words = [w for w in re.split(r"\s+", text.strip()) if w]
    return len(words)


# ==============================================================================
# FLUENT, SIMPLE & CLEAR PERSIAN PROSE — TASK 1
# ==============================================================================
FA_TASK1_SEC_1_1 = """
<p>در این پروژه، داده‌های عملکرد سیستم حمل‌ونقل شهری در ۱۲ شهر اروپایی را بررسی کردیم. این مجموعه داده شامل ۵,۰۰۰ رکورد روزانه در سال‌های ۲۰۲۴ و ۲۰۲۵ است و ۱۸ متغیر مختلف را ثبت کرده است. در مرحله بررسی اولیه و تمیزکاری داده‌ها، اطمینان حاصل شد که هیچ مقدار گمشده یا نامعتبری وجود ندارد و تمام شناسه‌ها کاملاً یکتا هستند. همچنین تاریخ‌های عددی اکسل به فرمت استاندارد تاریخ تبدیل شدند. برای اینکه بتوانیم وسایل مختلف مثل مترو، اتوبوس، تراموا و اسکوترهای برقی را منصفانه و دقیق با یکدیگر مقایسه کنیم، چند شاخص کلیدی جدید ساختیم: حاشیه سود خالص، درصد پوشش هزینه‌ها با کرایه، هزینه و کرایه به ازای هر مسافر، تعداد شکایت‌ها به ازای هر ۱۰,۰۰۰ مسافر، و میزان کاهش دی‌اکسید کربن به ازای هر کیلووات‌ساعت برق مصرفی.</p>
"""

FA_TASK1_SEC_1_2 = """
<p>آمار اولیه (جدول ۱) نشان می‌دهد که متغیرهای وابسته به حجم مسافر بسیار نامتقارن هستند؛ مثلاً تعداد مسافران روزانه (با میانگین ۸,۱۸۱ و میانه ۴,۳۹۸) یا درآمد بلیت، چون متروی پرظرفیت (با میانگین بیش از ۲۴,۰۰۰ مسافر در روز و سهم ۶۳ درصدی از کل مسافران) در کنار دوچرخه‌ها و اسکوترهای تک‌نفره (با میانگین حدود ۳۵۰ مسافر در روز) قرار گرفته است. اما برعکس، شاخص‌های کیفیت خدمات توزیع بسیار یکدست و متقارنی دارند: میانگین تأخیر کل شبکه ۴.۳۵ دقیقه، نرخ وقت‌شناسی ۸۲ درصد و امتیاز رضایت مسافران ۴.۰۱ از ۵ است.</p>
"""

FA_TASK1_FIG1_TEXT = """
<p><strong>۱. تغییرات فصلی و روزهای کاری (شکل ۱):</strong> این نمودار روند تغییرات مسافران را در ماه‌های سال‌های ۲۰۲۴ و ۲۰۲۵ نشان می‌دهد. نوار میانی مشخص می‌کند که در روزهای کاری هفته، تقاضای سفر حدود ۳۴٪ بیشتر از روزهای تعطیل آخر هفته است (۸,۸۰۰ مسافر در برابر ۶,۵۰۰ مسافر). تقاضا در فصل بهار (ماه‌های مارس و آوریل) به اوج می‌رسد و در ماه اکتبر با ۲۷٪ کاهش به کمترین مقدار سالانه می‌رسد؛ بنابراین ماه اکتبر بهترین زمان برای تعمیرات اساسی ناوگان است بدون اینکه به سفرهای کاری روزمره لطمه‌ای وارد شود.</p>
"""

FA_TASK1_FIG2_TEXT = """
<p><strong>۲. کشف تناقض آماری سیمپسون در سود شهرها (شکل ۲):</strong> نمودار دمبلی سود خام شهرها را در کنار سود تعدیل‌شده مقایسه می‌کند. در نگاه اول و با آمار خام، شهر برلین سودده به نظر می‌رسید و مادرید ضررده‌ترین شهر بود. اما بررسی عمیق‌تر نشان داد که در مادرید، سهم ثبت اطلاعات دوچرخه‌ها و اسکوترهای اشتراکی بیشتر بوده و همین موضوع آمار شهر را خراب کرده بود. وقتی سهم وسایل نقلیه را در تمام شهرها یکسان کردیم، واقعیت آشکار شد: برلین ۷ پله سقوط کرد و در جایگاه ۱۱ قرار گرفت، در حالی که مادرید بخش عمده ضرر ظاهری‌اش جبران شد و رتبه سوم تقاضای واقعی مسافر در اروپا را به دست آورد.</p>
"""

FA_TASK1_FIG3_TEXT = """
<p><strong>۳. درآمد و هزینه هر مسافر در برابر حفظ محیط‌زیست (شکل ۳):</strong> این نمودار دو بخشی، اقتصاد هر سفر و اثرات زیست‌محیطی آن را نشان می‌دهد. بخش الف اثبات می‌کند که اسکوترها و دوچرخه‌های اشتراکی از نظر اقتصادی کاملاً زیان‌ده هستند؛ چون جمع‌آوری و شارژ هر اسکوتر حدود ۲۲ یورو هزینه دارد در حالی که کرایه دریافتی فقط ۱.۵۹ یورو است (یعنی ۲۰ یورو ضرر خالص در هر سفر). در نقطه مقابل، مترو، تراموا و پارکینگ‌های اتصال حومه‌ای سودده هستند. از نظر محیط‌زیست هم مترو با صرفه‌جویی بیش از ۳,۱۵۰ تن دی‌اکسید کربن به ازای هر تن ۱,۳۶۶ یورو سود خالص برای شهر می‌سازد، در حالی که پرداخت یارانه به اسکوتر برای هر تن کاهش کربن بیش از ۱۵۰ هزار یورو خرج روی دست شهر می‌گذارد.</p>
"""

FA_TASK1_FIG4_TEXT = """
<p><strong>۴. بررسی دقیق تأخیرها با نمودار باران‌ابری (شکل ۴):</strong> این نمودار، توزیع پیوسته تأخیرها را به همراه تک‌تک سفرها نشان می‌دهد تا معطلی واقعی مردم پنهان نماند. در اینجا مشخص است که اتوبوس شهری گلوگاه اصلی تأخیر در کل شبکه است (با میانه تأخیر ۶.۵ دقیقه و کمترین وقت‌شناسی با ۷۵٪). در مقابل، مترو به دلیل مسیر اختصاصی زیرزمینی و دور بودن از ترافیک خیابان، بسیار قابل پیش‌بینی با تأخیر کم عمل می‌کند و دوچرخه و اسکوتر هم از راه‌بندان‌های خیابانی فرار می‌کنند.</p>
"""

FA_TASK1_FIG5_TEXT = """
<p><strong>۵. رابطه تأخیر و نارضایتی مسافران (شکل ۵):</strong> این نمودار نشان می‌دهد هر چقدر تأخیر بیشتر شود، رضایت مسافران کمتر می‌شود. وقتی تأخیر از ۶ دقیقه عبور می‌کند، افت رضایت شتاب می‌گیرد. نکته مهم در منحنی‌های بالایی این است که در روزهای رویدادهای بزرگ و جشن‌های شهری، مسافران ۲۶٪ بیشتر می‌شوند، اما چون ناوگان ذخیره برای جذب این مسافران آماده نشده، تأخیرها ۳۱٪ بالا می‌رود و رضایت مسافران افت می‌کند.</p>
"""

FA_TASK1_FIG6_7_TEXT = """
<p><strong>۶. اثر شرایط آب‌وهوا و مشکلات خطوط حومه‌ای (شکل‌های ۶ تا ۸):</strong> نقشه حرارتی آب‌وهوا (شکل ۶) نشان می‌دهد که بارش برف میانگین تأخیر شبکه را بیش از دو برابر می‌کند و تأخیر اتوبوس را به بالای ۱۰ دقیقه می‌رساند. نمودار مسیرها (شکل ۷) یک نکته پنهان را فاش می‌کند: اگر فقط تعداد شکایت‌ها را ببینیم، مترو بیشترین شکایت را دارد چون مسافر بسیار بیشتری جابه‌جا کرده؛ اما وقتی شکایت‌ها را به نسبت هر ۱۰,۰۰۰ مسافر حساب می‌کنیم، خطوط حومه‌ای پرمشکل‌ترین مسیرها هستند. به خصوص اسکوتر و دوچرخه در مناطق حومه شهر به دلیل نبود جای پارک مناسب در پیاده‌روها رها می‌شوند و نارضایتی مردم در آنجا ۵ برابر مناطق مرکزی است.</p>
"""


# ==============================================================================
# FLUENT, SIMPLE & CLEAR PERSIAN PROSE — TASK 2
# ==============================================================================
FA_TASK2_SEC_2_1 = """
<h3>۲.۱ اصول طراحی نمودارها و سادگی درک برای بیننده</h3>
<p>هدف اصلی در طراحی نمودارهای این گزارش، انتقال سریع و بدون ابهام اطلاعات به مدیران شهری و تحلیل‌گران بوده است. برای رسیدن به این هدف، از نمودارهای گمراه‌کننده مثل نمودارهای دایره‌ای، اشکال سه‌بعدی یا محورهای دوگانه نامتقارن دوری شده است. در تمام مقایسه‌ها، داده‌ها روی خطوط و محورهای مشترک قرار گرفته‌اند تا چشم بیننده به سادگی متوجه اختلاف‌ها و فاصله‌ها شود.</p>
<p>برای ایجاد آرامش بصری، پالت رنگی محدودی انتخاب شده است: رنگ سرمه‌ای برای ساختار کلی و محورها استفاده شده و رنگ فیروزه‌ای فقط برای جلب توجه به پیام‌ها و نقاط کلیدی به کار رفته است. به این ترتیب، نگاه خواننده بدون سردرگمی مستقیماً روی موضوعات مهم مثل تغییر رتبه شهرها یا ضرردهی وسایل اشتراکی می‌نشیند. همچنین استفاده از نمودارهای پیشرفته مثل پلات باران‌ابری کمک کرده تا به جای یک میانگین ساده، واقعیت توزیع و معطلی مسافران به روشنی دیده شود.</p>
"""

FA_TASK2_SEC_2_2 = """
<h3>۲.۲ جمع‌بندی یافته‌های مهم پروژه از دل داده‌ها</h3>
<p>بررسی ۵,۰۰۰ رکورد عملکرد حمل‌ونقل شهری چهار نتیجه اصلی و بسیار شفاف را پیش روی ما قرار داد:</p>
<ol>
  <li><strong>ضرر سنگین دوچرخه و اسکوتر در برابر سودآوری مترو:</strong> مترو ستون اصلی جابه‌جایی و هوای پاک در شهرهاست. مترو به تنهایی نزدیک به ۶۳٪ مسافران را جابه‌جا کرده و ۷۰٪ صرفه‌جویی کربن را به همراه دارد و سودآور است. اما دوچرخه و اسکوتر اشتراکی با اینکه یک‌چهارم رکوردهای ثبت‌شده را شامل می‌شوند، فقط ۱٪ از مسافران را جابه‌جا کرده و نزدیک به ۹ میلیون یورو ضرر به بار آورده‌اند. هر سفر اسکوتر ۲۰ یورو ضرر خالص ایجاد می‌کند، بنابراین تبلیغ برای افزایش سفر با اسکوتر در قراردادهای فعلی فقط ضرر شهرداری را بیشتر می‌کند.</li>
  <li><strong>خطای آماری در مقایسه سود شهرها:</strong> در آمار خام، شهر مادرید ضررده‌ترین و برلین سودده به نظر می‌رسید. اما این نتیجه‌گیری اشتباه به خاطر ترکیب نامتوازن داده‌ها بود. با یکسان‌سازی سهم وسایل نقلیه، برلین به رتبه ۱۱ سقوط کرد و مادرید ثابت کرد که یکی از پرتقاضاترین و باکیفیت‌ترین سیستم‌های حمل‌ونقل را دارد.</li>
  <li><strong>گرفتار شدن اتوبوس‌ها در ترافیک و روزهای برفی:</strong> اتوبوس شهری بیشترین تأخیر (میانگین ۶.۵ دقیقه) و کمترین وقت‌شناسی (۷۵٪) را در شبکه دارد. بارش برف این مشکل را دو برابر می‌کند و تأخیر اتوبوس را به بالای ۱۰ دقیقه می‌رساند. همچنین در روزهای جشن و رویدادهای بزرگ، مسافران ۲۶٪ بیشتر می‌شوند ولی تأخیر هم ۳۱٪ جهش پیدا می‌کند.</li>
  <li><strong>بحران رها شدن اسکوترها در پیاده‌روهای حاشیه شهر:</strong> با اینکه شمار کل شکایات مترو به خاطر جمعیت زیادش بالاست، اما نرخ شکایت به ازای هر ۱۰ هزار مسافر نشان داد که مسیرهای حومه‌ای بیشترین نارضایتی را دارند. اسکوترها و دوچرخه‌ها در حاشیه شهرها به خاطر نبود پارکینگ استاندارد در پیاده‌رو رها می‌شوند و باعث شکایت شهروندان شده‌اند.</li>
</ol>
"""

FA_TASK2_SEC_2_3 = """
<h3>۲.۳ بررسی عملکرد و محدودیت‌های داشبورد تعاملی</h3>
<p>داشبورد تعاملی به گونه‌ای طراحی شده که مدیران بتوانند به سرعت وضعیت شبکه را ببینند و سناریوهای مختلف را با چند کلیک فیلتر کنند. برای مثال، اگر ناوگان سطحی (اتوبوس و تراموا) را در روزهای بارانی و برفی فیلتر کنیم، فوراً مشخص می‌شود که وقت‌شناسی به ۷۲٪ افت می‌کند و تأخیر به ۷.۴ دقیقه می‌رسد. با این حال، چند محدودیت هم وجود دارد: اول اینکه گزارش‌های کاغذی امکان کار تعاملی با نمودارها را ندارند؛ دوم اینکه داده‌ها به صورت میانگین روزانه ثبت شده‌اند و ترافیک ساعات اوج صبح و عصر را به تفکیک نشان نمی‌دهند؛ و سوم اینکه هزینه‌های استهلاک واگن‌ها و باتری‌ها در این داده‌ها لحاظ نشده است.</p>
"""

FA_TASK2_SEC_2_4 = """
<h3>۲.۴ چهار پیشنهاد عملی و کاربردی برای مدیران شهری</h3>
<p>برای بهبود پایدار وضعیت حمل‌ونقل و رضایت شهروندان، چهار اقدام فوری و مهم پیشنهاد می‌شود:</p>
<ol>
  <li><strong>اصلاح فوری قراردادهای اسکوتر و دوچرخه برقی:</strong> توقف کمپین‌های پرهزینه تبلیغاتی در ساختار فعلی. تغییر مدل پرداخت به پیمانکاران جمع‌آوری و شارژ، کاهش تعداد وسایل در ماه‌های خلوت سال (به‌ویژه ماه اکتبر)، و ادغام بلیت دوچرخه و اسکوتر در کارت‌های تخفیف‌دار مترو.</li>
  <li><strong>ساخت خطوط ویژه اتوبوس تندرو (BRT):</strong> حل مشکل تأخیر ۶.۵ دقیقه‌ای اتوبوس از طریق جداسازی خطوط در خیابان‌های اصلی و هوشمندسازی چراغ‌های راهنمایی برای رساندن تأخیر به زیر ۵ دقیقه، همزمان با برقی‌سازی اتوبوس‌ها.</li>
  <li><strong>برنامه‌ریزی هوشمند برای روزهای برفی و رویدادهای بزرگ:</strong> تنظیم خودکار برنامه‌ها بر اساس پیش‌بینی هواشناسی (مثل نمک‌پاشی پیشگیرانه و تزریق اتوبوس کمکی در برف) و آماده‌باش نگه داشتن ۲۵٪ قطار ذخیره در روزهای جشن و رویدادهای پرجمعیت.</li>
  <li><strong>ساماندهی ایستگاه‌ها در مناطق حومه شهر:</strong> اختصاص بودجه مناسب به محله‌های حاشیه‌ای برای ساخت توقفگاه‌های منظم دوچرخه و اسکوتر و ایجاد شیب‌راه‌های ویژه برای راحتی تردد سالمندان و معلولان.</li>
</ol>
"""


# ==============================================================================
# SINCERE, ARTICULATE STUDENT REFLECTIONS (صدای صمیمانه، ساده و واقعی دانشجو)
# ==============================================================================
FA_REFLECTIONS = {
    "sec1_1": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · شروع کار و تمیزکاری داده‌ها</div>
        <p>«وقتی اول کار فایل اکسل رو باز کردم، دیدم تاریخ‌ها به شکل عددهای عجیبی مثل ۴۵۲۹۲ ذخیره شدن و تعداد مسافران مترو اصلاً با وسایلی مثل دوچرخه قابل مقایسه نیست. اگر همون اول بدون حساب و کتاب میانگین می‌گرفتم، کل نتایج اشتباه از آب درمی‌اومد. تبدیل تاریخ‌ها به تقویم استاندارد و محاسبه هزینه‌ها به ازای هر مسافر، مهم‌ترین کاری بود که پایه بقیه تحلیل‌ها رو محکم کرد.»</p>
      </div>
    """,
    "sec1_2": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · تفاوت بزرگ وسایل نقلیه</div>
        <p>«بررسی آمارها خیلی زود بهم نشون داد که تکیه کردن به یک میانگین ساده چقدر می‌تونه گمراه‌کننده باشه. وقتی مترو روزی ۲۴ هزار مسافر داره ولی اسکوتر فقط ۳۵۰ نفر، چیزی به اسم "مسافر متوسط" معنی نداره. فهمیدم درآمد و شلوغی دست متروئه، اما موضوع تأخیر و معطلی چیزیه که همه مسافران در هر وسیله‌ای باهاش دست‌وپنجه نرم می‌کنن.»</p>
      </div>
    """,
    "fig1": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · پیدا کردن بهترین زمان برای تعمیرات</div>
        <p>«توی شکل ۱ هدفم این نبود که فقط چند تا خط ساده بکشم. می‌خواستم ریتم زندگی شهری در اروپا رو نشون بدم. وقتی دیدم در روزهای کاری مسافران ۳۴٪ بیشترن و در ماه اکتبر با یک افت ۲۷ درصدی روبرو می‌شیم، به این نتیجه رسیدم که این بهترین راهنما برای مدیرانه: شما نمی‌تونید ناوگان رو توی شلوغی فروردین و اردیبهشت تعمیر کنید، اما مهر و آبان بهترین فرصت برای سرویس اساسی وسایله.»</p>
      </div>
    """,
    "fig2": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · کشف هیجان‌انگیز خطای آماری</div>
        <p>«این یکی از جالب‌ترین لحظات کار من بود! اول که نمودار سود شهرها رو کشیدم، برلین سودده به نظر می‌رسید و مادرید انگار غرق در ضرر بود. اما وقتی دقیق‌تر شدم، دیدم مادرید فقط به خاطر سهم بیشتر رکوردهای اسکوتر زیان‌ده ثبت شده. به محض اینکه سهم وسایل رو برابر کردم، همه چیز برگشت: برلین به رتبه ۱۱ سقوط کرد و مادرید نشون داد چقدر تقاضای واقعی بالایی داره.»</p>
      </div>
    """,
    "fig3": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · پرده‌برداری از ضرر ۲۰ یورویی اسکوتر</div>
        <p>«توی تبلیغات شهری همیشه از اسکوتر و دوچرخه به عنوان نجات‌بخش محیط‌زیست صحبت می‌شه. اما حساب و کتاب ریاضی بهم نشون داد که هر سفر اسکوتر ۱.۵۹ یورو کرایه می‌گیره ولی نگهداری و شارژش ۲۲ یورو خرج برمی‌داره؛ یعنی ۲۰ یورو ضرر خالص در هر سفر! از اون طرف مترو علاوه بر پاکیزگی، سودده هم هست. نشون دادن این دو تا نمودار کنار هم نشون می‌ده که تصمیم‌گیری باید بر اساس واقعیت اقتصادی باشه نه شعار.»</p>
      </div>
    """,
    "fig4": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · انتخاب نموداری که واقعیت رو پنهان نکنه</div>
        <p>«نخواستم برای تأخیرها یک نمودار میله‌ای ساده بکشم، چون یک عدد میانگین، معطلی و خستگی مردم در ایستگاه رو پنهان می‌کنه. با نمودار باران‌ابری خواستم هر کسی در یک نگاه ببینه که اتوبوس‌ها چقدر دنباله تأخیر طولانی دارن و تا ۱۲ دقیقه مردم رو معطل می‌کنن، در حالی که مترو و تراموا ثبات خیلی بهتری دارند.»</p>
      </div>
    """,
    "fig5": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · تأخیر و افت رضایت مردم</div>
        <p>«مقایسه مستقیم تأخیر و رضایت مسافران ثابت کرد که معطلی بالای ۶ دقیقه اعتماد مردم رو از بین می‌بره. اما چیزی که برام خیلی جالب بود، روزهای جشن و مسابقات بود: مسافرها زیاد می‌شن، ولی چون قطار اضافه پیش‌بینی نشده، تأخیرها بالا می‌ره و خاطره بدی توی ذهن مردم ساخته می‌شه.»</p>
      </div>
    """,
    "fig6_7": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · حل معمای شکایت‌ها در محله‌های حاشیه شهر</div>
        <p>«در آمار کل، مترو چون ۲۵ میلیون نفر رو جابه‌جا کرده بیشترین شکایت رو داشت. اما وقتی شکایت‌ها رو به ازای هر ۱۰ هزار نفر حساب کردم، دیدم خطوط حومه‌ای مشکل اصلی هستند. به ویژه اسکوتر و دوچرخه در حاشیه شهرها به خاطر نبود جا در پیاده‌روها رها می‌شن و صدای مردم رو درمیارن.»</p>
      </div>
    """,
    "dash": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · فراتر از عکس‌های ثابت به سمت ابزار زنده</div>
        <p>«تصاویر ثابت توی گزارش‌ها فقط یک سناریو رو نشون می‌دن. من این داشبورد رو ساختم تا هر مدیری بتونه خودش پشت فرمون داده‌ها بشینه. مثلاً با دو کلیک ببینه در روزهای برفی وضعیت اتوبوس‌ها چطور می‌شه و چطور وقت‌شناسی افت می‌کنه.»</p>
      </div>
    """,
    "sec2_1": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · احترام به وقت و چشم بیننده</div>
        <p>«هدفم این بود که گزارش شلوغ و خسته‌کننده نباشه. تمام نمودارهای دایره‌ای و گرافیک‌های سه‌بعدی رو کنار گذاشتم تا چشم بیننده گمراه نشه. با انتخاب رنگ سرمه‌ای برای متن و رنگ فیروزه‌ای برای پیام‌های کلیدی، خواستم هر المان دلیلی برای بودن داشته باشه.»</p>
      </div>
    """,
    "sec2_2": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · اتصال اقتصاد، عملیات و محیط‌زیست</div>
        <p>«جمع‌بندی این اطلاعات بهم نشون داد سازمان حمل‌ونقل شهری در واقع دو دنیای متفاوته: یکی سیستم ریلی موفق و پاک که خرج خودش رو درمیاره، و دیگری اسکوترهای پر از ضرر و اتوبوس‌های گیر افتاده در ترافیک. مدیریت درست یعنی دیدن این تفاوت‌ها، نه میانگین‌گیری‌های ساده‌لوحانه.»</p>
      </div>
    """,
    "sec2_3": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · صداقت علمی درباره محدودیت‌ها</div>
        <p>«هر چقدر هم که از این پروژه راضی باشم، باید مرزهای کار رو هم بگم. رکوردهای روزانه تفاوت شلوغی صبح و عصر رو تفکیک نمی‌کنه و استهلاک واگن‌ها هم در محاسبات مالی نیومده. گفتن این محدودیت‌ها نه تنها ضعف نیست، بلکه نشانه دقت کار علمیه.»</p>
      </div>
    """,
    "sec2_4": """
      <div class="reflection-box">
        <div class="tag"><span>✍️</span> یادداشت من · از تحلیل تا تصمیم‌گیری در اتاق مدیران</div>
        <p>«اگر قرار بود این نتایج رو به شهردار توضیح بدم، ۴ کار روشن پیشنهاد می‌کردم: اصلاح قرارداد اسکوترها برای بستن نشتی ضرر، ساخت خط ویژه اتوبوس، آماده‌باش برای برف، و ساخت جای پارک در حاشیه شهر. ارزش این نمودارها به تصمیم‌هاییه که بهشون قدرت می‌ده.»</p>
      </div>
    """,
}


def build_fa_html() -> None:
    df = pd.read_csv(DATA_CSV, parse_dates=["Date_ISO"])
    stats_df = pd.read_csv(TABLES_DIR / "table01_initial_statistics.csv")
    city_df = pd.read_csv(TABLES_DIR / "table03_city_summary.csv")

    t1_words = (
        count_words(FA_TASK1_SEC_1_1)
        + count_words(FA_TASK1_SEC_1_2)
        + count_words(FA_TASK1_FIG1_TEXT)
        + count_words(FA_TASK1_FIG2_TEXT)
        + count_words(FA_TASK1_FIG3_TEXT)
        + count_words(FA_TASK1_FIG4_TEXT)
        + count_words(FA_TASK1_FIG5_TEXT)
        + count_words(FA_TASK1_FIG6_7_TEXT)
    )
    t2_words = (
        count_words(FA_TASK2_SEC_2_1)
        + count_words(FA_TASK2_SEC_2_2)
        + count_words(FA_TASK2_SEC_2_3)
        + count_words(FA_TASK2_SEC_2_4)
    )

    records = df[
        [
            "YearMonth",
            "Country",
            "City",
            "Transport_Mode",
            "Route_Type",
            "Weather",
            "Event_Day",
            "Passengers",
            "Ticket_Revenue_EUR",
            "Operating_Cost_EUR",
            "Average_Delay_Minutes",
            "On_Time_Percentage",
            "CO2_Saved_KG",
            "Customer_Rating",
            "Accessibility_Complaints",
        ]
    ].to_dict(orient="records")
    data_json = json.dumps(records)

    countries = sorted(df["Country"].unique().tolist())
    cities = sorted(df["City"].unique().tolist())
    modes = sorted(df["Transport_Mode"].unique().tolist())
    routes = sorted(df["Route_Type"].unique().tolist())
    weathers = ["Clear", "Cloudy", "Rain", "Snow", "Windy", "Heatwave"]

    MODE_FA = {
        "Bike Share": "دوچرخه اشتراکی",
        "Bus": "اتوبوس شهری",
        "E-Scooter": "اسکوتر برقی",
        "Metro": "مترو شهری",
        "Park & Ride": "پارکینگ و سوار",
        "Tram": "تراموا",
    }
    ROUTE_FA = {
        "Central Corridor": "کریدور مرکزی",
        "Commercial Trunk": "خط مستقیم تجاری",
        "Suburban Feeder": "خط ارتباطی حومه‌ای",
    }
    WEATHER_FA = {
        "Clear": "آفتابی و صاف",
        "Cloudy": "ابری",
        "Rain": "بارانی",
        "Snow": "برفی",
        "Windy": "باد شدید",
        "Heatwave": "موج گرما",
    }
    COUNTRY_FA = {
        "France": "فرانسه",
        "Germany": "آلمان",
        "Italy": "ایتالیا",
        "Netherlands": "هلند",
        "Portugal": "پرتغال",
        "Spain": "اسپانیا",
    }
    CITY_FA = {
        "Amsterdam": "آمستردام",
        "Barcelona": "بارسلونا",
        "Berlin": "برلین",
        "Frankfurt": "فرانکفورت",
        "Hamburg": "هامبورگ",
        "Lisbon": "لیسبون",
        "Madrid": "مادرید",
        "Milan": "میلان",
        "Munich": "مونیخ",
        "Paris": "پاریس",
        "Porto": "پورتو",
        "Rotterdam": "روتردام",
    }

    def opts_fa(items, fa_dict=None):
        out = ['<option value="ALL">همه موارد</option>']
        for it in items:
            label = fa_dict.get(it, it) if fa_dict else it
            out.append(f'<option value="{it}">{label}</option>')
        return "\n".join(out)

    STAT_VAR_FA = {
        "Passengers": "تعداد مسافران روزانه",
        "Ticket_Revenue_EUR": "درآمد بلیت (€)",
        "Operating_Cost_EUR": "هزینه عملیاتی (€)",
        "Average_Delay_Minutes": "میانگین تأخیر (دقیقه)",
        "On_Time_Percentage": "درصد وقت‌شناسی (%)",
        "Energy_Consumption_kWh": "مصرف انرژی (کیلووات‌ساعت)",
        "CO2_Saved_KG": "صرفه‌جویی کربن (کیلوگرم)",
        "Customer_Rating": "رضایت مسافران (از ۵)",
        "Accessibility_Complaints": "شکایات دسترسی",
        "Net_Margin_EUR": "حاشیه سود خالص (€)",
        "Cost_Recovery_Pct": "درصد بازیافت هزینه (%)",
        "Cost_per_Pax_EUR": "هزینه هر مسافر (€)",
        "Fare_per_Pax_EUR": "کرایه هر مسافر (€)",
        "Complaints_per_10k_Pax": "شکایت در هر ۱۰ هزار مسافر",
        "CO2_per_kWh": "کاهش کربن در کیلووات‌ساعت",
    }

    stat_rows_html = []
    for _, r in stats_df.iterrows():
        v_label = STAT_VAR_FA.get(r["Variable"], r["Variable"])
        stat_rows_html.append(
            f"<tr><td><strong>{v_label}</strong></td>"
            f"<td class='num'>{r['Mean']:,.2f}</td>"
            f"<td class='num'>{r['SD']:,.2f}</td>"
            f"<td class='num'>{r['Median']:,.2f}</td>"
            f"<td class='num'>{r['IQR']:,.2f}</td>"
            f"<td class='num'>{r['Min']:,.2f}</td>"
            f"<td class='num'>{r['Max']:,.2f}</td>"
            f"<td class='num'>{r['Skewness']:+.2f}</td></tr>"
        )

    city_rows_html = []
    for _, r in city_df.iterrows():
        c_label = CITY_FA.get(r["City"], r["City"])
        cnt_label = COUNTRY_FA.get(r["Country"], r["Country"])
        is_neg = r["Net_Margin_EUR"] < 0
        cls = "hi" if is_neg else ""
        margin_str = f"€{r['Net_Margin_EUR']:,.2f}" if not is_neg else f"-€{abs(r['Net_Margin_EUR']):,.2f}"
        city_rows_html.append(
            f"<tr class='{cls}'><td>{cnt_label}</td><td><strong>{c_label}</strong></td>"
            f"<td class='num'>{int(r['Records']):,}</td>"
            f"<td class='num'>{int(r['Total_Passengers']):,}</td>"
            f"<td class='num'>{r['Mean_Passengers']:,.1f}</td>"
            f"<td class='num'>{r['Mean_Delay_Min']:.2f}</td>"
            f"<td class='num'>{r['Mean_OnTime_Pct']:.2f}%</td>"
            f"<td class='num' style='font-weight:700;'>{margin_str}</td>"
            f"<td class='num'>{r['Cost_Recovery_Pct']:.2f}%</td>"
            f"<td class='num'>{r['Mean_Rating']:.2f}</td>"
            f"<td class='num'>{r['Complaints_per_10k_Pax']:.2f}</td></tr>"
        )

    code_files = [
        ("style/palette.py", BASE_DIR / "style" / "palette.py"),
        ("scripts/01_data_prep_and_eda.py", BASE_DIR / "scripts" / "01_data_prep_and_eda.py"),
        ("scripts/02_charts.py", BASE_DIR / "scripts" / "02_charts.py"),
        ("scripts/03_diagrams.py", BASE_DIR / "scripts" / "03_diagrams.py"),
        ("scripts/04_dashboard.py", BASE_DIR / "scripts" / "04_dashboard.py"),
    ]
    appendix_snippets = []
    for title, p in code_files:
        if p.exists():
            code = html.escape(p.read_text(encoding="utf-8"))
            appendix_snippets.append(f"""
            <details class="code-fold">
              <summary><strong>کد پایتون: <code>{title}</code></strong> — برای دیدن کد کلیک کنید</summary>
              <pre><code>{code}</code></pre>
            </details>
            """)
    appendix_html = "\n".join(appendix_snippets)

    page_html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>ارزیابی پایداری حمل‌ونقل شهری در اروپا · گزارش تحلیلی (نسخه فارسی)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
  <style>
    :root {{
      --midnight: #002B49;
      --midnight-soft: #123B5A;
      --tiffany: #66C9BA;
      --tiffany-deep: #3AA89A;
      --paper: #F7FAFB;
      --white: #FFFFFF;
      --line: #E1E8EC;
      --mute: #5A6E7C;
      --text: #1C2D37;
      --mist: #E8F4F8;
      --teal: #005F73;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: var(--paper);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Vazirmatn", "Shabnam", system-ui, Tahoma, sans-serif;
      font-size: 14.5px;
      font-weight: 350;
      line-height: 1.85;
      direction: rtl;
      text-align: right;
      letter-spacing: -0.15px;
    }}
    code, pre {{
      font-family: 'JetBrains Mono', Consolas, monospace;
      font-size: 13px;
      direction: ltr;
      display: inline-block;
    }}
    .top-nav {{
      position: sticky;
      top: 0;
      z-index: 999;
      background: var(--midnight);
      color: var(--white);
      padding: 12px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 10px rgba(0,43,73,0.18);
      font-size: 13.5px;
    }}
    .top-nav .brand {{
      font-weight: 600;
      letter-spacing: 0.2px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .top-nav .brand span {{
      color: var(--tiffany);
      font-weight: 400;
      font-size: 12px;
    }}
    .top-nav .links {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
    }}
    .top-nav a {{
      color: var(--line);
      text-decoration: none;
      font-weight: 400;
      transition: color 0.15s ease;
    }}
    .top-nav a:hover {{
      color: var(--tiffany);
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px 20px 80px 20px;
    }}
    .hero-card {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-top: 5px solid var(--midnight);
      border-radius: 16px;
      padding: 28px 32px;
      margin-bottom: 24px;
      box-shadow: 0 2px 8px rgba(0,43,73,0.05);
    }}
    .hero-card h1 {{
      margin: 0 0 10px 0;
      font-size: 21px;
      line-height: 1.6;
      font-weight: 700;
      color: var(--midnight);
    }}
    .hero-card .sub {{
      color: var(--mute);
      font-size: 14px;
      margin-bottom: 20px;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      background: var(--paper);
      padding: 14px 18px;
      border-radius: 12px;
      border: 1px solid var(--line);
    }}
    .meta-item .label {{
      font-size: 11.5px;
      color: var(--mute);
      font-weight: 600;
      margin-bottom: 2px;
    }}
    .meta-item .val {{
      font-size: 14px;
      font-weight: 600;
      color: var(--midnight);
    }}
    .badge {{
      display: inline-block;
      padding: 2px 9px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 600;
      color: var(--white);
      background: var(--tiffany-deep);
      vertical-align: middle;
      margin-right: 6px;
    }}
    .badge.navy {{ background: var(--midnight); }}

    /* CLEAN PERSIAN KPI STRIP */
    .kpi-strip-fa {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}
    .kpi-card-fa {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 12px;
      padding: 14px 12px;
      text-align: center;
    }}
    .kpi-card-fa.hi {{
      background: var(--mist);
      border: 1.5px solid var(--tiffany-deep);
    }}
    .kpi-card-fa .label {{
      font-size: 12px;
      color: var(--mute);
      font-weight: 500;
      margin-bottom: 4px;
    }}
    .kpi-card-fa .val {{
      font-size: 20px;
      font-weight: 700;
      color: var(--midnight);
      direction: ltr;
      display: inline-block;
    }}
    .kpi-card-fa .sub {{
      font-size: 11px;
      color: var(--mute);
      margin-top: 4px;
    }}

    .section-card {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 16px;
      padding: 28px 32px;
      margin-bottom: 28px;
      box-shadow: 0 2px 8px rgba(0,43,73,0.04);
    }}
    h2 {{
      margin-top: 0;
      font-size: 18px;
      font-weight: 600;
      color: var(--midnight);
      padding-bottom: 12px;
      border-bottom: 2px solid var(--mist);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    h3 {{
      font-size: 15.5px;
      font-weight: 600;
      color: var(--midnight);
      margin: 26px 0 12px 0;
      padding-right: 10px;
      border-right: 3px solid var(--tiffany);
    }}
    p {{
      margin: 0 0 14px 0;
      text-align: justify;
    }}
    ol, ul {{
      margin: 0 0 16px 0;
      padding-right: 22px;
      padding-left: 0;
    }}
    li {{
      margin-bottom: 8px;
      text-align: justify;
    }}
    .fig-box {{
      background: var(--paper);
      border: 1.5px solid var(--line);
      border-radius: 12px;
      padding: 14px;
      margin: 22px 0;
      text-align: center;
    }}
    .fig-box img {{
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      display: block;
      margin: 0 auto;
      box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .fig-caption {{
      margin-top: 10px;
      font-size: 13px;
      color: var(--mute);
      text-align: right;
      line-height: 1.6;
      padding: 0 6px;
    }}
    .fig-caption strong {{
      color: var(--midnight);
    }}
    .reflection-box {{
      background: #F9FCFB;
      border-right: 3px solid var(--tiffany-deep);
      border-left: 1px solid var(--line);
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
      border-radius: 8px 3px 3px 8px;
      padding: 14px 18px;
      margin: 16px 0 22px 0;
      font-size: 14px;
      line-height: 1.8;
      color: var(--midnight-soft);
    }}
    .reflection-box .tag {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-weight: 600;
      font-size: 12px;
      color: var(--tiffany-deep);
      margin-bottom: 6px;
    }}
    .reflection-box p {{
      margin: 0;
    }}
    .table-wrap {{
      overflow-x: auto;
      margin: 18px 0;
      border: 1.5px solid var(--line);
      border-radius: 10px;
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      background: var(--white);
    }}
    table.data-table th {{
      background: var(--midnight);
      color: var(--white);
      padding: 10px 12px;
      font-weight: 600;
      text-align: right;
      white-space: nowrap;
    }}
    table.data-table th.num, table.data-table td.num {{
      text-align: left;
      direction: ltr;
    }}
    table.data-table td {{
      padding: 8px 12px;
      border-bottom: 1px solid var(--line);
    }}
    table.data-table tr:hover {{
      background: var(--mist);
    }}
    table.data-table tr.hi {{
      background: #FFF9F2;
    }}
    .dash-shell {{
      background: var(--paper);
      border: 1.5px solid var(--line);
      border-radius: 14px;
      padding: 20px;
      margin: 20px 0;
    }}
    .dash-filters {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 12px;
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 16px;
    }}
    .dash-filters label {{
      display: block;
      font-size: 12px;
      font-weight: 600;
      color: var(--midnight);
      margin-bottom: 4px;
    }}
    .dash-filters select {{
      width: 100%;
      padding: 6px 10px;
      border-radius: 8px;
      border: 1.5px solid var(--line);
      font-size: 12.5px;
      color: var(--midnight);
      background: var(--paper);
      font-family: inherit;
    }}
    .dash-kpis {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }}
    .dash-kpi {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 12px;
      padding: 12px 10px;
      text-align: center;
    }}
    .dash-kpi.claim {{
      background: var(--mist);
      border: 1.5px solid var(--tiffany);
    }}
    .dash-kpi .t {{ font-size: 12px; color: var(--mute); font-weight: 500; }}
    .dash-kpi .v {{ font-size: 20px; font-weight: 700; color: var(--midnight); margin: 3px 0; direction: ltr; }}
    .dash-kpi .s {{ font-size: 11px; color: var(--mute); }}
    .dash-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    @media (max-width: 900px) {{
      .dash-grid {{ grid-template-columns: 1fr; }}
      .top-nav {{ flex-direction: column; gap: 8px; align-items: flex-start; }}
    }}
    .dash-card {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 12px;
      padding: 10px;
    }}
    .site-footer {{
      margin-top: 48px;
      padding-top: 20px;
      border-top: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: var(--mute);
    }}
    .site-footer a {{
      color: var(--mute);
      text-decoration: underline;
    }}
    .site-footer a:hover {{
      color: var(--midnight);
    }}
    .ref-list p {{
      margin-bottom: 8px;
      padding-right: 18px;
      text-indent: -18px;
      font-size: 13px;
      direction: ltr;
      text-align: left;
    }}
    details.code-fold {{
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px 14px;
      margin-bottom: 10px;
    }}
    details.code-fold summary {{
      cursor: pointer;
      font-size: 13px;
      color: var(--midnight);
    }}
    details.code-fold pre {{
      margin-top: 10px;
      padding: 12px;
      background: var(--white);
      border: 1px solid var(--line);
      border-radius: 6px;
      overflow-x: auto;
      font-size: 12px;
      line-height: 1.5;
    }}
  </style>
</head>
<body>

  <nav class="top-nav">
    <div class="brand">
      پروژه مصورسازی داده‌ها
      <span>· پیش‌نویس گزارش دانشجو (شناسه: 25199053)</span>
    </div>
    <div class="links">
      <a href="#overview">نمای کلی</a>
      <a href="#roadmap">روند کار</a>
      <a href="#task1">بخش ۱ (مصورسازی)</a>
      <a href="#dashboard">داشبورد تعاملی</a>
      <a href="#task2">بخش ۲ (گزارش تحلیلی)</a>
      <a href="#references">منابع</a>
      <a href="#appendix">ضمیمه کدها</a>
    </div>
  </nav>

  <div class="container">

    <!-- HERO / ASSESSMENT METADATA -->
    <section id="overview" class="hero-card">
      <h1>ارزیابی عملکرد پایداری حمل‌ونقل شهری در اروپا: بررسی مصورسازی داده‌ها در پایتون و گزارش تحلیلی</h1>
      <div class="sub">پیش‌نویس اولیه برای بازخورد استاد راهنما · مجموعه داده: سازمان حمل‌ونقل EcoMove (سال‌های ۲۰۲۴ و ۲۰۲۵)</div>
      <div class="meta-grid">
        <div class="meta-item"><div class="label">شماره دانشجویی</div><div class="val">25199053</div></div>
        <div class="meta-item"><div class="label">درس و مقطع</div><div class="val">کارشناسی ارشد علم داده</div></div>
        <div class="meta-item"><div class="label">استاد درس</div><div class="val">احمد حسن (Ahmed Hassan)</div></div>
        <div class="meta-item"><div class="label">کلمات بخش ۱</div><div class="val">{t1_words} کلمه <span class="badge">هدف: ~۶۰۰</span></div></div>
        <div class="meta-item"><div class="label">کلمات بخش ۲</div><div class="val">{t2_words} کلمه <span class="badge">هدف: ~۹۰۰</span></div></div>
        <div class="meta-item"><div class="label">حجم کلی کار</div><div class="val">۱۵۰۰ کلمه عملی + {t1_words + t2_words} کلمه متن</div></div>
      </div>

      <!-- PURE PERSIAN KPI TILES (NO ENGLISH BANNER) -->
      <div class="kpi-strip-fa">
        <div class="kpi-card-fa"><div class="label">کل مسافران</div><div class="val">۴۰.۹۱ میلیون</div><div class="sub">۱۲ شهر اروپایی</div></div>
        <div class="kpi-card-fa"><div class="label">وقت‌شناسی</div><div class="val">۸۲.۱٪</div><div class="sub">میانگین شبکه</div></div>
        <div class="kpi-card-fa hi"><div class="label">میانگین تأخیر</div><div class="val">۴.۳۵ دقیقه</div><div class="sub">اتوبوس: ۶.۵۸ دقیقه</div></div>
        <div class="kpi-card-fa hi"><div class="label">پوشش هزینه</div><div class="val">۹۹.۶٪</div><div class="sub">دوچرخه: ۵.۲٪</div></div>
        <div class="kpi-card-fa"><div class="label">صرفه‌جویی کربن</div><div class="val">۴,۴۸۲ تن</div><div class="sub">سهم مترو: ۷۰.۳٪</div></div>
        <div class="kpi-card-fa"><div class="label">رضایت مسافران</div><div class="val">۴.۰۱ از ۵</div><div class="sub">میانگین کل</div></div>
      </div>
    </section>

    <!-- SECTION 0: PROJECT TOPOLOGY & STATUS -->
    <section id="roadmap" class="section-card" style="padding: 22px 28px; margin-bottom: 24px;">
      <h2>
        <span>روند کار و نمای کلی وضعیت پروژه</span>
        <span><span class="badge navy">وضعیت: ۸۵٪ تکمیل‌شده</span> <span class="badge">در انتظار بازخورد استاد</span></span>
      </h2>

      <p style="margin: 0 0 10px 0; font-size: 14px; color: var(--mute);">یک شمای کلی از ۶ مرحله پروژه، که رفت‌و‌برگشت‌ها میان اعتبارسنجی داده‌ها، ساخت شاخص‌ها، تولید نمودارها و بازخورد استاد را نشان می‌دهد.</p>

      <div class="fig-box" style="margin: 8px 0 12px 0; padding: 8px; background: var(--paper); border: 1.5px solid var(--line);">
        <img src="{b64_img('fig00_workflow_roadmap.png')}" alt="روند کار و وضعیت پیشرفت"/>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; background: var(--paper); border: 1px solid var(--line); border-radius: 10px; padding: 10px 18px; font-size: 13px; flex-wrap: wrap; gap: 8px;">
        <div><strong>مراحل انجام‌شده:</strong> <span style="color:var(--tiffany-deep); font-weight:600;">✓</span> بارگذاری و تمیزکاری داده · <span style="color:var(--tiffany-deep); font-weight:600;">✓</span> مهندسی ویژگی‌ها · <span style="color:var(--tiffany-deep); font-weight:600;">✓</span> تولید نمودارها · <span style="color:var(--tiffany-deep); font-weight:600;">✓</span> داشبورد تعاملی</div>
        <div><strong>تمرکز فعلی:</strong> <span class="badge" style="background:var(--tiffany-deep);">پیش‌نویس گزارش تحلیلی</span></div>
        <div><strong>گام بعدی:</strong> <span style="color:var(--mute); font-weight:600;">بازخورد استاد احمد حسن و نسخه نهایی Word</span></div>
      </div>
    </section>

    <!-- TASK 1 SECTION -->
    <section id="task1" class="section-card">
      <h2>
        <span>بخش ۱ — بررسی و مصورسازی داده‌ها با پایتون</span>
        <span><span class="badge navy">۷۰ نمره</span> <span class="badge">{t1_words} کلمه متن + کار عملی پایتون</span></span>
      </h2>

      <h3>۱.۱ بارگذاری داده‌ها، تمیزکاری و ساخت شاخص‌های جدید</h3>
      {FA_TASK1_SEC_1_1}

      <div class="fig-box">
        <img src="{b64_img('fig08_methodology_pipeline.png')}" alt="مراحل انجام کار"/>
        <div class="fig-caption"><strong>شکل الف (مراحل پنج‌گانه تحلیل در پایتون):</strong> فرآیند کار از بارگذاری اکسل خام و تبدیل تاریخ‌ها شروع شده و به ساخت شاخص‌های استاندارد، رسم نمودارها و ساخت داشبورد تعاملی منتهی می‌شود.</div>
      </div>
      {FA_REFLECTIONS['sec1_1']}

      <h3>۱.۲ آمار توصیفی اولیه و تفاوت وسایل نقلیه</h3>
      {FA_TASK1_SEC_1_2}

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>متغیر</th>
              <th class="num">میانگین</th>
              <th class="num">انحراف معیار</th>
              <th class="num">میانه</th>
              <th class="num">دامنه بین‌چارکی (IQR)</th>
              <th class="num">حداقل</th>
              <th class="num">حداکثر</th>
              <th class="num">چولگی</th>
            </tr>
          </thead>
          <tbody>
            {''.join(stat_rows_html)}
          </tbody>
        </table>
      </div>
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:12px;"><strong>جدول ۱:</strong> آمار توصیفی متغیرهای اصلی در ۵,۰۰۰ رکورد داده‌های سال‌های ۲۰۲۴ و ۲۰۲۵.</div>
      {FA_REFLECTIONS['sec1_2']}

      <h3>۱.۳ تحلیل نمودارها و یافته‌های کلیدی (شکل‌های ۱ تا ۸)</h3>

      {FA_TASK1_FIG1_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig01_monthly_demand_trend.png')}" alt="شکل ۱ روند فصلی تقاضا"/>
        <div class="fig-caption"><strong>شکل ۱ (روند فصلی تقاضا و تقویم کاری):</strong> تقاضای روزهای کاری ۳۴٪ بیشتر از آخر هفته‌هاست و ماه اکتبر با ۲۷٪ افت، بهترین زمان برای تعمیرات اساسی است.</div>
      </div>
      {FA_REFLECTIONS['fig1']}

      {FA_TASK1_FIG2_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig02_city_demand_comparison.png')}" alt="شکل ۲ مقایسه شهرها و تناقض سیمپسون"/>
        <div class="fig-caption"><strong>شکل ۲ (نمودار دمبلی — رفع خطای آماری سیمپسون):</strong> مقایسه سود خام و تعدیل‌شده در ۱۲ شهر اروپا نشان داد که سقوط برلین و موفقیت مادرید به خاطر تفاوت در سهم اسکوترها بوده است.</div>
      </div>
      {FA_REFLECTIONS['fig2']}

      {FA_TASK1_FIG3_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig03_mode_cost_recovery.png')}" alt="شکل ۳ اقتصاد سفر و حفظ محیط‌زیست"/>
        <div class="fig-caption"><strong>شکل ۳ (اقتصاد هر مسافر و بازدهی کاهش کربن):</strong> بخش الف نشان‌دهنده ضرر ۲۰ یورویی در هر سفر اسکوتر است. بخش ب نشان می‌دهد مترو به ازای هر تن کاهش کربن سودآور است ولی اسکوتر بسیار پرهزینه‌ است.</div>
      </div>
      {FA_REFLECTIONS['fig3']}

      {FA_TASK1_FIG4_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig04_delay_distribution_boxplot.png')}" alt="شکل ۴ توزیع تأخیرها"/>
        <div class="fig-caption"><strong>شکل ۴ (نمودار باران‌ابری تأخیرها):</strong> اتوبوس با بیشترین معطلی (میانگین ۶.۵ دقیقه) گلوگاه اصلی شبکه است، در حالی که مترو بسیار دقیق و منظم حرکت می‌کند.</div>
      </div>
      {FA_REFLECTIONS['fig4']}

      {FA_TASK1_FIG5_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig05_delay_rating_relationship.png')}" alt="شکل ۵ رابطه تأخیر و رضایت"/>
        <div class="fig-caption"><strong>شکل ۵ (رابطه تأخیر و رضایت مسافر):</strong> با افزایش تأخیر، رضایت به سرعت افت می‌کند. در روزهای شلوغ جشن و مسابقات، تأخیرها ۳۱٪ بالا می‌رود.</div>
      </div>
      {FA_REFLECTIONS['fig5']}

      {FA_TASK1_FIG6_7_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig06_weather_mode_delay_heatmap.png')}" alt="شکل ۶ نقشه حرارتی آب‌وهوا و تأخیر"/>
        <div class="fig-caption"><strong>شکل ۶ (اثر آب‌وهوا بر تأخیر وسایل نقلیه):</strong> بارش برف میانگین تأخیر شبکه را دو برابر می‌کند و اتوبوس را به تأخیر بالای ۱۰ دقیقه می‌رساند.</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig07_route_accessibility_rate.png')}" alt="شکل ۷ شکایت‌ها در مسیرهای مختلف"/>
        <div class="fig-caption"><strong>شکل ۷ (نرخ شکایت‌ها به ازای هر ۱۰ هزار مسافر):</strong> بیشترین شکایت‌ها مربوط به خطوط حومه‌ای است، چون اسکوترها و دوچرخه‌ها در پیاده‌روها رها می‌شوند.</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig09_mode_performance_matrix.png')}" alt="شکل ۸ مقایسه جامع وسایل نقلیه"/>
        <div class="fig-caption"><strong>شکل ۸ (ماتریس خلاصه مقایسه وسایل):</strong> این ماتریس نشان می‌دهد مترو ستون اصلی پاکیزگی و درآمد شبکه است.</div>
      </div>
      {FA_REFLECTIONS['fig6_7']}
    </section>

    <!-- INTERACTIVE DASHBOARD SECTION -->
    <section id="dashboard" class="section-card">
      <h2>
        <span>۱.۴ داشبورد تعاملی (بررسی سناریوهای مختلف)</span>
        <span class="badge">داشبورد زنده + تصاویر گزارش</span>
      </h2>
      <p style="margin-top:0;">با انتخاب فیلترهای زیر می‌توانید تأثیر شهر، وسیله نقلیه، آب‌وهوا و روزهای رویداد را روی تأخیر، مسافران، هزینه‌ها و رضایت مردم به صورت زنده بررسی کنید.</p>

      <div class="dash-shell">
        <div class="dash-filters">
          <div><label>کشور</label><select id="f-country" onchange="updateDash()">{opts_fa(countries, COUNTRY_FA)}</select></div>
          <div><label>شهر</label><select id="f-city" onchange="updateDash()">{opts_fa(cities, CITY_FA)}</select></div>
          <div><label>وسیله نقلیه</label><select id="f-mode" onchange="updateDash()">{opts_fa(modes, MODE_FA)}</select></div>
          <div><label>نوع مسیر</label><select id="f-route" onchange="updateDash()">{opts_fa(routes, ROUTE_FA)}</select></div>
          <div><label>آب‌وهوا</label><select id="f-weather" onchange="updateDash()">{opts_fa(weathers, WEATHER_FA)}</select></div>
          <div><label>روز رویداد خاص</label><select id="f-event" onchange="updateDash()"><option value="ALL">همه روزها</option><option value="No">روز عادی</option><option value="Yes">روز رویداد و شلوغی</option></select></div>
        </div>

        <div class="dash-kpis">
          <div class="dash-kpi"><div class="t">مجموع مسافران</div><div class="v" id="k-pax">-</div><div class="s" id="k-records">-</div></div>
          <div class="dash-kpi"><div class="t">وقت‌شناسی</div><div class="v" id="k-ontime">-</div><div class="s">هدف: ۸۵٪</div></div>
          <div class="dash-kpi claim"><div class="t">میانگین تأخیر</div><div class="v" id="k-delay">-</div><div class="s">دقیقه</div></div>
          <div class="dash-kpi claim"><div class="t">پوشش هزینه</div><div class="v" id="k-recovery">-</div><div class="s" id="k-margin">-</div></div>
          <div class="dash-kpi"><div class="t">کاهش کربن</div><div class="v" id="k-co2">-</div><div class="s">تن دی‌اکسید کربن</div></div>
          <div class="dash-kpi"><div class="t">رضایت مسافران</div><div class="v" id="k-rating">-</div><div class="s" id="k-comp">-</div></div>
        </div>

        <div class="dash-grid">
          <div class="dash-card"><div id="c-trend" style="height:280px;"></div></div>
          <div class="dash-card"><div id="c-mode" style="height:280px;"></div></div>
          <div class="dash-card"><div id="c-weather" style="height:280px;"></div></div>
          <div class="dash-card"><div id="c-route" style="height:280px;"></div></div>
        </div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig10_dashboard_overview.png')}" alt="شکل ۹ نمای پیش‌فرض داشبورد"/>
        <div class="fig-caption"><strong>شکل ۹ (نمای پیش‌فرض داشبورد):</strong> نمای کلی شبکه در حالت بدون فیلتر با پوشش هزینه ۹۹.۶٪ و میانگین تأخیر ۴.۳۵ دقیقه.</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig11_dashboard_filtered_scenario.png')}" alt="شکل ۱۰ سناریوی فیلترشده داشبورد"/>
        <div class="fig-caption"><strong>شکل ۱۰ (بررسی سناریوی باران و برف برای ناوگان سطحی):</strong> فیلتر کردن اتوبوس و تراموا در برف و باران نشان می‌دهد وقت‌شناسی تا ۷۲٪ افت کرده و تأخیر به ۷.۴ دقیقه می‌رسد.</div>
      </div>
      {FA_REFLECTIONS['dash']}
    </section>

    <!-- TASK 2 SECTION -->
    <section id="task2" class="section-card">
      <h2>
        <span>بخش ۲ — گزارش تحلیلی و راهبردی برای تصمیم‌گیری</span>
        <span><span class="badge navy">۳۰ نمره</span> <span class="badge">{t2_words} کلمه متن تحلیلی</span></span>
      </h2>

      {FA_TASK2_SEC_2_1}
      {FA_REFLECTIONS['sec2_1']}

      {FA_TASK2_SEC_2_2}

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>کشور</th>
              <th>شهر</th>
              <th class="num">تعداد رکورد</th>
              <th class="num">کل مسافران</th>
              <th class="num">میانگین مسافر</th>
              <th class="num">میانگین تأخیر</th>
              <th class="num">وقت‌شناسی</th>
              <th class="num">سود خالص (€)</th>
              <th class="num">پوشش هزینه</th>
              <th class="num">رضایت</th>
              <th class="num">شکایت در ۱۰ هزار</th>
            </tr>
          </thead>
          <tbody>
            {''.join(city_rows_html)}
          </tbody>
        </table>
      </div>
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:12px;"><strong>جدول ۲:</strong> مقایسه عملکرد حمل‌ونقل در ۱۲ شهر اروپایی. ردیف‌های رنگی شهرهایی را نشان می‌دهند که به خاطر هزینه‌های اسکوتر در ضرر هستند.</div>
      {FA_REFLECTIONS['sec2_2']}

      {FA_TASK2_SEC_2_3}
      {FA_REFLECTIONS['sec2_3']}

      {FA_TASK2_SEC_2_4}

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>موضوع تصمیم‌گیری</th>
              <th>بخش و شهر هدف</th>
              <th>شواهد به دست آمده از داده‌ها</th>
              <th>پیشنهاد عملی و راهکار</th>
            </tr>
          </thead>
          <tbody>
            <tr class="hi">
              <td><strong>۱. پایداری مالی</strong></td>
              <td>دوچرخه و اسکوتر اشتراکی (به‌ویژه مادرید، بارسلونا و برلین)</td>
              <td>دوچرخه فقط ۵.۲٪ و اسکوتر ۷.۴٪ از هزینه‌هاشون رو تأمین می‌کنند و حدود ۹ میلیون یورو ضرر زده‌اند (شکل ۳).</td>
              <td>تغییر قراردادهای شارژ و نگهداری، کم کردن تعداد وسایل در ماه‌های خلوت سال، و ادغام با بلیت مترو.</td>
            </tr>
            <tr>
              <td><strong>۲. رفع تأخیر و پاکیزگی هوا</strong></td>
              <td>شبکه اتوبوسرانی در تمام ۱۲ شهر</td>
              <td>اتوبوس بیشترین معطلی (۶.۵۸ دقیقه)، کمترین وقت‌شناسی (۷۵٪) و کمترین راندمان انرژی را دارد (شکل‌های ۴ و ۸).</td>
              <td>ساخت خطوط ویژه اتوبوس تندرو (BRT)، چراغ‌های راهنمایی هوشمند و خرید اتوبوس‌های برقی جدید.</td>
            </tr>
            <tr class="hi">
              <td><strong>۳. مقاومت در برابر برف و روزهای شلوغ</strong></td>
              <td>ناوگان خیابانی در برف و باران و روزهای جشن</td>
              <td>برف تأخیر شبکه را به بالای ۸ دقیقه می‌رساند (شکل ۶) و روزهای شلوغ تأخیر را ۳۱٪ بالا می‌برد (شکل ۵).</td>
              <td>اجرای برنامه‌های نمک‌پاشی خودکار با پیش‌بینی هواشناسی و آماده کردن ۲۵٪ قطار ذخیره در روزهای جشن.</td>
            </tr>
            <tr>
              <td><strong>۴. عدالت اجتماعی در محله‌های حاشیه</strong></td>
              <td>خطوط حومه‌ای و ایستگاه‌های اطراف شهر</td>
              <td>نرخ شکایت در خطوط حومه‌ای بالاترین مقدار را دارد، چون اسکوترها در پیاده‌روها رها می‌شوند (شکل ۷).</td>
              <td>ساخت جای پارک استاندارد برای دوچرخه و اسکوتر در حاشیه شهر و ایجاد شیب‌راه‌های ویژه برای ویلچر.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:12px;"><strong>جدول ۳:</strong> خلاصه چهار راهکار عملی متصل به یافته‌های نمودارها در ابعاد مالی، زیست‌محیطی، خدمات شهری و عدالت اجتماعی.</div>
      {FA_REFLECTIONS['sec2_4']}
    </section>

    <!-- REFERENCES SECTION -->
    <section id="references" class="section-card">
      <h2>
        <span>منابع و مراجع علمی</span>
        <span class="badge navy">ادبیات علمی</span>
      </h2>
      <div class="ref-list">
        <p>Banister, D. (2008) ‘The sustainable mobility paradigm’, <em>Transport Policy</em>, 15(2), pp. 73–80.</p>
        <p>Cleveland, W.S. and McGill, R. (1984) ‘Graphical perception: Theory, experimentation, and application to the development of graphical methods’, <em>Journal of the American Statistical Association</em>, 79(387), pp. 531–554.</p>
        <p>European Commission (2021) <em>The New EU Urban Mobility Framework</em> (COM(2021) 811 final). Brussels: European Commission.</p>
        <p>Few, S. (2012) <em>Show Me the Numbers: Designing Tables and Graphs to Enlighten</em>. 2nd edn. Burlingame, CA: Analytics Press.</p>
        <p>Few, S. (2013) <em>Information Dashboard Design: Displaying Data for At-a-Glance Monitoring</em>. 2nd edn. Burlingame, CA: Analytics Press.</p>
        <p>Munzner, T. (2014) <em>Visualization Analysis and Design</em>. Boca Raton, FL: CRC Press.</p>
        <p>Shneiderman, B. (1996) ‘The eyes have it: A task by data type taxonomy for information visualizations’, <em>Proceedings of the IEEE Symposium on Visual Languages</em>, Boulder, CO, 3–6 September, pp. 336–343.</p>
        <p>Tufte, E.R. (2001) <em>The Visual Display of Quantitative Information</em>. 2nd edn. Cheshire, CT: Graphics Press.</p>
        <p>Ware, C. (2021) <em>Information Visualization: Perception for Design</em>. 4th edn. Cambridge, MA: Morgan Kaufmann.</p>
        <p>Wertheimer, M. (1923) ‘Untersuchungen zur Lehre von der Gestalt II’, <em>Psychologische Forschung</em>, 4(1), pp. 301–350.</p>
      </div>
    </section>

    <!-- APPENDIX SECTION -->
    <section id="appendix" class="section-card">
      <h2>
        <span>ضمیمه — کدهای پایتون</span>
        <span class="badge navy">کدهای قابل بازتولید</span>
      </h2>
      <p style="margin-top:0;">تمامی مراحل بارگذاری، تمیزکاری داده‌ها، رسم نمودارها و ساخت داشبورد با پایتون انجام شده است. برای مشاهده کد هر بخش روی عنوان آن کلیک کنید.</p>
      {appendix_html}
    </section>

    <footer class="site-footer">
      <span>درس مصورسازی داده‌ها · شماره دانشجویی: 25199053 · پیش‌نویس برای بازخورد استاد</span>
      <span>زبان: <strong>فارسی</strong> · <a href="index.html">English</a></span>
    </footer>

  </div>

  <script>
    const RAW_DATA = {data_json};

    const FA_MODES = {{
      'Bike Share': 'دوچرخه اشتراکی',
      'Bus': 'اتوبوس شهری',
      'E-Scooter': 'اسکوتر برقی',
      'Metro': 'مترو شهری',
      'Park & Ride': 'پارکینگ و سوار',
      'Tram': 'تراموا'
    }};

    const FA_WEATHERS = {{
      'Clear': 'آفتابی',
      'Cloudy': 'ابری',
      'Rain': 'بارانی',
      'Snow': 'برفی',
      'Windy': 'باد شدید',
      'Heatwave': 'موج گرما'
    }};

    const FA_ROUTES = {{
      'Central Corridor': 'مرکزی',
      'Commercial Trunk': 'تجاری',
      'Suburban Feeder': 'حومه‌ای'
    }};

    function updateDash() {{
      const country = document.getElementById('f-country').value;
      const city = document.getElementById('f-city').value;
      const mode = document.getElementById('f-mode').value;
      const route = document.getElementById('f-route').value;
      const weather = document.getElementById('f-weather').value;
      const eventDay = document.getElementById('f-event').value;

      const rows = RAW_DATA.filter(r =>
        (country === 'ALL' || r.Country === country) &&
        (city === 'ALL' || r.City === city) &&
        (mode === 'ALL' || r.Transport_Mode === mode) &&
        (route === 'ALL' || r.Route_Type === route) &&
        (weather === 'ALL' || r.Weather === weather) &&
        (eventDay === 'ALL' || r.Event_Day === eventDay)
      );

      const n = rows.length || 1;
      const totalPax = rows.reduce((s, r) => s + r.Passengers, 0);
      const meanOnTime = rows.reduce((s, r) => s + r.On_Time_Percentage, 0) / n;
      const meanDelay = rows.reduce((s, r) => s + r.Average_Delay_Minutes, 0) / n;
      const totalRev = rows.reduce((s, r) => s + r.Ticket_Revenue_EUR, 0);
      const totalCost = rows.reduce((s, r) => s + r.Operating_Cost_EUR, 0);
      const netMargin = totalRev - totalCost;
      const recovery = totalCost > 0 ? (totalRev / totalCost * 100) : 0;
      const totalCO2 = rows.reduce((s, r) => s + r.CO2_Saved_KG, 0) / 1000.0;
      const meanRating = rows.reduce((s, r) => s + r.Customer_Rating, 0) / n;
      const totalComp = rows.reduce((s, r) => s + r.Accessibility_Complaints, 0);
      const compRate = totalPax > 0 ? (totalComp / totalPax * 10000) : 0;

      document.getElementById('k-pax').textContent = (totalPax / 1e6).toFixed(2) + ' میلیون';
      document.getElementById('k-records').textContent = rows.length.toLocaleString('fa-IR') + ' رکورد';
      document.getElementById('k-ontime').textContent = meanOnTime.toFixed(1) + '٪';
      document.getElementById('k-delay').textContent = meanDelay.toFixed(2) + ' دقیقه';
      document.getElementById('k-recovery').textContent = recovery.toFixed(1) + '٪';
      document.getElementById('k-margin').textContent = 'تراز: ' + (netMargin >= 0 ? '+' : '-') + (Math.abs(netMargin)/1e6).toFixed(2) + 'M €';
      document.getElementById('k-co2').textContent = totalCO2.toFixed(1) + ' تن';
      document.getElementById('k-rating').textContent = meanRating.toFixed(2);
      document.getElementById('k-comp').textContent = compRate.toFixed(2) + ' در ۱۰ هزار';

      if (typeof Plotly === 'undefined') return;

      const byMonth = {{}};
      rows.forEach(r => {{
        if (!byMonth[r.YearMonth]) byMonth[r.YearMonth] = {{sum: 0, cnt: 0}};
        byMonth[r.YearMonth].sum += r.Passengers;
        byMonth[r.YearMonth].cnt += 1;
      }});
      const mKeys = Object.keys(byMonth).sort();
      Plotly.react('c-trend', [{{
        x: mKeys,
        y: mKeys.map(k => byMonth[k].sum / byMonth[k].cnt),
        mode: 'lines+markers',
        line: {{color: '#002B49', width: 2.2}},
        marker: {{color: '#3AA89A', size: 5}}
      }}], {{
        title: {{text: 'روند میانگین تقاضای روزانه مسافران در ماه‌ها', font: {{size: 13, color: '#002B49', family: 'Vazirmatn'}}}},
        paper_bgcolor: '#FFFFFF', plot_bgcolor: '#F7FAFB',
        margin: {{l: 55, r: 20, t: 40, b: 40}},
        xaxis: {{tickangle: -45, font: {{size: 10}}}},
        yaxis: {{title: 'مسافر در روز'}}
      }}, {{displayModeBar: false, responsive: true}});

      const byMode = {{}};
      rows.forEach(r => {{
        if (!byMode[r.Transport_Mode]) byMode[r.Transport_Mode] = {{rev: 0, cost: 0}};
        byMode[r.Transport_Mode].rev += r.Ticket_Revenue_EUR;
        byMode[r.Transport_Mode].cost += r.Operating_Cost_EUR;
      }});
      const modeKeys = Object.keys(byMode).sort((a,b) => (byMode[a].rev/byMode[a].cost) - (byMode[b].rev/byMode[b].cost));
      const modeVals = modeKeys.map(k => byMode[k].rev / byMode[k].cost * 100);
      const modeLabels = modeKeys.map(k => FA_MODES[k] || k);
      Plotly.react('c-mode', [{{
        x: modeVals, y: modeLabels, orientation: 'h', type: 'bar',
        marker: {{color: modeVals.map(v => v < 100 ? '#66C9BA' : '#1A4A6B')}}
      }}], {{
        title: {{text: 'درصد پوشش هزینه‌ها با کرایه (%)', font: {{size: 13, color: '#002B49', family: 'Vazirmatn'}}}},
        paper_bgcolor: '#FFFFFF', plot_bgcolor: '#F7FAFB',
        margin: {{l: 110, r: 20, t: 40, b: 40}},
        xaxis: {{title: 'درصد پوشش هزینه (%)'}}
      }}, {{displayModeBar: false, responsive: true}});

      const wOrder = ['Clear', 'Cloudy', 'Windy', 'Heatwave', 'Rain', 'Snow'];
      const byW = {{}};
      rows.forEach(r => {{
        if (!byW[r.Weather]) byW[r.Weather] = {{d: 0, c: 0}};
        byW[r.Weather].d += r.Average_Delay_Minutes;
        byW[r.Weather].c += 1;
      }});
      const wKeys = wOrder.filter(k => byW[k]);
      const wVals = wKeys.map(k => byW[k].d / byW[k].c);
      const wLabels = wKeys.map(k => FA_WEATHERS[k] || k);
      Plotly.react('c-weather', [{{
        x: wLabels, y: wVals, type: 'bar',
        marker: {{color: wKeys.map(k => (k === 'Rain' || k === 'Snow') ? '#66C9BA' : '#1A4A6B')}}
      }}], {{
        title: {{text: 'میانگین تأخیر (دقیقه) در شرایط آب‌وهوایی', font: {{size: 13, color: '#002B49', family: 'Vazirmatn'}}}},
        paper_bgcolor: '#FFFFFF', plot_bgcolor: '#F7FAFB',
        margin: {{l: 45, r: 20, t: 40, b: 40}},
        yaxis: {{title: 'دقیقه'}}
      }}, {{displayModeBar: false, responsive: true}});

      const byR = {{}};
      rows.forEach(r => {{
        if (!byR[r.Route_Type]) byR[r.Route_Type] = {{comp: 0, pax: 0}};
        byR[r.Route_Type].comp += r.Accessibility_Complaints;
        byR[r.Route_Type].pax += r.Passengers;
      }});
      const rKeys = Object.keys(byR).sort((a,b) => (byR[a].comp/byR[a].pax) - (byR[b].comp/byR[b].pax));
      const rVals = rKeys.map(k => byR[k].comp / byR[k].pax * 10000);
      const rLabels = rKeys.map(k => FA_ROUTES[k] || k);
      const maxR = Math.max(...rVals);
      Plotly.react('c-route', [{{
        x: rVals, y: rLabels, orientation: 'h', type: 'bar',
        marker: {{color: rVals.map(v => v === maxR ? '#66C9BA' : '#1A4A6B')}}
      }}], {{
        title: {{text: 'شکایت‌ها در هر ۱۰ هزار مسافر بر حسب نوع مسیر', font: {{size: 13, color: '#002B49', family: 'Vazirmatn'}}}},
        paper_bgcolor: '#FFFFFF', plot_bgcolor: '#F7FAFB',
        margin: {{l: 90, r: 20, t: 40, b: 40}},
        xaxis: {{title: 'نرخ شکایت'}}
      }}, {{displayModeBar: false, responsive: true}});
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      updateDash();
      const params = new URLSearchParams(window.location.search);
      if (params.get('lang') === 'en') {{
        window.location.href = 'index.html';
      }}
    }});
  </script>
</body>
</html>
"""

    OUT_HTML_FA.write_text(page_html, encoding="utf-8")
    ROOT_INDEX_FA.write_text(page_html, encoding="utf-8")
    print(f"Built self-contained Persian review HTML: {OUT_HTML_FA}")
    print(f"Copied to root GitHub Pages: {ROOT_INDEX_FA}")
    print(f"Task 1 Persian word count: {t1_words} words")
    print(f"Task 2 Persian word count: {t2_words} words")
    print(f"Total Persian written prose: {t1_words + t2_words} words")


if __name__ == "__main__":
    build_fa_html()
