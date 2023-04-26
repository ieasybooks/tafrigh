from setuptools import setup, find_packages

setup(
    version='1.0',
    name='tafrigh',
    packages=find_packages(),
    py_modules=['tafrigh'],
    author='الكتب المٌيسّرة',
    install_requires=[
        'auditok',
        'faster-whisper @ https://github.com/guillaumekln/faster-whisper/archive/refs/heads/master.tar.gz',
        'numpy',
        'openai-whisper',
        'scipy',
        'stable-ts',
        'tqdm',
        'transformers',
        'whisper-jax @ git+https://github.com/sanchit-gandhi/whisper-jax.git',
        'yt-dlp',
    ],
    description='تفريغ النصوص وإنشاء ملفات SRT و VTT بناءً على نموذج Whisper من OpenAI.',
    entry_points={
        'console_scripts': ['tafrigh=tafrigh.cli:main'],
    },
    include_package_data=True,
)
