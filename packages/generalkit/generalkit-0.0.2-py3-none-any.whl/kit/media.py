import os.path

import ffmpy
from kit.file_utils import Files
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips


class VideoHandler:

    def video_format_converter(self, source_video, target_video):
        video = ffmpy.FFmpeg(
            inputs={source_video: None},
            outputs={target_video: None})
        video.run()

    def merge_videos(self, videos, target_file):
        all = []
        for i in videos:
            all.append(VideoFileClip(i))
        final_video = concatenate_videoclips(all)
        final_video.write_videofile(target_file)

    def audio_format_converter(self, source_file, target_file):
        cmd = 'ffmpeg.exe -y -i ' + source_file + ' -acodec pcm_s16le -f s16le -ac 1 -ar 16000 ' + target_file
        os.system(cmd)

    def cut_video_by_second(self, source_file, target_file, start_s, end_s):
        clipOri = VideoFileClip(source_file).subclip(start_s, end_s)
        clipOri.write_videofile(target_file)

    def extract_gif_from_video(self, source_file, target_file, start_s, end_s, size):
        clipOri = VideoFileClip(source_file).subclip(start_s, end_s)
        clipOri.write_gif(target_file, size)


    def extract_audio_from_video(self, source_video, target_audio):
        audio = AudioSegment.from_file(source_video)
        audio.export(target_audio, format=Files.get_file_format(target_audio))


class AudioHandler:

    def split_audio_by_ms(self, source_file, destination, duration_ms):
        f = Files.get_file_format(source_file)
        d = Files.get_file_name(source_file).replace(' ', '')
        audio = AudioSegment.from_file(source_file, format=f)

        chunks = make_chunks(audio, duration_ms)
        for i, chunk in enumerate(chunks):
            path = os.path.join(destination, d)
            Path(path).mkdir(parents=True, exist_ok=True)
            chunk_name = os.path.join(destination, d, '{}.{}'.format(i, f))
            chunk.export(chunk_name, format=f)

    def split_audio_by_second(self, source_file, destination, duration_s):
        self.split_audio_by_ms(source_file, destination, duration_s * 1000)

    def cut_audio_by_ms(self, source_file, destination, start_ms, end_ms):
        f = Files.get_file_format(source_file)
        n = Files.get_file_name(source_file)
        audio = AudioSegment.from_file(source_file, format=f)
        slice = audio[start_ms:end_ms]
        path = os.path.join(destination, '{}.{}'.format(n, f))
        slice.export(path, format=f)

    def cut_audio_by_second(self, source_file, destination, start_s, end_s):
        self.cut_audio_by_ms(source_file, destination, start_s * 1000, end_s * 1000)

    def merge_audios(self, audios, target_file):
        all_files = []
        for file in audios:
            all_files.append(AudioSegment.from_file(file))

        audio_merged = all_files[0]
        del all_files[0]
        for i in all_files:
            audio_merged += i
        audio_merged.export(target_file, format=Files.get_file_format(target_file))

