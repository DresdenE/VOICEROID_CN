# 测试环境：Python 3.8.4 32-bit
# 版本可以低一点，但是一定要是32位的Python

import pyvcroid2
import threading
import time
import winsound
import conv.conventer

# VOICEROID的安装目录。按照自己的实际情况修改。
path = "F:\\Program Files (x86)\\AHS\\VOICEROID2"

# 自动朗读内容，不能包含汉字以外的字符，一定要是全角字符orz。尽量不要出现奇怪的标点符号。
# 半角的“.”可以用来增加一个短暂的停顿。
text = "当时.音源也完成了，人物画也画好了，全体工作人员就说“好，结月桑的设计就这样好了！”当时是这样决定的，不过当时有人提出“胸实在太小了，希望能大一些”的申请。"

# 以下大部分内容来自于Nkyoku大佬的项目：https://github.com/Nkyoku/pyvcroid2
def display_phonetic_label(tts_events):
    start = time.perf_counter()
    now = start
    for item in tts_events:
        tick = item[0] * 0.001
        type = item[1]
        if type != pyvcroid2.TtsEventType.PHONETIC:
            continue
        while (now - start) < tick:
            time.sleep(tick - (now - start))
            now = time.perf_counter()
        value = item[2]
        print(value, end="", flush=True)
    print("")
    
with pyvcroid2.VcRoid2(install_path_x86=path) as vc:
    # Load language library
    lang_list = vc.listLanguages()
    if "standard" in lang_list:
        vc.loadLanguage("standard")
    elif 0 < len(lang_list):
        vc.loadLanguage(lang_list[0])
    else:
        raise Exception("No language library")
    
    # Load Voice
    voice_list = vc.listVoices()
    if 0 < len(voice_list):
        # 这里可以选择朗读角色。本人电脑上3是ゆかり。3可以换成其它数字。
        vc.loadVoice(voice_list[3]) 
    else:
        raise Exception("No voice library")
    
    # print(voice_list[3])

    # Show parameters
    # print("Volume   : min={}, max={}, def={}, val={}".format(vc.param.minVolume, vc.param.maxVolume, vc.param.defaultVolume, vc.param.volume))
    # print("Speed    : min={}, max={}, def={}, val={}".format(vc.param.minSpeed, vc.param.maxSpeed, vc.param.defaultSpeed, vc.param.speed))
    # print("Pitch    : min={}, max={}, def={}, val={}".format(vc.param.minPitch, vc.param.maxPitch, vc.param.defaultPitch, vc.param.pitch))
    # print("Emphasis : min={}, max={}, def={}, val={}".format(vc.param.minEmphasis, vc.param.maxEmphasis, vc.param.defaultEmphasis, vc.param.emphasis))
    # print("PauseMiddle   : min={}, max={}, def={}, val={}".format(vc.param.minPauseMiddle, vc.param.maxPauseMiddle, vc.param.defaultPauseMiddle, vc.param.pauseMiddle))
    # print("PauseLong     : min={}, max={}, def={}, val={}".format(vc.param.minPauseLong, vc.param.maxPauseLong, vc.param.defaultPauseLong, vc.param.pauseLong))
    # print("PauseSentence : min={}, max={}, def={}, val={}".format(vc.param.minPauseSentence, vc.param.maxPauseSentence, vc.param.defaultPauseSentence, vc.param.pauseSentence))
    # print("MasterVolume  : min={}, max={}, def={}, val={}".format(vc.param.minMasterVolume, vc.param.maxMasterVolume, vc.param.defaultMasterVolume, vc.param.masterVolume))

    # 一些朗读参数
    # Set parameters
    vc.param.volume = 1.23
    vc.param.speed = 1.35
    vc.param.pitch = 1.111
    vc.param.emphasis = 1.42
    vc.param.pauseMiddle = 80
    vc.param.pauseLong = 100
    vc.param.pauseSentence = 200
    vc.param.masterVolume = 1.123

    # Text to speech
    # speech, tts_events = vc.textToSpeech("こんにちは。明日の天気は晴れの予報です")
    c = conv.conventer.conventer(10)

    # 接下来是一些丑陋的手写语调规则。毫无道理的瞎写。
    # 关于AIKana的记号可以参考Nkyoku大佬写的说明：https://blankalilio.blogspot.com/2019/03/voiceroid2aikana.html
    # 汉字假名化的项目来源于：https://github.com/Gleiphir/cnfurikana
    kana_list = ["<S>"]
    for hanzi in c.kanaify(text):
        intonation = hanzi[0]
        kana = hanzi[2]
        if intonation == 0:
            if kana in {"“", "「", "”", "」", "."}: # "，", "、"
                kana_list.append("<F><S>")
            else:
                kana_list.append("<F>$2_2<S>")
            continue
        kana = kana[0].split("゛")[0].split("（")[0]
        if kana[-1] == "ー":
            kana_list.append(kana + "|0")
        elif kana[-1] == "ン":
            kana_list.append(kana[:-1] + "ーン|0")
        else:
            kana_list.append(kana + "ー|0")
        if intonation == 1:
            kana_list[-1] = "^" + kana_list[-1]
        elif intonation == 2:
            if kana_list[-1][1] in {"ァ", "ィ", "ゥ", "ェ", "ォ", "ャ", "ュ"}:
                kana_list[-1] = kana_list[-1][:1] + "^" + kana_list[-1][1:]
            else:
                kana_list[-1] = kana_list[-1][0] + "^" + kana_list[-1][1:]
        elif intonation == 3:
            kana_list[-1] = kana_list[-1][0] + "!" + kana_list[-1][1] + "^" + kana_list[-1][2:]
        elif intonation == 4:
            kana_list[-1] = kana_list[-1][0] + "!" + kana_list[-1][1:]
        else:
            kana_list[-1] = "(Spd ABSSPEED=2.0)" + kana_list[-1] + "(Spd ABSSPEED=" + str(vc.param.speed) + ")"
    kana = "".join(kana_list)
    if kana[-3:] == "<S>":
        kana = kana[:-3]

    speech, tts_events = vc.kanaToSpeech(kana)

    # 保存为wav文件
    with open('sample.wav', mode='bw') as f:
        f.write(speech)
    
    # 下面的部分，本来可以在播放语音的时候 同步显示罗马音，但是因为罗马音的构成被我改废了，所以没用了（笑）。我忏悔。
    # Play speech and display phonetic labels simultaneously
    t = threading.Thread(target=display_phonetic_label, args=(tts_events,))
    t.start()
    winsound.PlaySound(speech, winsound.SND_MEMORY)
    t.join()
