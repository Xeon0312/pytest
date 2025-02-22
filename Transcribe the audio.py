


import whisper
print("\n Loding model \n")
model = whisper.load_model("turbo", device="cuda")
print("\n Transcribe start! Please wait... \n")
result = model.transcribe(r"E:\Users\caobo\OneDrive\Document\xwechat_files\caoboyu666_7cf7\msg\file\2025-01\听力官方练习录音材料8-30\听力官方练习录音材料8-30\038246_26_CO_C_ACT19.mp3")
print("\n Transcribe complete! \n")
print(result["text"])