# Gold Trader skill — سكيلات الذهب XAUUSD

9 سكيلات ديال Claude خاصين بالذهب. كيعطيوك **الفوندامونتال والحسابات**،
وما كيتدخلوش فالاستراتيجية ديالك، وما كيديرو حتى صفقة.

9 Claude skills for gold (XAUUSD) traders: fundamentals, context and risk
arithmetic. They never touch your strategy and never place an order.
Standard-library Python 3.9+, nothing to install, no API key.

| السكيل | شنو كيدير |
| --- | --- |
| `/gold-brief` | **الخلاصة ديال النهار**: الأخبار، الدولار والعوائد، الكبار، العناوين المهمة. جاهزة للواتساب |
| `/gold-econ` | الأجندة الاقتصادية (FOMC، CPI، NFP…) بساعتك، مع التأثير المعتاد على الذهب ووقت البعد من السوق |
| `/gold-news` | آخر الأخبار اللي كتحرك الذهب، مصنفة حسب الموضوع، وغير الجديد منها |
| `/gold-macro` | الدولار DXY، العائد 10 سنين، العائد الحقيقي، VIX، الفضة: داعم ولا ضاغط على الذهب |
| `/gold-cot` | تقرير CFTC: شحال شاريين الصناديق الكبار فالذهب، وواش المراكز مزدحمة |
| `/gold-size` | حساب اللوت حسب الرصيد ونسبة المخاطرة والستوب ديالك |
| `/gold-risk` | فحص قبل الصفقة: المخاطرة، R:R، عدد الصفقات، الخسارة اليومية، الأخبار، السبريد |
| `/gold-journal` | يوميات التداول والإحصائيات: نسبة الربح، PF، أطول سلسلة خسائر، حسب الجلسة |
| `/gold-sessions` | واش السوق مفتوح، وشمن جلسة دابا، والأوقات بساعتك |

## التثبيت — Install

**Claude Code (plugin):**

```
/plugin marketplace add rayanhalfa8-oss/GAFSTUDIO
/plugin install gold-trader-skill@gold-trader-skill
```

They then show up as `/gold-trader-skill:gold-brief` etc.

**Or copy the folders** (plain `/gold-brief`):

```bash
git clone https://github.com/rayanhalfa8-oss/GAFSTUDIO.git
cp -r GAFSTUDIO/gold-trader-skill/skills/gold-* ~/.claude/skills/
```

Keep all nine in the same parent folder: `/gold-brief` runs the others.

## أول مرة — First run

1. نسخ `skills/gold-brief/config.example.json` ل `gold/config.json` فالمجلد
   اللي خدام فيه، وبدل: الساعة ديالك (`timezone`)، الرصيد، نسبة المخاطرة،
   والحدود ديالك. أو غير قول ل Claude: "عمر ليا config ديال الذهب".
2. قول ل Claude: **"عطيني الخلاصة ديال الذهب اليوم"**.

## كيفاش كيتربطو — How they connect

```
gold-econ ──> gold/calendar.json ──┐
gold-journal ─> gold/journal.csv ──┼──> gold-risk  (PASS / WARN / BLOCK)
gold-size  (lots) ─────────────────┘
gold-sessions + gold-econ + gold-macro + gold-cot + gold-news ──> gold-brief
```

## Data sources

| tool | source | note |
| --- | --- | --- |
| econ | Forex Factory weekly JSON (nfs.faireconomy.media) | cached 1 h |
| news | Google News RSS | headlines only |
| macro | Yahoo Finance chart endpoint, FRED (DFII10) | Yahoo's endpoint is unofficial and can change; GC=F is futures, a few $ above spot |
| cot | CFTC public reporting API, gold 088691 | positions of Tuesday, out Friday |

The parsers are tested offline on sample files in `tests/fixtures`. If a
site changes its format, the tool says what is missing instead of guessing.

```bash
python3 -m unittest discover -s tests -v
```

## مهم — Fine print

- **ماشي نصيحة مالية.** هادي معلومات وحسابات. السوق ما كيتضمنش، وتقدر تخسر.
- **حتى استراتيجية ما كتربحش 100%.** `/gold-journal` كيقيس الاستراتيجية ديالك بالأرقام من بعد 30–50 صفقة.
- **الواتساب:** Claude ما يقدرش يصيفط رسائل. `/gold-brief` كيعطيك الخلاصة فبلوك واحد، تنسخو وتصيفطو.
- "PASS" فـ `/gold-risk` معناه الصفقة كتحترم الحدود ديالك، ماشي أن الصفقة مزيانة.
