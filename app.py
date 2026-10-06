import random
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ser_el_tafouk_secret_key' # مفتاح الجلسة لتخزين الأسئلة والإجابات

QUESTIONS_DB = {
    "مبتدئ": [
        {
          "id": 1,
        "type": "multiple_choice",
        "prompt": "أي مما يلي يمثل مجموعة الأعداد الحقيقية R؟",
        "options": ["Q ∩ Q'", "Q ∪ Q'", "N ∪ Z", "Z ∪ Q"],
        "answer": "Q ∪ Q'"
    },
    {
        "id": 2,
        "type": "multiple_choice",
        "prompt": "ما هو ناتج تقاطع مجموعة الأعداد النسبية Q ومجموعة الأعداد غير النسبية Q'؟",
        "options": ["R", "Z", "Ø", "N"],
        "answer": "Ø"
    },
    {
        "id": 3,
        "type": "multiple_choice",
        "prompt": "الترتيب الصحيح لاحتواء مجموعات الأعداد هو:",
        "options": ["N ⊂ Z ⊂ Q ⊂ R", "R ⊂ Q ⊂ Z ⊂ N", "Z ⊂ N ⊂ Q ⊂ R", "N ⊂ Q ⊂ Z ⊂ R"],
        "answer": "N ⊂ Z ⊂ Q ⊂ R"
    },
    {
        "id": 4,
        "type": "multiple_choice",
        "prompt": "أي من العلاقات التالية تعبر عن احتواء الأعداد غير النسبية في الأعداد الحقيقية؟",
        "options": ["Q' ⊂ Z", "Q' ⊂ N", "Q' ⊂ R", "R ⊂ Q'"],
        "answer": "Q' ⊂ R"
    },
    {

        "id": 7,
        "type": "multiple_choice",
        "prompt": "أي من العبارات التالية صحيحة دائماً في مجموعة الأعداد الحقيقية؟",
        "options": [
            "لا يوجد جذر تربيعي لعدد حقيقي سالب",
            "يوجد جذر تربيعي لعدد حقيقي سالب",
            "الجذر التكعيبي لعدد حقيقي سالب غير معرف",
            "الأعداد غير النسبية هي أعداد صحيحة"
        ],
        "answer": "لا يوجد جذر تربيعي لعدد حقيقي سالب"
    },
    {
        "id": 8,
        "type": "multiple_choice",
        "prompt": "العدد الحقيقي يمكن تعريفه بأنه عدد يمكن كتابته على صورة a/b حيث b لا تساوي الصفر و a و b عددان صحيحان. هذا هو تعريف:",
        "options": ["العدد غير النسبي", "العدد النسبي", "العدد الطبيعي", "العدد الصحيح"],
        "answer": "العدد النسبي"
    },
    {
        "id": 9,
        "type": "multiple_choice",
        "prompt": "مجموعة الأعداد الحقيقية تتكون من اتحاد مجموعتين منفصلتين هما:",
        "options": ["N و Z", "Z و Q", "Q و Q'", "N و Q'"],
        "answer": "Q و Q'"
    },
    {
            "id": 12,
        "type": "multiple_choice",
        "prompt": "العدد 0.73 يعتبر عدداً نسبياً لأنه يمكن كتابته على الصورة:",
        "options": ["73/10", "73/100", "7.3/100", "73/1000"],
        "answer": "73/100"
    },
    {
        "id": 14,
        "type": "multiple_choice",
        "prompt": "العدد π + 2 ينتمي إلى مجموعة الأعداد:",
        "options": ["Q", "Q'", "Z", "N"],
        "answer": "Q'"
    },
    {
        "id": 15,
        "type": "multiple_choice",
        "prompt": "العدد 2.5 ينتمي إلى مجموعة الأعداد:",
        "options": ["Q'", "Q", "Z", "N"],
        "answer": "Q"
    },
    {

        "id": 21,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: جذر 3 .... R هو:",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∈"
    },
    {
        "id": 23,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: {3, جذر 4} .... Q هو:",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "⊂"
    },
    {
        "id": 24,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: جذر -4 .... R هو:",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∉"
    },
    {
        "id": 25,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: 0.72 .... Q هو:",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∈"
    },
    {
        "id": 27,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: Q .... R هو:",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "⊂"
    },
    {
        "id": 28,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: جذر 10 .... Q' هو:",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∈"
    },
    {
        "id": 29,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: | -7 | .... Q هو:",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∈"
    },
    {
        "id": 30,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: - جذر 19 على 3 .... Z هو:",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∉"
    },
    {
        "id": 31,
        "type": "multiple_choice",
        "prompt": "العدد جذر 18 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["3 و 4", "4 و 5", "5 و 6", "16 و 25"],
        "answer": "4 و 5"
    },
    {
        "id": 32,
        "type": "multiple_choice",
        "prompt": "العدد الجذر التكعيبي لـ 25 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["2 و 3", "3 و 4", "4 و 5", "8 و 27"],
        "answer": "2 و 3"
    },
    {
        "id": 33,
        "type": "multiple_choice",
        "prompt": "العدد - جذر 33 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["-5 و -4", "-6 و -5", "-7 و -6", "5 و 6"],
        "answer": "-6 و -5"
    },
    {
        "id": 34,
        "type": "multiple_choice",
        "prompt": "التقدير التقريبي للمقدار 3 جذر 34 لأقرب عدد صحيح يساوي تقريباً:",
        "options": ["15", "18", "21", "24"],
        "answer": "18"
    },
    {
        "id": 35,
        "type": "multiple_choice",
        "prompt": "التقدير التقريبي للمقدار 5 - الجذر التكعيبي لـ 126 لأقرب عدد صحيح يساوي تقريباً:",
        "options": ["0", "1", "-1", "2"],
        "answer": "0"
    },
    {
    "id": 37,
        "type": "multiple_choice",
        "prompt": "العلامة الصحيحة للمقارنة بين (الجذر التكعيبي لـ 25) و (جذر 9) هي:",
        "options": [">", "<", "=", "≥"],
        "answer": "<"
    },
    {
        "id": 38,
        "type": "multiple_choice",
        "prompt": "العلامة الصحيحة للمقارنة بين (- جذر 7) و (-2.6) هي:",
        "options": [">", "<", "=", "≤"],
        "answer": "<"
    },
    {
        "id": 39,
        "type": "multiple_choice",
        "prompt": "عند ترتيب الأعداد (6.36̄ ، 6 ، 7 ، جذر 40) تصاعدياً، يكون العدد الأصغر هو:",
        "options": ["6", "جذر 40", "6.36̄", "7"],
        "answer": "6"
    },
    {
        "id": 40,
        "type": "multiple_choice",
        "prompt": "أي من الأعداد التالية يمثل عدداً غير نسبي يقع بين 0.3 و 0.6؟",
        "options": ["0.4", "0.5", "جذر 3 على 3", "0.25"],
        "answer": "جذر 3 على 3"
    },
    {

"id": 45,
"type": "multiple_choice",
"prompt": "مجموعة حل المعادلة: X^2 + 25 = 0 حيث X تنتمي إلى R هي:",
"options": ["{5, -5}", "{5}", "{-5}", "Ø"],
"answer": "Ø"
},
{
"id": 46,
"type": "multiple_choice",
"prompt": "مربع مساحته 29 سم^2، طول ضلعه ينتمي إلى مجموعة الأعداد:",
"options": ["النسبية Q", "غير النسبية Q'", "الصحيحة Z", "الطبيعية N"],
"answer": "غير النسبية Q'"
},
{

"id": 49,
"type": "multiple_choice",
"prompt": "مكعب مساحته الكلية 300 سم^2، فإن طول حرفه يساوي جذر 50 سم، وهو عدد:",
"options": ["نسبي", "غير نسبي", "طبيعي", "صحيح"],
"answer": "غير نسبي"

          }
    ],
    "متوسط": [
          {
             "id": 51,
        "type": "multiple_choice",
        "prompt": "أي من المجموعات التالية يمثل محتواها بالكامل أعداداً حقيقية؟",
        "options": ["N ∪ Z ∪ Q ∪ Q'", "N ∩ Z ∩ Q", "Q' ∩ R", "Ø فقط"],
        "answer": "N ∪ Z ∪ Q ∪ Q'"
    },
    {
        "id": 53,
        "type": "multiple_choice",
        "prompt": "ما هي المجموعات التي ينتمي إليها العدد 19؟",
        "options": ["N, Z, Q, R", "Q, Q', R", "Z, Q' فقط", "N, Q' فقط"],
        "answer": "N, Z, Q, R"
    },
    {
        "id": 55,
        "type": "multiple_choice",
        "prompt": "العدد النسبة الذهبية (φ) يظهر بوضوح في الطبيعة في محار أحد الكائنات البحرية، وهو ينتمي إلى:",
        "options": ["Q", "Q'", "Z", "N"],
        "answer": "Q'"
    },
    {
        "id": 56,
        "type": "multiple_choice",
        "prompt": "أي من العلاقات التالية خاطئة رياضياً؟",
        "options": ["N ⊂ Z", "Z ⊂ Q", "Q ⊂ R", "Q' ⊂ Q"],
        "answer": "Q' ⊂ Q"
    },
    {
        "id": 57,
        "type": "multiple_choice",
        "prompt": "أي المجموعات التالية لا تحتوي على أي أعداد سالبة؟",
        "options": ["مجموعة الأعداد الطبيعية N", "مجموعة الأعداد الصحيحة Z", "مجموعة الأعداد النسبية Q", "مجموعة الأعداد الحقيقية R"],
        "answer": "مجموعة الأعداد الطبيعية N"
    },
    {
        "id": 58,
        "type": "multiple_choice",
        "prompt": "العدد الدوري 0.323232... الوارد في تمارين الكتاب يعتبر عدداً:",
        "options": ["نسبياً", "غير نسبي", "صحيحاً", "طبيعياً"],
        "answer": "نسبياً"
    },
    {
        "id": 59,
        "type": "multiple_choice",
        "prompt": "لماذا العدد جذر 12 عدد غير نسبي؟",
        "options": ["لأن 12 ليس مكعباً كاملاً", "لأن 12 ليس مربعاً كاملاً", "لأن 12 عدد سالب", "لأن 12 يساوي صفر"],
        "answer": "لأن 12 ليس مربعاً كاملاً"
    },
    {
        "id": 60,
        "type": "multiple_choice",
        "prompt": "لماذا العدد الجذر التكعيبي لـ 4 عدد غير نسبي؟",
        "options": ["لأن 4 ليس مربعاً كاملاً", "لأن 4 ليس مكعباً كاملاً", "لأن 4 عدد حقيقي سالب", "لأن 4 أكبر من الواحد"],
        "answer": "لأن 4 ليس مكعباً كاملاً"
    },
    {
        "id": 61,
        "type": "multiple_choice",
        "prompt": "العدد (جذر 19 + 11) المذكر في جدول حاول بنفسك هو عدد:",
        "options": ["نسبي", "غير نسبي", "طبيعي", "صحيح"],
        "answer": "غير نسبي"
    },
    {
        "id": 62,
        "type": "multiple_choice",
        "prompt": "العدد الكسري 2 وثلاثة أثمان (2 و 3/8) ينتمي إلى مجموعة الأعداد:",
        "options": ["Q", "Q'", "N", "الغير حقيقية"],
        "answer": "Q"
    },
    {
        "id": 65,
        "type": "multiple_choice",
        "prompt": "العدد (12 / 31) الوارد في تمارين تحديد النوع هو عدد:",
        "options": ["نسبي", "غير نسبي", "صحيح", "طبيعي"],
        "answer": "نسبي"
    },
    {
        "id": 66,
        "type": "multiple_choice",
        "prompt": "العدد (جذر 16 / 9) يساوي:",
        "options": ["4/3 وهو نسبي", "4/3 وهو غير نسبي", "16/9 وهو نسبي", "غير معرف"],
        "answer": "4/3 وهو نسبي"
    },
    {
        "id": 67,
        "type": "multiple_choice",
        "prompt": "العدد (جذر 9 + جذر 16) يساوي:",
        "options": ["5 وهو نسبي", "جذر 25 وهو غير نسبي", "7 وهو نسبي", "7 وهو غير نسبي"],
        "answer": "7 وهو نسبي"
    },
    {
        "id": 68,
        "type": "multiple_choice",
        "prompt": "العدد (الجذر التكعيبي لـ 16) هو عدد غير نسبي لأن:",
        "options": ["16 مربع كامل", "16 ليس مكعباً كاملاً", "16 عدد سالب", "16 ليس له جذر تربيعي"],
        "answer": "16 ليس مكعباً كاملاً"
    },
    {
        "id": 69,
        "type": "multiple_choice",
        "prompt": "ما هو الرمز الصحيح للفراغ التالي: جذر 13 .... Q' ؟",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∈"
    },
    {
        "id": 71,
        "type": "multiple_choice",
        "prompt": "ما هو الرمز الصحيح للفراغ التالي: | -4 | .... N ؟",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∈"
    },
    {
        "id": 72,
        "type": "multiple_choice",
        "prompt": "ما هو الرمز الصحيح للفراغ التالي: {جذر 8، جذر 9} .... Q ؟",
        "options": ["⊂", "⊄", "∈", "∉"],
        "answer": "⊄"
    },
    {
        "id": 73,
        "type": "multiple_choice",
        "prompt": "ما هو الرمز الصحيح للفراغ التالي: الجذر التكعيبي لـ 3 .... Q ؟",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∉"
    },
    {
        "id": 74,
        "type": "multiple_choice",
        "prompt": "العدد جذر 7 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["1 و 2", "2 و 3", "3 & 4", "4 و 5"],
        "answer": "2 و 3"
    },
    {
        "id": 75,
        "type": "multiple_choice",
        "prompt": "العدد جذر 63 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["6 و 7", "7 و 8", "8 و 9", "62 و 64"],
        "answer": "7 و 8"
    },
    {
        "id": 77,
        "type": "multiple_choice",
        "prompt": "العدد جذر 11 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["2 و 3", "3 و 4", "4 و 5", "9 و 16"],
        "answer": "3 و 4"
    },
    {
        "id": 78,
        "type": "multiple_choice",
        "prompt": "العدد جذر 132 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["10 و 11", "11 و 12", "12 و 13", "131 و 133"],
        "answer": "11 و 12"
    },
    {
        "id": 79,
        "type": "multiple_choice",
        "prompt": "العدد - جذر 95 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["-9 و -8", "-10 و -9", "-11 و -10", "9 و 10"],
        "answer": "-10 و -9"
    },
    {
        "id": 81,
        "type": "multiple_choice",
        "prompt": "إذا كان X عدد صحيح يحقق العلاقة: X < جذر 80 < X + 1، فما قيمة X؟",
        "options": ["7", "8", "9", "10"],
        "answer": "8"
    },
    {
        "id": 82,
        "type": "multiple_choice",
        "prompt": "إذا كان X عدد صحيح يحقق العلاقة: X < جذر 12 < X + 1، فما قيمة X؟",
        "options": ["2", "3", "4", "5"],
        "answer": "3"
    },
    {
        "id": 84,
        "type": "multiple_choice",
        "prompt": "التقدير التقريبي للمقدار (2 - جذر 8) على جذر 7 لأقرب عدد صحيح يساوي تقريباً:",
        "options": ["0", "1", "-1", "2"],
        "answer": "0"
    },
    {
        "id": 85,
        "type": "multiple_choice",
        "prompt": "أي من العلاقات التالية صحيحة للمقارنة بين جذر 96 والعدد 14؟",
        "options": ["جذر 96 > 14", "جذر 96 < 14", "جذر 96 = 14", "جذر 96 ≥ 14"],
        "answer": "جذر 96 < 14"
    },
    {

        "id": 87,
        "type": "multiple_choice",
        "prompt": "وفقاً للنقاش الوارد بالملف بين حمزة وآسر حول حصر (- جذر 5)، من منهما اتبع الطريقة الصحيحة بالخطوات؟",
        "options": ["آسر فقط", "حمزة فقط", "كلاهما خطأ", "كلاهما صحيح بنفس الدقة"],
        "answer": "حمزة فقط"
    },
    {
        "id": 88,
        "type": "multiple_choice",
        "prompt": "مجموعة حل المعادلة X^3 - 11 = 5 في R هي:",
        "options": ["{4}", "{2}", "{-2}", "Ø"],
        "answer": "{4}"
    },
    {
        "id": 89,
        "type": "multiple_choice",
        "prompt": "مجموعة حل المعادلة 2X^3 + 13 = 67 في R هي:",
        "options": ["{3}", "{27}", "{3, -3}", "Ø"],
        "answer": "{3}"
    },
    {
        "id": 90,
        "type": "multiple_choice",
        "prompt": "مجموعة حل المعادلة 2X^3 + 17 = 33 في R هي:",
        "options": ["{2}", "{8}", "{2, -2}", "Ø"],
        "answer": "{2}"
    },
    {
        "id": 91,
        "type": "multiple_choice",
        "prompt": "مجموعة حل المعادلة 2X^2 + 8 = 16 في R هي:",
"options": ["{2, -2}", "{جذر 2, - جذر 2}", "{2}", "Ø"],
"answer": "{2, -2}"
},
{
"id": 93,
"type": "multiple_choice",
"prompt": "مجموعة حل المعادلة 3X^2 - 1 = -13 في R هي:",
"options": ["{2, -2}", "{جذر -4}", "Ø", "{-4}"],
"answer": "Ø"
},
{
"id": 94,
"type": "multiple_choice",
"prompt": "مجموعة حل المعادلة (2 / X^3) + 5 = 21 (حيث X لا تساوي صفر) في R هي:",
"options": ["{1/2}", "{2}", "{-1/2}", "Ø"],
"answer": "{1/2}"
},
{
"id": 97,
"type": "multiple_choice",
"prompt": "مجموعة حل المعادلة 6X^2 - 3 = 4X^2 + 7 في Q هي:",
"options": ["{جذر 5, - جذر 5}", "Ø", "{5, -5}", "{5}"],
"answer": "Ø"
},
{
"id": 98,
"type": "multiple_choice",
"prompt": "مجموعة حل المعادلة (X - 1)^2 = 4 في Q هي:",
"options": ["{3, -1}", "{2, -2}", "{3}", "{1}"],
"answer": "{3, -1}"
},
{
"id": 100,
"type": "multiple_choice",
"prompt": "أيهما أكبر في المساحة أو الأبعاد وفقاً للمقارنة الهندسية الواردة بالصفحة الأخيرة؟",
"options": ["طول ضلع مربع مساحته 16 سم^2", "طول قطر مربع مساحته 9 سم^2", "كلاهما متساويان تماماً", "طول ضلع مربع مساحته 9 سم^2"],
"answer": "طول قطر مربع مساحته 9 سم^2"

        }
    ],
    "محترف": [
           {
             "id": 101,
        "type": "multiple_choice",
        "prompt": "أي من الرموز التالية يوضع في الفراغ: جذر 2 .... 2 ؟",
        "options": ["<", ">", "=", "≥"],
        "answer": "<"
    },
    {
        "id": 104,
        "type": "multiple_choice",
        "prompt": "ما هو الرمز الصحيح للفراغ التالي: | -4 | .... N ؟",
        "options": ["∈", "∉", "⊂", "⊄"],
        "answer": "∈"
    },
    {
           "id": 106,
        "type": "multiple_choice",
        "prompt": "العدد جذر 6 المذكور في التمارين ينتمي إلى:",
        "options": ["Q'", "Q", "Z", "N"],
        "answer": "Q'"
    },
    {
        "id": 107,
        "type": "multiple_choice",
        "prompt": "العدد الكسري (2 وربع) تحت الجذر التربيعي يساوي جذر (9/4) وهو ينتمي إلى:",
        "options": ["Q", "Q'", "Z", "N"],
        "answer": "Q"
    },
    {
        "id": 108,
        "type": "multiple_choice",
        "prompt": "العدد جذر 169 المذكور في التمارين يساوي 13، وهو ينتمي إلى المجموعة:",
        "options": ["Q'", "N", "الأعداد غير الحقيقية", "Z-"],
        "answer": "N"
    },
    {
        "id": 109,
        "type": "multiple_choice",
        "prompt": "العدد (الجذر التكعيبي لـ 1) يساوي 1، وهو عدد:",
        "options": ["نسبي وصحيح وطبيعي", "غير نسبي", "سالب", "غير حقيقي"],
        "answer": "نسبي وصحيح وطبيعي"
    },
    {
        "id": 110,
        "type": "multiple_choice",
        "prompt": "العدد (محيط الدائرة / طول قطرها) يعبر دائماً عن الثابت الرياضي:",
        "options": ["π وهو غير نسبي", "φ وهو نسبي", "π وهو نسبي", "φ وهو غير نسبي"],
        "answer": "π وهو غير نسبي"
    },
    {
        "id": 111,
        "type": "multiple_choice",
        "prompt": "العدد جذر 18 يكون أقرب على خط الأعداد إلى العدد الصحيح:",
        "options": ["4", "5", "3", "6"],
        "answer": "4"
    },
    {
        "id": 112,
        "type": "multiple_choice",
        "prompt": "العدد الجذر التكعيبي لـ 25 يكون أقرب على خط الأعداد إلى العدد الصحيح:",
        "options": ["3", "2", "4", "5"],
        "answer": "3"
    },
    {
        "id": 113,
        "type": "multiple_choice",
        "prompt": "العدد - جذر 33 يكون أقرب على خط الأعداد إلى العدد الصحيح:",
        "options": ["-6", "-5", "-4", "-7"],
        "answer": "-6"
    },
    {
        "id": 114,
        "type": "multiple_choice",
        "prompt": "العدد جذر 5 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["2 و 3", "1 و 2", "3 و 4", "4 و 5"],
        "answer": "2 و 3"
    },
    {
        "id": 115,
        "type": "multiple_choice",
        "prompt": "العدد جذر 14 يقع بين العددين الصحيحين المتتاليين:",
        "options": ["3 و 4", "2 و 3", "4 و 5", "13 و 15"],
        "answer": "3 و 4"
    },
    {

        "id": 118,
        "type": "multiple_choice",
        "prompt": "إذا كان y و X عددين صحيحين متتاليين يحصران العدد جذر 57، فما قيمة y + X؟",
        "options": ["15", "13", "11", "17"],
        "answer": "15"
    },
    {
        "id": 120,
        "type": "multiple_choice",
        "prompt": "ما هو الرمز الصحيح للمقارنة في العبارة: -2 .... - جذر 24 ؟",
        "options": [">", "<", "=", "≤"],
        "answer": ">"
    },
    {
        "id": 121,
        "type": "multiple_choice",
        "prompt": "العدد 0.25 ينتمي إلى المجموعات الممكنة التالية:",
        "options": ["Q, R", "Z, Q, R", "N, Z, Q, R", "Q' , R"],
        "answer": "Q, R"
    },
    {
        "id": 122,
        "type": "multiple_choice",
        "prompt": "العدد جذر 100 يساوي 10، المجموعات الممكنة التي ينتمي إليها هي:",
        "options": ["N, Z, Q, R", "Q, R فقط", "Q', R", "Z, Q, R فقط"],
        "answer": "N, Z, Q, R"
    },
    {
        "id": 123,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: الجذر التكعيبي لـ 3 .... Q هو:",
        "options": ["∉", "∈", "⊂", "⊄"],
        "answer": "∉"
    },
    {
        "id": 124,
        "type": "multiple_choice",
        "prompt": "الرمز المناسب في العبارة: مجموع الأعداد (2 وثلاثة أرباع) .... Z هو:",
        "options": ["∉", "∈", "⊂", "⊄"],
        "answer": "∉"
    },
    {
     
        "id": 126,
        "type": "multiple_choice",
        "prompt": "مجموعة حل المعادلة: 4X^3 = -32 في Q هي:",
        "options": ["{-2}", "{2}", "Ø", "{-8}"],
        "answer": "{-2}"
    },
    {
        "id": 134,
        "type": "multiple_choice",
        "prompt": "مجموعة حل المعادلة: 2(X^2 - 1) = -10 في R هي:",
        "options": ["Ø", "{جذر -4}", "{2, -2}", "{-2}"],
        "answer": "Ø"
    },
    {
        "id": 135,
        "type": "multiple_choice",
        "prompt": "في حل المعادلة 3X^2 + 5 = -4 بالخطوات، نجد أن X^2 تساوي:",
        "options": ["-3", "3", "-9", "-1"],
        "answer": "-3"
    },
    {
        "id": 136,
        "type": "multiple_choice",
        "prompt": "في حل المعادلة 64X^3 - 2 = -29 بالخطوات، نجد أن X^3 تساوي:",
        "options": ["-27/64", "-31/64", "-27", "-3/4"],
        "answer": "-27/64"
    },
    {
        "id": 137,
        "type": "multiple_choice",
        "prompt": "مجموعة حل المعادلة: (5X - 3)^3 - 2 = 6 في Q هي:",
        "options": ["{1}", "{2}", "Ø", "{5}"],
        "answer": "{1}"
    },
    {
        "id": 139,
        "type": "multiple_choice",
        "prompt": "مجموعة حل المعادلة: X^2 + 4 = 0 في R هي:",
        "options": ["Ø", "{2, -2}", "{-2}", "{2}"],
        "answer": "Ø"
       }
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 5))
    action = request.form.get('action', 'select')
   
    pool = QUESTIONS_DB.get(level, QUESTIONS_DB.get("متوسط", []))
   
    if request.method == 'GET' or action == 'select':
        return render_template_string(MAIN_TEMPLATE, level=level, num_questions=num_questions)
       
    elif action == 'generate':
        selected_questions = random.sample(pool, min(num_questions, len(pool))) if pool else []
        session['questions'] = selected_questions
        session['level'] = level
        session['current_index'] = 0
        session['user_answers'] = {}
        return redirect(url_for('quiz_step'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_step():
    questions = session.get('questions', [])
    current_index = session.get('current_index', 0)
    level = session.get('level', 'متوسط')
   
    if not questions:
        return redirect(url_for('index'))
       
    if request.method == 'POST':
        ans = request.form.get('current_answer')
        
        user_answers = session.get('user_answers', {})
        user_answers[str(current_index)] = {
            "prompt": questions[current_index]['prompt'],
            "user_ans": ans if ans else "لم تتم الإجابة",
            "correct_ans": questions[current_index]['answer'],
            "is_correct": (ans == questions[current_index]['answer'])
        }
        session['user_answers'] = user_answers
       
        current_index += 1
        session['current_index'] = current_index
       
    if current_index >= len(questions):
        return redirect(url_for('results'))
       
    current_question = questions[current_index]
   
    return render_template_string(
        QUIZ_TEMPLATE,
        level=level,
        question=current_question,
        current_num=current_index + 1,
        total_questions=len(questions),
        num_questions=len(questions)
    )

@app.route('/results')
def results():
    user_answers = session.get('user_answers', {})
    level = session.get('level', 'متوسط')
   
    score = 0
    total = len(user_answers)
    results_list = []
   
    for idx, data in sorted(user_answers.items(), key=lambda x: int(x[0])):
        if data['is_correct']:
            score += 1
        results_list.append({
            "id": int(idx) + 1,
            "prompt": data['prompt'],
            "user_ans": data['user_ans'],
            "correct_ans": data['correct_ans'],
            "is_correct": data['is_correct']
        })
       
    return render_template_string(
        RESULT_TEMPLATE,
        level=level,
        score=score,
        total=total,
        results=results_list
    )

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - تصميم الامتحان</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .header-badge { text-align: center; color: #d4a373; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        .section-title { font-weight: bold; color: #222; font-size: 15px; margin-bottom: 10px; }
        .levels-container { display: flex; gap: 10px; margin-bottom: 20px; }
        .level-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 12px; background: #fff; cursor: pointer; text-align: center; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .level-btn input { display: none; }
        .level-btn.active, .level-btn:hover { border-color: #114b3e; background: #e8f5e9; color: #114b3e; }
        .slider-container { margin-bottom: 25px; background: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; color: #114b3e; }
        input[type=range] { width: 100%; accent-color: #114b3e; cursor: pointer; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .whatsapp-link-btn { display: block; width: 100%; background: #25d366; color: white; padding: 13px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 15px; text-decoration: none; box-shadow: 0 4px 10px rgba(37,211,102,0.3); transition: 0.3s; margin-top: 15px; box-sizing: border-box; }
        .whatsapp-link-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">منصة سر التفوق التعليمية ✨</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">اختبر معلوماتك الآن بكل سهولة ⏱️</div>
       
        <form method="POST">
            <input type="hidden" name="action" value="generate">
            <div class="section-title">اختيار مستوى الصعوبة الدرس الاول رياضيات 2 اعدادي</div>
            <div class="levels-container">
                <label class="level-btn {% if level == 'مبتدئ' %}active{% endif %}">
                    <input type="radio" name="level" value="مبتدئ" {% if level == 'مبتدئ' %}checked{% endif %} onchange="updateActive(this)"> مبتدئ
                </label>
                <label class="level-btn {% if level == 'متوسط' %}active{% endif %}">
                    <input type="radio" name="level" value="متوسط" {% if level == 'متوسط' %}checked{% endif %} onchange="updateActive(this)"> متوسط
                </label>
                <label class="level-btn {% if level == 'محترف' %}active{% endif %}">
                    <input type="radio" name="level" value="محترف" {% if level == 'محترف' %}checked{% endif %} onchange="updateActive(this)"> محترف ⏱️
                </label>
            </div>
           
            <div class="slider-container">
                <div class="slider-header">
                    <span>عدد الأسئلة بالاختبار</span>
                    <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                </div>
                <input type="range" name="num_questions" min="5" max="15" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
           
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
       
        <a href="https://wa.me/201221581154?s=t" class="whatsapp-link-btn" target="_blank">💬 للاشتراك اضغط هنا</a>
    </div>
    <script>
        function updateActive(radio) {
            document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
            radio.closest('.level-btn').classList.add('active');
        }
    </script>
</body>
</html>
"""

QUIZ_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - حل الاختبار</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; border-right: 5px solid #114b3e; }
        .options-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
        .option-item { background: #f9f9f9; border: 1px solid #e0e0e0; padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 14px; }
        .option-item:hover { background: #e8f5e9; border-color: #114b3e; }
        .option-item input { margin-left: 10px; }
        .badge-type { display: inline-block; background: #e8f5e9; color: #114b3e; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
        .hint { color: #555; font-size: 13px; margin-top: 10px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        #timer-box { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 16px; display: none; }
        @media print {
            body { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="main-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
            <span style="font-size: 14px; color: #555;">السؤال: <strong style="color: #114b3e;">{{ current_num }} من {{ total_questions }}</strong></span>
        </div>

        <h2>اختبار الدرس الأول الشامل</h2>
       
        <form method="POST" action="{{ url_for('quiz_step') }}" id="quiz-form">
            <div class="question-box">
                <span class="badge-type">اختيار من متعدد</span>
                <p><strong>سؤال {{ current_num }}:</strong> {{ question.prompt }}</p>
               
                <div class="options-list">
                    {% for opt in question.options %}
                        <label class="option-item">
                            <input type="radio" name="current_answer" value="{{ opt }}" required> {{ opt }}
                        </label>
                    {% endfor %}
                </div>
                <div class="hint">💡 <em>{{ question.hint }}</em></div>
            </div>
           
            <button type="submit" class="start-btn">السؤال التالي ←</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نتيجة الامتحان - سر التفوق</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .score-box { background: #e8f5e9; border: 2px solid #2e7d32; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
        .score-num { font-size: 32px; font-weight: bold; color: #1b5e20; }
        .res-item { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; }
        .correct { border-right: 5px solid #2e7d32; }
        .wrong { border-right: 5px solid #c62828; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .wa-btn { background: #25d366; margin-top: 10px; display: block; text-align: center; }
        .wa-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <h2>نتيجة اختبارك</h2>
       
        <div class="score-box">
            <p style="margin: 0 0 5px 0; font-size: 16px; color: #333;">لقد أتممت الاختبار بنجاح!</p>
            <div class="score-num">{{ score }} / {{ total }}</div>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">المستوى: {{ level }}</p>
        </div>

        <h3>تفاصيل الإجابات:</h3>
        <div style="margin-top: 15px;">
            {% for r in results %}
                <div class="res-item {% if r.is_correct %}correct{% else %}wrong{% endif %}">
                    <p><strong>سؤال {{ r.id }}:</strong> {{ r.prompt }}</p>
                    <p style="margin: 5px 0; font-size: 14px;">إجابتك: <span style="font-weight: bold; color: {% if r.is_correct %}#2e7d32{% else %}#c62828{% endif %};">{{ r.user_ans }} {% if r.is_correct %}✅{% else %}❌{% endif %}</span></p>
                    {% if not r.is_correct %}
                        <p style="margin: 5px 0; font-size: 14px; color: #2e7d32;">الإجابة الصحيحة هي: <strong>{{ r.correct_ans }}</strong></p>
                    {% endif %}
                </div>
            {% endfor %}
        </div>

        <button type="button" class="start-btn print-btn" onclick="window.print()" style="background: #455a64; margin-top: 15px;">🖨️ طباعة النتيجة</button>
        <a href="/" class="start-btn" style="text-align: center; margin-top: 10px;">🔄 تصميم امتحان جديد</a>
        <a href="https://wa.me/201221581154?s=t" class="start-btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
