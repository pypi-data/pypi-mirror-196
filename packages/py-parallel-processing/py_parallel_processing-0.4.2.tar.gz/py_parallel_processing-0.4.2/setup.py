import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_parallel_processing",  # 소문자 영단어
    version="0.4.2",
    author="Hyeonjin Kim",  # ex) Sunkyeong Lee
    author_email="ilhj122@gmail.com",
    description="ProcessPool은 여러 개의 프로세스를 생성하여 각각의 프로세스에서 함수를 병렬로 처리할 수 있도록 도와줍니다. tqdm은 진행상황 바(progress bar)를 표시하는 라이브러리로, total인자에 전체 반복횟수를 넣어주면 반복문 진행상황을 보여줍니다.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
