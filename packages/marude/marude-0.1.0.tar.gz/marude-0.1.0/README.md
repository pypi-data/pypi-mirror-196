# Marude

**Maru**sia **de**mo interface - an http api client which allows to automatically convert russian short texts into speech using [vk cloud](https://mcs.mail.ru/).

## Installation

To create a conda environment and install dependencies use the following command:

```sh
conda create -f environment.yml
```

Then activate created environment:

```sh
conda activate marude
```

## Usage

After the environment is set up, the app can be used from the command line: 

```sh
python -m marude tts 'Привет, мир' -m pavel -p message.mp3
```

The provided text (which must be 1024 characters long or shorter) will be converted into speech and saved as an audiofile `message.mp3`. By default the file is saved at `assets/message.mp3`.
