<p align="center">
  <img src="https://user-images.githubusercontent.com/7662492/229289746-89c5a4c7-afa6-4d46-a0e6-63dfdeb98285.jpg" style="width: 100%;"/>
</p>

<div dir="rtl">
  <a href="https://colab.research.google.com/github/ieasybooks/tafrigh/blob/main/colab_notebook.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="قم بتجربة تفريغ على Google Colab الآن"/></a>
</div>

# تفريغ

تفريغ المواد المرئية أو المسموعة إلى نصوص.

يمكنك الاطلاع على أمثلة تم تفريغها باستخدام تفريغ من [هنا](https://drive.google.com/drive/folders/1mwdJ9t4tiu8jFGosvNsq8SL54HoQMB8G?usp=sharing).

## مميزات تفريغ

<ul dir="rtl">
  <li>تفريغ المواد المرئي والمسموع إلى نصوص باستخدام أحدث تقنيات الذكاء الاصطناعي المقدمة من شركة OpenAI</li>
  <li>إمكانية تفريغ المواد باستخدام تقنيات wit.ai المقدمة من شركة Facebook</li>
  <li>تحميل المحتوى المرئي بشكل مباشر من منصة YouTube سواءً كان المستهدف مادة واحدة أو قائمة تشغيل كاملة</li>
  <li>توفير صيَغ مخرجات مختلفة كـ `txt` و `srt` و `vtt`</li>
</ul>

## متطلبات الاستخدام

<ul dir="rtl">
  <li>يُفضّل وجود معالج رسوميات قوي في حاسبك</li>
  <li>تثبيت لغة Python بإصدار 3.9 أو أعلى على حاسبك</li>
  <li>تثبيت برمجية [FFmpeg](https://ffmpeg.org) على حاسبك</li>
  <li>تثبيت برمجية [yt-dlp](https://github.com/yt-dlp/yt-dlp) على حاسبك</li>
</ul>

## تثبيت تفريغ

<ul dir="rtl">
  <li>قم بتنزيل هذا المستودع من خلال الضغط على Code ثم Download ZIP أو من خلال تنفيذ الأمر التالي: <code>git clone git@github.com:ieasybooks/tafrigh.git</code></li>
  <li>قم بفك ضغط الملف إذا قمت بتنزيله بصيغة ZIP وتوجّه إلى مجلد المشروع</li>
  <li>قم بتنفيذ الأمر التالي لتثبيت تفريغ: <code dir="ltr">pip install .</code></li>
</ul>

## استخدام تفريغ

### الخيارات المتوفرة

<ul dir="rtl">
  <li>
    المدخلات
    <ul dir="rtl">
      <li>الروابط: يجب تمرير الروابط للمواد المُراد تفريغها بعد اسم أداة تفريغ بشكل مباشر. على سبيل المثال: <code dir="ltr">tafrigh "https://yout..." "https://yout..."</code></li>
    </ul>
  </li>

  <li>
    خيارات تقنية Whisper
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
      <li>حجم نطاق البحث: يمكنك تحسين النتائج باستخدام اختيار <code dir="ltr">--beam_size</code> والذي يسمح لك بإجبار النموذج على البحث في نطاق أوسع من الكلمات أثناء إنشاء النص. القيمة الإفتراضية هي <code>5</code></li>
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
    </ul>
  </li>

  <li>
    خيارات تقنية Wit
    <ul dir="rtl">
      <li>مفتاح <a href="wit.ai">wit.ai</a>: يمكنك استخدام تقنيات <a href="wit.ai">wit.ai</a> لتفريغ المواد إلى نصوص من خلال تمرير المفتاح الخاص بك للاختيار <code dir="ltr">--wit_client_access_token</code>. إذا تم تمرير هذا الاختيار، سيتم استخدام <a href="wit.ai">wit.ai</a> لتفريغ المواد إلى نصوص. غير ذلك، سيتم استخدام نماذج Whisper</li>
      <li>تحديد أقصى مدة للتقطيع: يمكنك تحديد أقصى مدة للتقطيع والتي ستؤثر على طول الجمل في ملفات SRT و VTT من خلال تمرير الاختيار <code dir="ltr">--max_cutting_duration</code>. القيمة الافتراضية هي <code>15</code></li>
    </ul>
  </li>

  <li>
    المخرجات
    <ul dir="rtl">
      <li>ضغط الأجزاء: يمكنك استخدام الاختيار <code dir="ltr">--min_words_per_segment</code> للتحكم في أقل عدد من الكلمات التي يمكن أن تكون داخل جزء واحد من أجزاء التفريغ. القيمة الإفتراضية هي <code>1</code>، يمكنك تمرير <code>0</code> لتعطيل هذه الخاصية</li>
      <li>
        صيغة المخرجات: يمكنك تحديد صيغة المخرجات من خلال الاختيار <code dir="ltr">--output_formats</code>. الصيغ المتوفرة:
        <ul dir="rtl">
          <li><code dir="ltr">txt</code></li>
          <li><code dir="ltr">srt</code></li>
          <li><code dir="ltr">vtt</code></li>
          <li><code dir="ltr">all</code> <strong>(الاختيار الإفتراضي)</strong></li>
          <li><code dir="ltr">none</code> (لن يتم إنشاء ملف في حال تمرير هذه الصيغة)</li>
        </ul>
      </li>
      <li>يمكنك حفظ مخرجات مكتبة <code>yt-dlp</code> بصيغة <code>json</code> من خلال تمرير الاختيار <code dir="ltr">--save_yt_dlp_responses</code></li>
      <li>مجلد المخرجات: يمكنك تحديد مجلد الاخراج من خلال الاختيار <code dir="ltr">--output_dir</code>. بشكل تلقائي سيكون المجلد الحالي هو مجلد الاخراج إذا لم يتم تحديده</li>
    </ul>
  </li>
</ul>

```bash
➜ tafrigh --help
usage: tafrigh [-h] [--verbose | --no-verbose] [-m MODEL_NAME_OR_CT2_MODEL_PATH] [-t {transcribe,translate}]
               [-l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}]
               [--beam_size BEAM_SIZE] [--ct2_compute_type {default,int8,int8_float16,int16,float16}] [-w WIT_CLIENT_ACCESS_TOKEN] [--max_cutting_duration [1-17]] [--min_words_per_segment MIN_WORDS_PER_SEGMENT] [-f {all,txt,srt,vtt,none} [{all,txt,srt,vtt,none} ...]] [--save_yt_dlp_responses | --no-save_yt_dlp_responses] [-o OUTPUT_DIR]
               urls [urls ...]

options:
  -h, --help            show this help message and exit

Input:
  urls                  Video/Playlist URLs to transcribe.
  --verbose, --no-verbose
                        Whether to print out the progress and debug messages. (default: False)

Whisper:
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

Wit:
  -w WIT_CLIENT_ACCESS_TOKEN, --wit_client_access_token WIT_CLIENT_ACCESS_TOKEN
                        wit.ai client access token. If provided, wit.ai APIs will be used to do the transcription, otherwise whisper will be used.
  --max_cutting_duration [1-17]
                        The maximum allowed cutting duration. It should be between 1 and 17.

Output:
  --min_words_per_segment MIN_WORDS_PER_SEGMENT
                        The minimum number of words should appear in each transcript segment. Any segment have words count less than this threshold will be merged with the next one. Pass 0 to disable this
                        behavior.
  -f {all,txt,srt,vtt,none} [{all,txt,srt,vtt,none} ...], --output_formats {all,txt,srt,vtt,none} [{all,txt,srt,vtt,none} ...]
                        Format of the output file; if not specified, all available formats will be produced.
  --save_yt_dlp_responses, --no-save_yt_dlp_responses
                        Whether to save the yt-dlp library JSON responses or not. (default: False)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to save the outputs.
```

### التفريغ باستخدام نماذج Whisper

#### تفريغ مقطع واحد

```
tafrigh "https://youtu.be/dDzxYcEJbgo" \
    --model_name_or_ct2_model_path small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --output_formats txt srt
```

#### تفريغ قائمة تشغيل كاملة

```
tafrigh "https://youtube.com/playlist?list=PLyS-PHSxRDxsLnVsPrIwnsHMO5KgLz7T5" \
    --model_name_or_ct2_model_path small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --output_formats txt srt
```

#### تفريغ أكثر من مقطع

```
tafrigh "https://youtu.be/4h5P7jXvW98" "https://youtu.be/jpfndVSROpw" \
    --model_name_or_ct2_model_path small \
    --task transcribe \
    --language ar \
    --output_dir . \
    --output_formats txt srt
```

#### تسريع عملية التفريغ

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
    --output_formats txt srt \
    --ct2_compute_type float16
```

### التفريغ باستخدام تقنية wit.ai

#### تفريغ مقطع واحد

```
tafrigh "https://youtu.be/dDzxYcEJbgo" \
    --wit_client_access_token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
    --output_dir . \
    --output_formats txt srt \
    --min_words_per_segment 10 \
    --max_cutting_duration 10
```

#### تفريغ قائمة تشغيل كاملة

```
tafrigh "https://youtube.com/playlist?list=PLyS-PHSxRDxsLnVsPrIwnsHMO5KgLz7T5" \
    --wit_client_access_token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
    --output_dir . \
    --output_formats txt srt \
    --min_words_per_segment 10 \
    --max_cutting_duration 10
```

#### تفريغ أكثر من مقطع

```
tafrigh "https://youtu.be/4h5P7jXvW98" "https://youtu.be/jpfndVSROpw" \
    --wit_client_access_token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
    --output_dir . \
    --output_formats txt srt \
    --min_words_per_segment 10 \
    --max_cutting_duration 10
```

------------------

تم الاعتماد بشكل كبير على مستودع [yt-whisper](https://github.com/m1guelpf/yt-whisper) لإنجاز تفريغ بشكل أسرع.
