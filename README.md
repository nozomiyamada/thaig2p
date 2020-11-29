# Thai G2P (grapheme to phoneme) 

## now still testing phase, not recommended for practical use  

dictionary-based conversion -> [web application](https://web.thaicorpus.tk/g2p)

+BiLSTM seq2seq model (under construction)


in the dictionary, all phonemes are encoded as **one character** as below

one syllable consist of 4-5 characters

- onset (1-2)
- vowel (1)
- coda (1)
- tone (1)

e.g.
- ปลา `plA-1`
- ธนาคารแห่งประเทศไทย `Ta-4 nA-1 KAn1 hyN2 pra-1 TEt3 Taj1`

### vowels

|phoneme|encoded|IPA|Haas|
|:-:|:-:|:-:|:-:|
|/อะ/|a|a|a|
|/อา/|A|aː|aa|
|/อิ/|i|i|i|
|/อี/|I|iː|ii|
|/อุ/|u|u|u|
|/อู/|U|uː|uu|
|/อึ/|v|ɯ|ɯ|
|/อือ/|V|ɯː|ɯɯ|
|/เอะ/|e|e|e|
|/เอ/|E|eː|ee|
|/แอะ/|y|ɛ|ɛ|
|/แอ/|Y|ɛː|ɛɛ|
|/โอะ/|o|o|o|
|/โอ/|O|oː|oo|
|/เอาะ/|x|ɔ|ɔ|
|/ออ/|X|ɔː|ɔɔ|
|/เออะ/|z|ə|ə|
|/เออ/|Z|əː|əə|
|/เอีย/|J|iə|ia|
|/เอือ/|W|ɯə|ɯa|
|/อัว/|R|uə|ua|

### consonants

|phoneme|encoded|IPA|Haas|
|:-:|:-:|:-:|:-:|
|/บ/|b|b|b|
|/ป/|p|p|p|
|/พ/|P|pʰ|pʰ|
|/ม/|m|m|m|
|/ฟ/|f|f|f|
|/ด/|d|d|d|
|/ต/|t|t|t|
|/ท/|T|tʰ|tʰ|
|/น/|n|n|n|
|/ส/|s|s|s|
|/ร/|r|r|r|
|/ล/|l|l|l|
|/จ/|c|tɕ|c|
|/ช/|C|tɕʰ|cʰ|
|/ก/|k|k|k|
|/ค/|K|kʰ|kʰ|
|/ง/|N|ŋ|ŋ|
|/ว/|w|w|w|
|/ย/|j|j|y|
|/ห/|h|h|h|
|/อ/|?|ʔ|ʔ|
|no coda|-|||


* Note for myself

- "ไทมส์" ทำไงดี (/Tajm/ มี coda สองตัว ซึ่งไม่ตามหลักการ)

- เวลาเทรน ใช้ End-to-End model ซึ่งแปลงอักษรไทยไป phone โดยตรง (ไม่ต้องตัดคำก่อน)

- ผลลัพธ์ของ decoder เป็น tuple (onset, vowel, coda, tone)

- อาจจะใช้ attention หรือ CNN ใน encoder
