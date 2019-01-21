from pydub import AudioSegment
from pydub.playback import play
song = AudioSegment.from_mp3('/home/pi/Desktop/eva/eva-audio/ingreso_dni.mp3')
play(song)
song = AudioSegment.from_mp3('/home/pi/Desktop/eva/eva-audio/pulso_inicio.mp3')
play(song)
song = AudioSegment.from_mp3('/home/pi/Desktop/eva/eva-audio/bajar_base.mp3')
play(song)