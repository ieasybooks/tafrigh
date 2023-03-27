<div dir="rtl">
  <a href="https://colab.research.google.com/github/ieasybooks/tafrigh/blob/main/colab_notebook.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="قم بتجربة تفريغ على Google Colab الآن"/></a>
</div>

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
    النموذج: يمكنك تحديد النموذج من خلال الاختيار <code dir="ltr">--model_name_or_ct2_model_path</code>. النماذج المتوفرة:
    <ul dir="rtl">
      <li><code dir="ltr">tiny.en</code> (لغة انجليزية فقط)</li>
      <li><code dir="ltr">tiny</code> (الأقل دقة)</li>
      <li><code dir="ltr">base.en</code> (لغة انجليزية فقط)</li>
      <li><code dir="ltr">base</code></li>
      <li><code dir="ltr">small.en</code> (لغة انجليزية فقط)</li>
      <li><code dir="ltr">small</code> <strong>(الاختيار الإفتراضي)</strong></li>
      <li><code dir="ltr">medium.en</code> (لغة انجليزية فقط)</li>
      <li><code dir="ltr">medium</code></li>
      <li><code dir="ltr">large-v1</code></li>
      <li><code dir="ltr">large-v2</code></li>
      <li><code dir="ltr">large</code> (الأعلى دقة)</li>
      <li>مسار نموذج تم تحويله باستخدام أداة <a href="https://opennmt.net/CTranslate2/guides/transformers.html"><code>ct2-transformers-converter</code></a> لاستخدام المكتبة السريعة <a href="https://github.com/guillaumekln/faster-whisper"><code>faster-whisper</code></a></li>
    </ul>
  </li>
  <li>
    المهمة: يمكنك تحديد المهمة من خلال الاختيار <code dir="ltr">--task</code>. المهمات المتوفرة:
    <ul dir="rtl">
      <li><code dir="ltr">transcribe</code>: تحويل الصوت إلى نص <strong>(الاختيار الإفتراضي)</strong></li>
      <li><code dir="ltr">translation</code>: ترجمة الصوت إلى نص باللغة الانجليزية</li>
    </ul>
  </li>
  <li>اللغة: يمكنك تحديد لغة الصوت من خلال الاختيار <code dir="ltr">--language</code>. على سبيل المثال، لتحديد اللغة العربية قم بتمرير <code dir="ltr">ar</code>. إذا لم يتم تحديد اللغة، سيتم التعرف عليها تلقائيا</li>
  <li>حجم نطاق البحث: يمكنك تحسين النتائج باستخدام اختيار <code>beam_size</code> والذي يسمح لك بإجبار النموذج على البحث في نطاق أوسع من الكلمات أثناء إنشاء النص. القيمة الإفتراضية هي <code>5</code></li>
  <li>
    طريقة ضغط النموذج: يمكنك تحديد الطريقة التي تم بها ضغط النموذج أثناء تحويله باستخدام أداة <a href="https://opennmt.net/CTranslate2/guides/transformers.html"><code>ct2-transformers-converter</code></a> من خلال تمرير الاختيار <code dir="ltr">--ct2_compute_type</code>. الطرق المتوفرة:
    <ul dir="rtl">
      <li><code dir="ltr">default</code> <strong>(الاختيار الإفتراضي)</strong></li>
      <li><code dir="ltr">int8</code></li>
      <li><code dir="ltr">int8_float16</code></li>
      <li><code dir="ltr">int16</code></li>
      <li><code dir="ltr">float16</code></li>
    </ul>
  </li>
  <li>ضغط الأجزاء: يمكنك استخدام الاختيار <code>min_words_per_segment</code> للتحكم في أقل عدد من الكلمات التي يمكن أن تكون داخل جزء واحد من أجزاء التفريغ. القيمة الإفتراضية هي <code>30</code>، يمكنك تمرير <code>0</code> لتعطيل هذه الخاصية</li>
  <li>
    صيغة المخرجات: يمكنك تحديد صيغة المخرجات من خلال الاختيار <code dir="ltr">--format</code>. الصيغ المتوفرة:
    <ul dir="rtl">
      <li><code dir="ltr">none</code> (لن يتم إنشاء ملف في حال تمرير هذه الصيغة)</li>
      <li><code dir="ltr">srt</code> <strong>(الاختيار الإفتراضي)</strong></li>
      <li><code dir="ltr">vtt</code></li>
    </ul>
  </li>
  <li>يمكنك حفظ نسخة نصية بصيغة <codde>txt</code> من خلال تمرير الاختيار <code dir="ltr">--output_txt_file</code></li>
  <li>يمكنك حفظ مخرجات مكتبة <code>yt-dlp</code> بصيغة <code>json</code> من خلال تمرير الاختيار <code dir="ltr">--save_yt_dlp_responses</code></li>
  <li>مجلد المخرجات: يمكنك تحديد مجلد الاخراج من خلال الاختيار <code dir="ltr">--output_dir</code>. بشكل تلقائي سيكون المجلد الحالي هو مجلد الاخراج إذا لم يتم تحديده</li>
</ul>

```bash
➜ tafrigh --help
usage: tafrigh [-h] [-m MODEL_NAME_OR_CT2_MODEL_PATH] [-t {transcribe,translate}]
               [-l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}]
               [--beam_size BEAM_SIZE] [--ct2_compute_type {default,int8,int8_float16,int16,float16}] [--min_words_per_segment MIN_WORDS_PER_SEGMENT] [-f {none,srt,vtt}][--output_txt_file | --no-output_txt_file] [--save_yt_dlp_responses | --no-save_yt_dlp_responses] [-o OUTPUT_DIR] [--verbose | --no-verbose]
               urls [urls ...]

positional arguments:
  urls                  Video/Playlist URLs to transcribe.

options:
  -h, --help            show this help message and exit
  -m MODEL_NAME_OR_CT2_MODEL_PATH, --model_name_or_ct2_model_path MODEL_NAME_OR_CT2_MODEL_PATH
                        Name of the Whisper model to use or a path to CTranslate2 model converted using `ct2-transformers-converter` tool.
  -t {transcribe,translate}, --task {transcribe,translate}
                        Whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate').
  -l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}, --language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}
                        Language spoken in the audio, skip to perform language detection.
  --beam_size BEAM_SIZE
                        Number of beams in beam search, only applicable when temperature is zero.
  --ct2_compute_type {default,int8,int8_float16,int16,float16}
                        Quantization type applied while converting the model to CTranslate2 format.
  --min_words_per_segment MIN_WORDS_PER_SEGMENT
                        The minimum number of words should appear in each transcript segment. Any segment have words count less than this threshold will be merged with the next one. Pass 0 to disable this behavior.
  -f {none,srt,vtt}, --format {none,srt,vtt}
                        Transcript format to output, pass none to skip writing transcripts.
  --output_txt_file, --no-output_txt_file
                        Whether to produce a text file or not. (default: True)
  --save_yt_dlp_responses, --no-save_yt_dlp_responses
                        Whether to save the yt-dlp library JSON responses or not. (default: False)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to save the outputs.
  --verbose, --no-verbose
                        Whether to print out the progress and debug messages. (default: False)
```

### تحويل مقطع واحد

```
tafrigh "https://youtu.be/dDzxYcEJbgo" \
    --model_name_or_ct2_model_path small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --format srt
```

### تحويل قائمة تشغيل كاملة

```
tafrigh "https://youtube.com/playlist?list=PLyS-PHSxRDxsLnVsPrIwnsHMO5KgLz7T5" \
    --model_name_or_ct2_model_path small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --format srt
```

### تحويل أكثر من مقطع

```
tafrigh "https://youtu.be/4h5P7jXvW98" "https://youtu.be/jpfndVSROpw" \
    --model_name_or_ct2_model_path small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --format srt
```

### تسريع عملية التفريغ

يمكنك استخدام مكتبة [`faster_whisper`](https://github.com/guillaumekln/faster-whisper) التي توفّر سرعة أكبر في تفريغ المواد من خلال تحويل النماذج المقدمة من شركة OpenAI باستخدام أداة [`ct2-transformers-converter`](https://opennmt.net/CTranslate2/guides/transformers.html) كالتالي:

```
ct2-transformers-converter --model openai/whisper-large-v2 --output_dir whisper-large-v2-ct2 --quantization float16 
```

ثم تمرير مسار مجلد النموذج المُحوّل إلى تفريغ كالتالي:

```
tafrigh "https://youtu.be/3K5Jh_-UYeA" \
    --model_name_or_ct2_model_path /path/to/whisper-large-v2-ct2 \
    --task transcribe \
    --language ar \
    --output_dir . \
    --format srt \
    --ct2_compute_type float16
```

------------------

تم الاعتماد بشكل كبير على مستودع [yt-whisper](https://github.com/m1guelpf/yt-whisper) لإنجاز تفريغ بشكل أسرع.
