# تفريغ

تحويل المواد المرئية أو المسموعة إلى نصوص

## مميزات تفريغ

- تحويل المواد المرئي والمسموع إلى نصوص باستخدام أحدث تقنيات الذكاء الاصطناعي المقدمة من شركة OpenAI
- تحميل المحتوى المرئي بشكل مباشر من منصة YouTube سواءً كان المستهدف مادة واحدة أو قائمة تشغيل كاملة
- توفير صيَغ مخرجات مختلفة كـ txt، srt، و vtt

## متطلبات الاستخدام

- يُفضّل وجود معالج رسوميات قوي في حاسبك
- تثبيت لغة Python بإصدار 3.9 أو أعلى على حاسبك
- تثبيت برمجية [FFmpeg](https://ffmpeg.org) على حاسبك
- تثبيت برمجية [yt-dlp](https://github.com/yt-dlp/yt-dlp) على حاسبك

## تثبيت تفريغ

- قم بتنزيل هذا المستودع من خلال الضغط على Code ثم Download ZIP أو من خلال تنفيذ الأمر التالي: `git clone git@github.com:ieasybooks/tafrigh.git`
- قم بفك ضغط الملف إذا قمت بتنزيله بصيغة ZIP وتوجّه إلى مجلد المشروع
- قم بتنفيذ الأمر التالي لتثبيت تفريغ: `pip install .`

## استخدام تفريغ

### الخيارات المتوفرة

- النموذج: يمكنك تحديد النموذج من خلال الاختيار `--model`. النماذج المتوفرة:
  - `tiny.en` (لغة انجليزية فقط)
  - `tiny` (الأقل دقة)
  - `base.en` (لغة انجليزية فقط)
  - `base`
  - `small.en` (لغة انجليزية فقط)
  - `small` **(الاختيار التلقائي)**
  - `medium.en` (لغة انجليزية فقط)
  - `medium`
  - `large-v1`
  - `large-v2`
  - `large` (الأعلى دقة)
- المهمة: يمكنك تحديد المهمة من خلال الاختيار `--task`. المهمات المتوفرة:
  - `transcribe`: تحويل الصوت إلى نص **(الاختيار التلقائي)**
  - `translation`: ترجمة الصوت إلى نص باللغة الانجليزية
- اللغة: يمكنك تحديد لغة الصوت من خلال الاختيار `--language`. على سبيل المثال، لتحديد اللغة العربية قم بتمرير `ar`. إذا لم يتم تحديد اللغة، سيتمر التعرف عليها تلقائيا
- صيغة المخرجات: يمكنك تحديد صيغة المخرجات من خلال الاختيار `--format`. الصيغ المتوفرة:
  - `srt` **(الاختيار التلقائي)**
  - `vtt`
- مجلد المخرجات: يمكنك تحديد مجلد الاخراج من خلال الاختيار `--output_dir`. بشكل تلقائي سيكون المجلد الحالي هو مجلد الاخراج إذا لم يتم تحديده

```bash
➜ tafrigh --help
usage: tafrigh [-h] [-m {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}] [-t {transcribe,translate}]
               [-l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}]
               [-o OUTPUT_DIR] [-f {srt,vtt}] [--verbose | --no-verbose]
               urls [urls ...]

positional arguments:
  urls                  Video/Playlist URLs to transcribe.

options:
  -h, --help            show this help message and exit
  -m {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}, --model {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}
                        Name of the Whisper model to use.
  -t {transcribe,translate}, --task {transcribe,translate}
                        Whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate')
  -l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}, --language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}
                        Language spoken in the audio, skip to perform language detection
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to save the outputs.
  -f {srt,vtt}, --format {srt,vtt}
                        Subtitle format to output.
  --verbose, --no-verbose
                        Whether to print out the progress and debug messages (default: False)
```

### تحويل مقطع واحد

```
tafrigh "https://youtu.be/dDzxYcEJbgo" \
    --model small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --format srt
```

### تحويل قائمة تشغيل كاملة

```
tafrigh "https://youtube.com/playlist?list=PLyS-PHSxRDxsLnVsPrIwnsHMO5KgLz7T5" \
    --model small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --format srt
```

### تحويل أكثر من مقطع

```
tafrigh "https://youtu.be/4h5P7jXvW98" "https://youtu.be/jpfndVSROpw" \
    --model small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --format srt
```
