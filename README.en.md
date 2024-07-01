<p align="center">
  <img src="https://user-images.githubusercontent.com/7662492/229289746-89c5a4c7-afa6-4d46-a0e6-63dfdeb98285.jpg" style="width: 100%;"/>
</p>

<div align="center">
  <a href="https://pypi.org/project/tafrigh" target="_blank"><img src="https://img.shields.io/pypi/v/tafrigh?label=PyPI%20Version&color=limegreen" /></a>
  <a href="https://pypi.org/project/tafrigh" target="_blank"><img src="https://img.shields.io/pypi/pyversions/tafrigh?color=limegreen" /></a>
  <a href="https://github.com/ieasybooks/tafrigh/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/pypi/l/tafrigh?color=limegreen" /></a>
  <a href="https://pepy.tech/project/tafrigh" target="_blank"><img src="https://static.pepy.tech/badge/tafrigh" /></a>

  <a href="https://github.com/ieasybooks/tafrigh/actions/workflows/formatter.yml" target="_blank"><img src="https://github.com/ieasybooks/tafrigh/actions/workflows/formatter.yml/badge.svg" /></a>
  <a href="https://sonarcloud.io/summary/new_code?id=ieasybooks_tafrigh" target="_blank"><img src="https://sonarcloud.io/api/project_badges/measure?project=ieasybooks_tafrigh&metric=code_smells" /></a>
  <a href="https://tafrigh.ieasybooks.com" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" /></a>
</div>

<div align="center">

  [![ar](https://img.shields.io/badge/lang-ar-brightgreen.svg)](README.md)
  [![en](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)

</div>

<h1>Tafrigh</h1>

<p>Transcribing visual or audio materials into text.</p>

<p>You can view examples transcribed using Tafrigh from <a href="https://drive.google.com/drive/folders/1mwdJ9t4tiu8jFGosvNsq8SL54HoQMB8G?usp=sharing">here</a>.</p>

<h2>Features of Tafrigh</h2>

<ul>
  <li>Transcribing visual and audio materials into text using the latest AI technologies provided by OpenAI</li>
  <li>Ability to transcribe materials using wit.ai technologies provided by Facebook</li>
  <li>Download materials directly from YouTube, Facebook, Twitter, SoundCloud, and <a href="https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md">other sites</a></li>
  <li>Download visual content directly from YouTube, whether a single video or a complete playlist</li>
  <li>Provide various output formats like <code>txt</code>, <code>srt</code>, <code>vtt</code>, <code>csv</code>, <code>tsv</code>, and <code>json</code></li>
</ul>

<h2>Requirements</h2>

<ul>
  <li>A strong GPU in your computer is recommended if using Whisper models</li>
  <li>Python version 3.10 or higher installed on your computer</li>
  <li><a href="https://ffmpeg.org">FFmpeg</a> installed on your computer</li>
  <li><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> installed on your computer</li>
</ul>

<h2>Installing Tafrigh</h2>

<h3>Using <code>pip</code></h3>

<p>You can install Tafrigh using <code>pip</code> with the command: <code>pip install tafrigh[wit,whisper]</code></p>

<p>You can specify the dependencies you want to install based on the technology you want to use by writing <code>wit</code> or <code>whisper</code> in square brackets as shown in the previous command.</p>

<h3>From the Source Code</h3>

<ul>
  <li>Download this repository by clicking on Code then Download ZIP or by executing the following command: <code>git clone git@github.com:ieasybooks/tafrigh.git</code></li>
  <li>Extract the file if downloaded as ZIP and navigate to the project folder</li>
  <li>Execute the following command to install Tafrigh: <code>poetry install</code></li>
</ul>

<p>Add <code>-E wit</code> or <code>-E whisper</code> to specify the dependencies to install.</p>

<h2>Using Tafrigh</h2>

<h3>Available Options</h3>

<ul>
  <li>
    Inputs
    <ul>
      <li>Links or file paths: Pass the links or file paths of the materials to be transcribed directly after the Tafrigh tool name. For example: <code>tafrigh "https://yout..." "https://yout..." "C:\Users\ieasybooks\leactue.wav"</code></li>
      <li>Skip transcription if output exists: Use the <code>--skip_if_output_exist</code> option to skip transcription if the required outputs already exist in the specified output folder</li>
      <li>Specify items to transcribe from a playlist: You can specify a range of items to be transcribed from a playlist using the <code>--playlist_items</code> option by passing a value in the format <code>"[START]:[STOP][:STEP]"</code>. For example, passing <code>2:5</code> will download items from <code>2</code> to <code>5</code> from the playlist. This option affects all playlists passed as inputs to Tafrigh</li>
      <li>Number of download retries: If downloading a full playlist using the <code>yt-dlp</code> library, some items may fail to download. The <code>--download_retries</code> option can be used to specify the number of retry attempts if a download fails. The default value is <code>3</code></li>
    </ul>
  </li>

  <li>
    Whisper Options
    <ul>
      <li>
        Model: You can specify the model using the <code>--model_name_or_path</code> option. Available models:
        <ul>
          <li><code>tiny.en</code> (English only)</li>
          <li><code>tiny</code> (least accurate)</li>
          <li><code>base.en</code> (English only)</li>
          <li><code>base</code></li>
          <li><code>small.en</code> (English only)</li>
          <li><code>small</code> <strong>(default)</strong></li>
          <li><code>medium.en</code> (English only)</li>
          <li><code>medium</code></li>
          <li><code>large-v1</code></li>
          <li><code>large-v2</code></li>
          <li><code>large-v3</code></li>
          <li><code>large</code> (most accurate)</li>
          <li>Whisper model name on HuggingFace Hub</li>
          <li>Path to a pre-downloaded Whisper model</li>
          <li>Path to a Whisper model converted using the <a href="https://opennmt.net/CTranslate2/guides/transformers.html"><code>ct2-transformers-converter</code></a> tool for use with the fast library <a href="https://github.com/guillaumekln/faster-whisper"><code>faster-whisper</code></a></li>
        </ul>
      </li>
      <li>
        Task: You can specify the task using the <code>--task</code> option. Available tasks:
        <ul>
          <li><code>transcribe</code>: Convert speech to text <strong>(default)</strong></li>
          <li><code>translation</code>: Translate speech to text in English</li>
        </ul>
      </li>
      <li>Language: You can specify the audio language using the <code>--language</code> option. For example, to specify Arabic, pass <code>ar</code>. If not specified, the language will be detected automatically</li>
      <li>Use faster version of Whisper models: By passing the <code>--use_faster_whisper</code> option, the faster version of Whisper models will be used</li>
      <li>Beam size: You can improve results using the <code>--beam_size</code> option, which allows the model to search a wider range of words during text generation. The default value is <code>5</code></li>
      <li>
        Model compression type: You can specify the compression method used during the model conversion using the <code>ct2-transformers-converter</code> tool by passing the <code>--ct2_compute_type</code> option. Available methods:
        <ul>
          <li><code>default</code> <strong>(default)</strong></li>
          <li><code>int8</code></li>
          <li><code>int8_float16</code></li>
          <li><code>int16</code></li>
          <li><code>float16</code></li>
        </ul>
      </li>
    </ul>
  </li>

  <li>
    Wit Options
    <ul>
      <li>Wit.ai keys: You can use <a href="wit.ai">wit.ai</a> technologies to transcribe materials into text by passing your wit.ai client access tokens to the <code>--wit_client_access_tokens</code> option. If this option is passed, wit.ai will be used for transcription. Otherwise, Whisper models will be used</li>
      <li>Maximum cutting duration: You can specify the maximum cutting duration, which will affect the length of sentences in SRT and VTT files, by passing the <code>--max_cutting_duration</code> option. The default value is <code>15</code></li>
    </ul>
  </li>

  <li>
    Outputs
    <ul>
      <li>Merge segments: You can use the <code>--min_words_per_segment</code> option to control the minimum number of words that can be in a single transcription segment. The default value is <code>1</code>. Pass <code>0</code> to disable this feature</li>
      <li>Save original files before merging: Use the <code>--save_files_before_compact</code> option to save the original files before merging segments based on the <code>--min_words_per_segment</code> option</li>
      <li>Save yt-dlp library responses: You can save the yt-dlp library responses in JSON format by passing the <code>--save_yt_dlp_responses</code> option</li>
      <li>Output sample segments: You can pass a value to the <code>--output_sample</code> option to get a random sample of all transcribed segments from each material after merging based on the <code>--min_words_per_segment</code> option. The default value is <code>0</code>, meaning no samples will be output</li>
      <li>
        Output formats: You can specify the output formats using the <code>--output_formats</code> option. Available formats:
        <ul>
          <li><code>txt</code></li>
          <li><code>srt</code></li>
          <li><code>vtt</code></li>
          <li><code>csv</code></li>
          <li><code>tsv</code></li>
          <li><code>json</code></li>
          <li><code>all</code> <strong>(default)</strong></li>
          <li><code>none</code> (No file will be created if this format is passed)</li>
        </ul>
      </li>
      <li>Output folder: You can specify the output folder using the <code>--output_dir</code> option. By default, the current folder will be the output folder if not specified</li>
    </ul>
  </li>
</ul>

```
➜ tafrigh --help
usage: tafrigh [-h] [--version] [--skip_if_output_exist | --no-skip_if_output_exist] [--playlist_items PLAYLIST_ITEMS]
               [--download_retries DOWNLOAD_RETRIES] [--verbose | --no-verbose] [-m MODEL_NAME_OR_PATH] [-t {transcribe,translate}]
               [-l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh}]
               [--use_faster_whisper | --no-use_faster_whisper] [--beam_size BEAM_SIZE]
               [--ct2_compute_type {default,int8,int8_float16,int16,float16}]
               [-w WIT_CLIENT_ACCESS_TOKENS [WIT_CLIENT_ACCESS_TOKENS ...]] [--max_cutting_duration [1-17]]
               [--min_words_per_segment MIN_WORDS_PER_SEGMENT] [--save_files_before_compact | --no-save_files_before_compact]
               [--save_yt_dlp_responses | --no-save_yt_dlp_responses] [--output_sample OUTPUT_SAMPLE]
               [-f {all,txt,srt,vtt,csv,tsv,json,none} [{all,txt,srt,vtt,csv,tsv,json,none} ...]] [-o OUTPUT_DIR]
               urls_or_paths [urls_or_paths ...]

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Input:
  urls_or_paths         Video/Playlist URLs or local folder/file(s) to transcribe.
  --skip_if_output_exist, --no-skip_if_output_exist
                        Whether to skip generating the output if the output file already exists.
  --playlist_items PLAYLIST_ITEMS
                        Comma separated playlist_index of the items to download. You can specify a range using "[START]:[STOP][:STEP]".
  --download_retries DOWNLOAD_RETRIES
                        Number of retries for yt-dlp downloads that fail.
  --verbose, --no-verbose
                        Whether to print out the progress and debug messages.

Whisper:
  -m MODEL_NAME_OR_PATH, --model_name_or_path MODEL_NAME_OR_PATH
                        Name or path of the Whisper model to use.
  -t {transcribe,translate}, --task {transcribe,translate}
                        Whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate').
  -l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh}, --language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh}
                        Language spoken in the audio, skip to perform language detection.
  --use_faster_whisper, --no-use_faster_whisper
                        Whether to use Faster Whisper implementation.
  --beam_size BEAM_SIZE
                        Number of beams in beam search, only applicable when temperature is zero.
  --ct2_compute_type {default,int8,int8_float16,int16,float16}
                        Quantization type applied while converting the model to CTranslate2 format.

Wit:
  -w WIT_CLIENT_ACCESS_TOKENS [WIT_CLIENT_ACCESS_TOKENS ...], --wit_client_access_tokens WIT_CLIENT_ACCESS_TOKENS [WIT_CLIENT_ACCESS_TOKENS ...]
                        List of wit.ai client access tokens. If provided, wit.ai APIs will be used to do the transcription, otherwise
                        whisper will be used.
  --max_cutting_duration [1-17]
                        The maximum allowed cutting duration. It should be between 1 and 17.

Output:
  --min_words_per_segment MIN_WORDS_PER_SEGMENT
                        The minimum number of words should appear in each transcript segment. Any segment have words count less than
                        this threshold will be merged with the next one. Pass 0 to disable this behavior.
  --save_files_before_compact, --no-save_files_before_compact
                        Saves the output files before applying the compact logic that is based on --min_words_per_segment.
  --save_yt_dlp_responses, --no-save_yt_dlp_responses
                        Whether to save the yt-dlp library JSON responses or not.
  --output_sample OUTPUT_SAMPLE
                        Samples random compacted segments from the output and generates a CSV file contains the sampled data. Pass 0 to
                        disable this behavior.
  -f {all,txt,srt,vtt,csv,tsv,json,none} [{all,txt,srt,vtt,csv,tsv,json,none} ...], --output_formats {all,txt,srt,vtt,csv,tsv,json,none} [{all,txt,srt,vtt,csv,tsv,json,none} ...]
                        Format of the output file; if not specified, all available formats will be produced.
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to save the outputs.
```

<h3>Transcription from command line</h3>

<h4>Transcribing using Whisper models</h4>

<h5>Transcribing a single material</h5>

```bash
tafrigh "https://youtu.be/dDzxYcEJbgo" \
  --model_name_or_path small \
  --task transcribe \
  --language ar \
  --output_dir . \
  --output_formats txt srt
```

<h5>Transcribing a full playlist</h5>

```bash
tafrigh "https://youtube.com/playlist?list=PLyS-PHSxRDxsLnVsPrIwnsHMO5KgLz7T5" \
  --model_name_or_path small \
  --task transcribe \
  --language ar \
  --output_dir . \
  --output_formats txt srt
```

<h5>Transcribing multiple materials</h5>

```bash
tafrigh "https://youtu.be/4h5P7jXvW98" "https://youtu.be/jpfndVSROpw" \
  --model_name_or_path small \
  --task transcribe \
  --language ar \
  --output_dir . \
  --output_formats txt srt
```

<h5>Speeding up the transcription process</h5>

<p>You can use the <code><a href="https://github.com/guillaumekln/faster-whisper">faster_whisper</a></code> library, which provides faster transcription, by passing the <code>--use_faster_whisper</code> option as follows:</p>

```bash
tafrigh "https://youtu.be/3K5Jh_-UYeA" \
  --model_name_or_path large \
  --task transcribe \
  --language ar \
  --use_faster_whisper \
  --output_dir . \
  --output_formats txt srt
```

<h4>Transcribing using wit.ai technology</h4>

<h5>Transcribing a single material</h5>

```bash
tafrigh "https://youtu.be/dDzxYcEJbgo" \
  --wit_client_access_tokens XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --output_dir . \
  --output_formats txt srt \
  --min_words_per_segment 10 \
  --max_cutting_duration 10
```

<h5>Transcribing a full playlist</h5>

```bash
tafrigh "https://youtube.com/playlist?list=PLyS-PHSxRDxsLnVsPrIwnsHMO5KgLz7T5" \
  --wit_client_access_tokens XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --output_dir . \
  --output_formats txt srt \
  --min_words_per_segment 10 \
  --max_cutting_duration 10
```

<h5>Transcribing multiple materials</h5>

```bash
tafrigh "https://youtu.be/4h5P7jXvW98" "https://youtu.be/jpfndVSROpw" \
  --wit_client_access_tokens XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --output_dir . \
  --output_formats txt srt \
  --min_words_per_segment 10 \
  --max_cutting_duration 10
```

<h3>Transcribing using code</h3>

<p>You can use Tafrigh through code as follows:</p>

```python
from tafrigh import farrigh, Config

if __name__ == '__main__':
  config = Config(
    input=Config.Input(
      urls_or_paths=['https://youtu.be/qFsUwp5iomU'],
      skip_if_output_exist=False,
      playlist_items='',
      download_retries=3,
      verbose=False,
    ),
    whisper=Config.Whisper(
      model_name_or_path='tiny',
      task='transcribe',
      language='ar',
      use_faster_whisper=True,
      beam_size=5,
      ct2_compute_type='default',
    ),
    wit=Config.Wit(
      wit_client_access_tokens=[],
      max_cutting_duration=10,
    ),
    output=Config.Output(
      min_words_per_segment=10,
      save_files_before_compact=False,
      save_yt_dlp_responses=False,
      output_sample=0,
      output_formats=['txt', 'srt'],
      output_dir='.',
    ),
  )

  for progress in farrigh(config):
    print(progress)
```

<p>The <code>farrigh</code> function is a generator that produces the current transcription state and the progress of the process. If you do not need to track this, you can skip the loop by using <code>deque</code> as follows:</p>

```python
from collections import deque

from tafrigh import farrigh, Config

if __name__ == '__main__':
  config = Config(...)

  deque(farrigh(config), maxlen=0)
```

<h3>Transcribing using Docker</h3>

<p>If you have Docker on your computer, the easiest way to use Tafrigh is through Docker. The following command downloads the Tafrigh Docker image and transcribes a YouTube material using wit.ai technologies, outputting the results in the current folder:</p>

```bash
docker run -it --rm -v "$PWD:/tafrigh" ghcr.io/ieasybooks/tafrigh \
  "https://www.youtube.com/watch?v=qFsUwp5iomU" \
  --wit_client_access_tokens XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  -f txt srt
```

<p>You can pass any option from the Tafrigh library options mentioned above.</p>

<p>There are multiple Docker images you can use for Tafrigh based on the dependencies you want to use:</p>
<ul>
  <li><code>ghcr.io/ieasybooks/tafrigh</code>: Contains dependencies for both wit.ai technologies and Whisper models</li>
  <li><code>ghcr.io/ieasybooks/tafrigh-whisper</code>: Contains dependencies for Whisper models only</li>
  <li><code>ghcr.io/ieasybooks/tafrigh-wit</code>: Contains dependencies for wit.ai technologies only</li>
</ul>

<p>One drawback is that Whisper models cannot use your computer's GPU when used through Docker, which is something we are working on resolving in the future.</p>

<hr>

<p>A significant part of this project is based on the <a href="https://github.com/m1guelpf/yt-whisper">yt-whisper</a> repository to achieve Tafrigh faster.</p>
