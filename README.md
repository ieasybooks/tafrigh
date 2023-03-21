# تفريغ

تحويل المواد المرئية أو المسموعة إلى نصوص

## مميزات تفريغ

- تحويل المواد المرئي والمسموع إلى نصوص باستخدام أحدث تقنيات الذكاء الاصطناعي المقدمة من شركة OpenAI
- تحميل المحتوى المرئي بشكل مباشر من منصة YouTube سواءً كان المستهدف مادة واحدة أو قائمة تشغيل كاملة
- توفير صيَغ مخرجات مختلفة كـ `txt` و `srt` و `vtt`

## متطلبات الاستخدام

- يُفضّل وجود معالج رسوميات قوي في حاسبك
- تثبيت لغة Python بإصدار 3.9 أو أعلى على حاسبك
- تثبيت برمجية [FFmpeg](https://ffmpeg.org) على حاسبك
- تثبيت برمجية [yt-dlp](https://github.com/yt-dlp/yt-dlp) على حاسبك

## تثبيت تفريغ

- قم بتنزيل هذا المستودع من خلال الضغط على Code ثم Download ZIP أو من خلال تنفيذ الأمر التالي: `git clone git@github.com:ieasybooks/tafrigh.git`
- قم بفك ضغط الملف إذا قمت بتنزيله بصيغة ZIP وتوجّه إلى مجلد المشروع
- قم بتنفيذ الأمر التالي لتثبيت تفريغ: <code dir="ltr">pip install .</code>

## استخدام تفريغ

### الخيارات المتوفرة

<ul dir="rtl">
  <li>
    النموذج: يمكنك تحديد النموذج من خلال الاختيار <code dir="ltr">--model</code>. النماذج المتوفرة:
    <ul dir="rtl">
      <li><code dir="ltr">tiny.en</code> (لغة انجليزية فقط)</li>
      <li><code dir="ltr">tiny</code> (الأقل دقة)</li>
      <li><code dir="ltr">base.en</code> (لغة انجليزية فقط)</li>
      <li><code dir="ltr">base</code></li>
      <li><code dir="ltr">small.en</code> (لغة انجليزية فقط)</li>
      <li><code dir="ltr">small</code> <strong>(الاختيار التلقائي)</strong></li>
      <li><code dir="ltr">medium.en</code> (لغة انجليزية فقط)</li>
      <li><code dir="ltr">medium</code></li>
      <li><code dir="ltr">large-v1</code></li>
      <li><code dir="ltr">large-v2</code></li>
      <li><code dir="ltr">large</code> (الأعلى دقة)</li>
    </ul>
  </li>
  <li>
    المهمة: يمكنك تحديد المهمة من خلال الاختيار <code dir="ltr">--task</code>. المهمات المتوفرة:
    <ul dir="rtl">
      <li><code dir="ltr">transcribe</code>: تحويل الصوت إلى نص <strong>(الاختيار التلقائي)</strong></li>
      <li><code dir="ltr">translation</code>: ترجمة الصوت إلى نص باللغة الانجليزية</li>
    </ul>
  </li>
  <li>اللغة: يمكنك تحديد لغة الصوت من خلال الاختيار <code dir="ltr">--language</code>. على سبيل المثال، لتحديد اللغة العربية قم بتمرير <code dir="ltr">ar</code>. إذا لم يتم تحديد اللغة، سيتمر التعرف عليها تلقائيا</li>
  <li>
    صيغة المخرجات: يمكنك تحديد صيغة المخرجات من خلال الاختيار <code dir="ltr">--format</code>. الصيغ المتوفرة:
    <ul dir="rtl">
      <li><code dir="ltr">none</code> (لن يتم إنشاء ملف في حال تمرير هذه الصيغة)</li>
      <li><code dir="ltr">srt</code> <strong>(الاختيار التلقائي)</strong></li>
      <li><code dir="ltr">vtt</code></li>
    </ul>
  </li>
  <li>مجلد المخرجات: يمكنك تحديد مجلد الاخراج من خلال الاختيار <code dir="ltr">--output_dir</code>. بشكل تلقائي سيكون المجلد الحالي هو مجلد الاخراج إذا لم يتم تحديده</li>
  <li>حفظ مخرجات مكتبة <code>yt-dlp</code> بصيغة <code>json</code> من خلال تمرير الاختيار <code dir="ltr">--save_yt_dlp_responses</code></li>
</ul>

```bash
➜ tafrigh --help
usage: tafrigh [-h] [-m {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}] [-t {transcribe,translate}]
               [-l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}]
               [-o OUTPUT_DIR] [-f {none,srt,vtt}] [--save_yt_dlp_responses | --no-save_yt_dlp_responses] [--verbose | --no-verbose]
               urls [urls ...]

positional arguments:
  urls                  Video/Playlist URLs to transcribe.

options:
  -h, --help            show this help message and exit
  -m {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}, --model {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}
                        Name of the Whisper model to use.
  -t {transcribe,translate}, --task {transcribe,translate}
                        Whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate').
  -l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}, --language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}
                        Language spoken in the audio, skip to perform language detection.
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to save the outputs.
  -f {none,srt,vtt}, --format {none,srt,vtt}
                        Transcript format to output, pass none to skip writing transcripts.
  --save_yt_dlp_responses, --no-save_yt_dlp_responses
                        Whether to save the yt-dlp library JSON responses or not. (default: False)
  --verbose, --no-verbose
                        Whether to print out the progress and debug messages. (default: False)
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

------------------

تم الاعتماد بشكل كبير على مستودع [yt-whisper](https://github.com/m1guelpf/yt-whisper) لإنجاز تفريغ بشكل أسرع.
