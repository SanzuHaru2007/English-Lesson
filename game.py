import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random

score = 0
mistakes = 0
max_mistakes = 3
duration = 5  
sample_rate = 44100

words_by_level = {
    "easy": {"кот": "cat", "собака": "dog", "яблоко": "apple", "молоко": "milk", "солнце": "sun"},
    "medium": {"банан": "banana", "школа": "school", "друг": "friend", "окно": "window", "жёлтый": "yellow"},
    "hard": {"технология": "technology", "университет": "university", "информация": "information", "произношение": "pronunciation", "воображение": "imagination"}
}

level = input("Выберите уровень сложности (easy, medium, hard): ").lower()
if level not in words_by_level:
    level = input("Неверный уровень. Выберите easy, medium или hard: ").lower()

mode = input("Выберите режим: 1 - Произношение английских слов, 2 - Перевод с русского на английский: ")
if mode not in ['1', '2']:
    mode = input("Неверный режим. Выберите 1 или 2: ")

words = list(words_by_level[level].keys())
random.shuffle(words)

recognizer = sr.Recognizer()

for word in words:
    if mistakes >= max_mistakes:
        print("Три ошибки. Игра окончена.")
        break

    if mode == '1':
        correct_word = words_by_level[level][word] 
        print(f"Произнеси слово: {correct_word}")
    else:
        correct_word = words_by_level[level][word]
        print(f"Переведи на английский: {word}")

    print("Говорите сейчас...")
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    wav.write("slovo.wav", sample_rate, recording)
    print("Запись завершена, распознаём...")

    with sr.AudioFile("slovo.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US").lower()
        print(f"Ты сказал: {text}")
        
        if text.strip() == correct_word.lower():
            score += 1
            print("Правильно! +1 очко 😊")
        else:
            mistakes += 1
            print(f"Неправильно 😔, ошибки: {mistakes}/{max_mistakes}")
            
            if mistakes >= max_mistakes:
                print("Три ошибки. Игра окончена 😢.")
                break
    
    except sr.UnknownValueError:
        print("Не удалось распознать речь 😕")
        mistakes += 1
        print(f"Считаем как ошибку. Ошибок: {mistakes}/{max_mistakes}")
        
    except sr.RequestError as e:
        print(f"Ошибка запроса: {e} 😞")
        mistakes += 1
        print(f"Считаем как ошибку. Ошибок: {mistakes}/{max_mistakes}")


print(f"Игра окончена, ваш счет за эту игру: {score} 🎉")