<p align="center">
  <img src="https://user-images.githubusercontent.com/7662492/229289746-89c5a4c7-afa6-4d46-a0e6-63dfdeb98285.jpg" style="width: 100%;"/>
</p>

<div align="right">

  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://tafrigh.ieasybooks.com)
  [![Formatter](https://github.com/ieasybooks/tafrigh/actions/workflows/formatter.yml/badge.svg)](https://github.com/ieasybooks/tafrigh/actions/workflows/formatter.yml)
  [![PyPI](https://img.shields.io/pypi/v/tafrigh?label=PyPI%20Version&color=limegreen)](https://pypi.org/project/tafrigh/)

</div>

<h1 dir="rtl">تفريغ</h1>

<p dir="rtl">تفريغ المواد المرئية أو المسموعة إلى نصوص.</p>

<p dir="rtl">يمكنك الاطلاع على أمثلة تم تفريغها باستخدام تفريغ من <a href="https://drive.google.com/drive/folders/1mwdJ9t4tiu8jFGosvNsq8SL54HoQMB8G?usp=sharing">هنا</a>.</p>

<h2 dir="rtl">مميزات تفريغ</h2>

<ul dir="rtl">
  <li>تفريغ المواد المرئي والمسموع إلى نصوص باستخدام أحدث تقنيات الذكاء الاصطناعي المقدمة من شركة OpenAI</li>
  <li>إمكانية تفريغ المواد باستخدام تقنيات wit.ai المقدمة من شركة Facebook</li>
  <li>تحميل المحتوى المرئي بشكل مباشر من منصة YouTube سواءً كان المستهدف مادة واحدة أو قائمة تشغيل كاملة</li>
  <li>توفير صيَغ مخرجات مختلفة كـ <code>txt</code> و <code>srt</code> و <code>vtt</code></li>
</ul>

<h2 dir="rtl">متطلبات الاستخدام</h2>

<ul dir="rtl">
  <li>يُفضّل وجود معالج رسوميات قوي في حاسبك في حال استخدام نماذج Whisper</li>
  <li>تثبيت لغة Python بإصدار 3.9 أو أعلى على حاسبك</li>
  <li>تثبيت برمجية <a href="https://ffmpeg.org">FFmpeg</a> على حاسبك</li>
  <li>تثبيت برمجية <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> على حاسبك</li>
</ul>

<h2 dir="rtl">تثبيت تفريغ</h2>

<h3 dir="rtl">من خلال الشيفرة المصدرية</h3>

<ul dir="rtl">
  <li>قم بتنزيل هذا المستودع من خلال الضغط على Code ثم Download ZIP أو من خلال تنفيذ الأمر التالي: <code>git clone git@github.com:ieasybooks/tafrigh.git</code></li>
  <li>قم بفك ضغط الملف إذا قمت بتنزيله بصيغة ZIP وتوجّه إلى مجلد المشروع</li>
  <li>قم بتنفيذ الأمر التالي لتثبيت تفريغ: <code dir="ltr">pip install .[wit,whisper]</code></li>
</ul>

<h3 dir="rtl">من خلال مستودع GitHub</h3>

<p dir="rtl">يمكن تثبيت تفريغ من خلال مستودع GitHub مباشرة عن طريق تنفيذ الأمر: <code dir="ltr">pip install "tafrigh[wit,whisper] @ git+https://github.com/ieasybooks/tafrigh"</code>.</p>

<p dir="rtl">يمكنك تحديد الاعتماديات التي تريد تثبيتها حسب نوع التقنية التي تريد استخدامها من خلال كتابة <code>wit</code> أو <code>whisper</code> بين قوسين مربعين كما هو موضّح في الأوامر السابقة.</p>

<h2 dir="rtl">استخدام تفريغ</h2>

<h3 dir="rtl">الخيارات المتوفرة</h3>

<ul dir="rtl">
  <li>
    المدخلات
    <ul dir="rtl">
      <li>الروابط أو مسارات الملفات: يجب تمرير الروابط أو مسارات الملفات للمواد المُراد تفريغها بعد اسم أداة تفريغ بشكل مباشر. على سبيل المثال: <code dir="ltr">tafrigh "https://yout..." "https://yout..." "C:\Users\ieasybooks\leactue.wav"</code></li>
      <li>تخطي عملية التفريغ في حال وجود المخرجات مسبقًا: يمكن تمرير الاختيار <code dir="ltr">--skip_if_output_exist</code> لتخطي عملية التفريغ إذا كانت المخرجات المطلوبة موجودة بالفعل في مجلد الإخراج المحدد</li>
      <li>المواد المُراد تفريفها من قائمة التشغيل: يمكن تحديد نطاق معين من المواد ليتم تفريغه من قائمة التشغيل من خلال الاختيار <code dir="ltr">--playlist_items</code> من خلال تمرير قيمة على صيغة <code dir="ltr">"[START]:[STOP][:STEP]"</code>. على سبيل المثال، عند تمرير <code dir="ltr">2:5</code> سيتم تحميل المواد من <code>2</code> إلى <code>5</code> من قائمة التشغيل. هذا الاختيار يُؤثّر على كل قوائم التشغيل التي يتم تمريرها كمدخلات لتفريغ</li>
    </ul>
  </li>

  <li>
    خيارات تقنية Whisper
    <ul dir="rtl">
      <li>
        النموذج: يمكنك تحديد النموذج من خلال الاختيار <code dir="ltr">--model_name_or_path</code>. النماذج المتوفرة:
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
          <li>اسم نموذج Whisper موجود على HuggingFace Hub</li>
          <li>مسار نموذج Whisper تم تحميلة مسبقًا</li>
          <li>مسار نموذج Whisper تم تحويله باستخدام أداة <a href="https://opennmt.net/CTranslate2/guides/transformers.html"><code>ct2-transformers-converter</code></a> لاستخدام المكتبة السريعة <a href="https://github.com/guillaumekln/faster-whisper"><code>faster-whisper</code></a></li>
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
      <li>استخدام نسخة أسرع من نماذج Whisper: من خلال تمرير الاختيار <code dir="ltr">--use_faster_whisper</code> سيتم استخدام النسخة الأسرع من نماذج Whisper</li>
      <li>إطار عمل JAX: يمكنك استخدام النموذج المكتوب باستخدام إطار عمل JAX من خلال تمرير الاختيار <code dir="ltr">--use_whisper_jax</code>، لكنك ستحتاج لتثبيت إطار عمل JAX يدويا على حاسبك من خلال اتباع الخطوات الموجودة <a href="https://github.com/google/jax#installation">هنا</a></li>
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
      <li>يمكنك تمرير الاختيار <code dir="ltr">--save_files_before_compact</code> لحفظ الملفات الأصلية قبل أن يتم دمج أجزائها بناء على اختيار <code dir="ltr">--min_words_per_segment</code></li>
      <li>يمكنك حفظ مخرجات مكتبة <code>yt-dlp</code> بصيغة <code>json</code> من خلال تمرير الاختيار <code dir="ltr">--save_yt_dlp_responses</code></li>
      <li>إخراج عينة من الأجزاء بعد الدمج: يمكنك تمرير قيمة للاختيار <code dir="ltr">--output_sample</code> للحصول على عينة عشوائية من جميع الأجزاء التي تم تفريغها من كل المواد بعد دمجها بناء على اختيار <code dir="ltr">--min_words_per_segment</code>. القيمة الافتراضية هي <code>0</code>، أي أنه لن يتم إخراج أي عينات</li>
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
      <li>مجلد المخرجات: يمكنك تحديد مجلد الاخراج من خلال الاختيار <code dir="ltr">--output_dir</code>. بشكل تلقائي سيكون المجلد الحالي هو مجلد الاخراج إذا لم يتم تحديده</li>
    </ul>
  </li>
</ul>

```
➜ tafrigh --help
usage: tafrigh [-h] [--skip_if_output_exist | --no-skip_if_output_exist] [--playlist_items PLAYLIST_ITEMS] [--verbose | --no-verbose] [-m MODEL_NAME_OR_PATH] [-t {transcribe,translate}]
               [-l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh}]
               [--use_faster_whisper | --no-use_faster_whisper] [--use_whisper_jax | --no-use_whisper_jax] [--beam_size BEAM_SIZE] [--ct2_compute_type {default,int8,int8_float16,int16,float16}]
               [-w WIT_CLIENT_ACCESS_TOKEN] [--max_cutting_duration [1-17]] [--min_words_per_segment MIN_WORDS_PER_SEGMENT] [--save_files_before_compact | --no-save_files_before_compact]
               [--save_yt_dlp_responses | --no-save_yt_dlp_responses] [--output_sample OUTPUT_SAMPLE] [-f {all,txt,srt,vtt,none} [{all,txt,srt,vtt,none} ...]] [-o OUTPUT_DIR]
               urls_or_paths [urls_or_paths ...]

options:
  -h, --help            show this help message and exit

Input:
  urls_or_paths         Video/Playlist URLs or local folder/file(s) to transcribe.
  --skip_if_output_exist, --no-skip_if_output_exist
                        Whether to skip generating the output if the output file already exists. (default: False)
  --playlist_items PLAYLIST_ITEMS
                        Comma separated playlist_index of the items to download. You can specify a range using "[START]:[STOP][:STEP]".
  --verbose, --no-verbose
                        Whether to print out the progress and debug messages. (default: False)

Whisper:
  -m MODEL_NAME_OR_PATH, --model_name_or_path MODEL_NAME_OR_PATH
                        Name or path of the Whisper model to use.
  -t {transcribe,translate}, --task {transcribe,translate}
                        Whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate').
  -l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh}, --language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh}
                        Language spoken in the audio, skip to perform language detection.
  --use_faster_whisper, --no-use_faster_whisper
                        Whether to use Faster Whisper implementation. (default: False)
  --use_whisper_jax, --no-use_whisper_jax
                        Whether to use Whisper JAX implementation. Make sure to have JAX installed before using this option. (default: False)
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
                        The minimum number of words should appear in each transcript segment. Any segment have words count less than this threshold will be merged with the next one. Pass 0 to disable this behavior.
  --save_files_before_compact, --no-save_files_before_compact
                        Saves the output files before applying the compact logic that is based on --min_words_per_segment. (default: False)
  --save_yt_dlp_responses, --no-save_yt_dlp_responses
                        Whether to save the yt-dlp library JSON responses or not. (default: False)
  --output_sample OUTPUT_SAMPLE
                        Samples random compacted segments from the output and generates a CSV file contains the sampled data. Pass 0 to disable this behavior.
  -f {all,txt,srt,vtt,none} [{all,txt,srt,vtt,none} ...], --output_formats {all,txt,srt,vtt,none} [{all,txt,srt,vtt,none} ...]
                        Format of the output file; if not specified, all available formats will be produced.
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to save the outputs.
```

<h3 dir="rtl">التفريغ باستخدام نماذج Whisper</h3>

<h4 dir="rtl">تفريغ مقطع واحد</h4>

```
tafrigh "https://youtu.be/dDzxYcEJbgo" \
  --model_name_or_path small \
  --task transcribe \
  --language ar \
  --output_dir . \
  --output_formats txt srt
```

<h4 dir="rtl">تفريغ قائمة تشغيل كاملة</h4>

```
tafrigh "https://youtube.com/playlist?list=PLyS-PHSxRDxsLnVsPrIwnsHMO5KgLz7T5" \
  --model_name_or_path small \
  --task transcribe \
  --language ar \
  --output_dir . \
  --output_formats txt srt
```

<h4 dir="rtl">تفريغ أكثر من مقطع</h4>

```
tafrigh "https://youtu.be/4h5P7jXvW98" "https://youtu.be/jpfndVSROpw" \
  --model_name_or_path small \
  --task transcribe \
  --language ar \
  --output_dir . \
  --output_formats txt srt
```

<h4 dir="rtl">تسريع عملية التفريغ</h4>

<p dir="rtl">يمكنك استخدام مكتبة <code><a href="https://github.com/guillaumekln/faster-whisper">faster_whisper</a></code> التي توفّر سرعة أكبر في تفريغ المواد من خلال تمرير الاختيار <code dir="ltr">--use_faster_whisper</code> كالتالي:</p>

```
tafrigh "https://youtu.be/3K5Jh_-UYeA" \
  --model_name_or_path large \
  --task transcribe \
  --language ar \
  --use_faster_whisper \
  --output_dir . \
  --output_formats txt srt
```

<h4 dir="rtl">تسريع عملية التفريغ أكثر (غير مختبر بشكل جيد)</h4>

<p dir="rtl">يمكنك استخدام مكتبة <code><a href="https://github.com/sanchit-gandhi/whisper-jax">whisper-jax</a></code> لتحصيل سرعة أكبر في تفريغ المواد من سرعة نماذج Whisper الأصلية من شركة OpenAI تصل إلى 70 ضعفًا، ولكن يجب أن يتم تثبيت إطار عمل JAX على حاسبك كما هو موضح <a href="https://github.com/google/jax#installation">هنا</a> لتتمكن من استخدام هذه المكتبة.</p>

<p dir="rtl">لاستخدام المكتبة، تحتاج فقط لتمرير الاختيار <code dir="ltr">--use_whisper_jax</code> إلى أمر التفريغ كالتالي:</p>

```
tafrigh "https://youtu.be/Di0vcmnxULs" \
  --model_name_or_path small \
  --task transcribe \
  --language ar \
  --use_whisper_jax \
  --output_dir . \
  --output_formats txt srt
```

<h3 dir="rtl">التفريغ باستخدام تقنية wit.ai</h3>

<h4 dir="rtl">تفريغ مقطع واحد</h4>

```
tafrigh "https://youtu.be/dDzxYcEJbgo" \
  --wit_client_access_token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --output_dir . \
  --output_formats txt srt \
  --min_words_per_segment 10 \
  --max_cutting_duration 10
```

<h4 dir="rtl">تفريغ قائمة تشغيل كاملة</h4>

```
tafrigh "https://youtube.com/playlist?list=PLyS-PHSxRDxsLnVsPrIwnsHMO5KgLz7T5" \
  --wit_client_access_token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --output_dir . \
  --output_formats txt srt \
  --min_words_per_segment 10 \
  --max_cutting_duration 10
```

<h4 dir="rtl">تفريغ أكثر من مقطع</h4>

```
tafrigh "https://youtu.be/4h5P7jXvW98" "https://youtu.be/jpfndVSROpw" \
  --wit_client_access_token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --output_dir . \
  --output_formats txt srt \
  --min_words_per_segment 10 \
  --max_cutting_duration 10
```

<hr>

<p dir="rtl">تم الاعتماد بشكل كبير على مستودع <a href="https://github.com/m1guelpf/yt-whisper">yt-whisper</a> لإنجاز تفريغ بشكل أسرع.</p>
