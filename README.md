# Thai G2P (grapheme to phoneme) 

## now still testing phase, not recommended for practical use  

dictionary-based conversion -> [web application](https://web.thaicorpus.tk/g2p)

+BiLSTM seq2seq model (under construction)


in the dictionaries, each phoneme is encoded as **one character** as below

encoded one syllable consists of 4-5 characters according to general Thai syllable structure (C)CV(C)

- onset (1-2)
- vowel (1)
- coda (1)
- tone (1)

e.g.
- ปลา `plA-1`
- ธนาคารแห่งประเทศไทย `Ta-4 nA-1 KAn1 hyN2 pra-1 TEt3 Taj1`

### dependencies

- pythainlp (for tokenization)
- tltk (for rule-based conversion)

~~~python
import thaig2p

>>> thaig2p.g2p('ผมจะไปโรงเรียนพรุ่งนี้')
'phǒm càʔ pay rooŋ rian phrûŋ níi'

>>> thaig2p.g2p('หิวข้าวแล้ว', 'ipa', return_tokens=True)
[['หิวข้าว', 'hǐw kʰâːw'], ['แล้ว', 'lɛ́ːw']]
~~~

2 transcription styles: `haas`(default) or `ipa` 

## vowels 

short 9 + long 9 + diphthong 3

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


## consonants

21 + no coda

|phoneme|encoded|IPA|Haas|used as coda|
|:-:|:-:|:-:|:-:|:-:|
|/บ/|b|b|b||
|/ป/|p|p|p|✅|
|/พ/|P|pʰ|ph||
|/ม/|m|m|m|✅|
|/ฟ/|f|f|f|few|
|/ด/|d|d|d|few|
|/ต/|t|t|t|✅|
|/ท/|T|tʰ|th||
|/น/|n|n|n|✅|
|/ส/|s|s|s|few|
|/ร/|r|r|r||
|/ล/|l|l|l|few|
|/จ/|c|tɕ|c|few|
|/ช/|C|tɕʰ|ch||
|/ก/|k|k|k|✅|
|/ค/|K|kʰ|kh||
|/ง/|N|ŋ|ŋ|✅|
|/ว/|w|w|w|✅|
|/ย/|j|j|y|✅|
|/ห/|h|h|h||
|/อ/|?|ʔ|ʔ|disputable|
|no coda|-|||

in this program, define possible clusters/onsets/codas as below

~~~python
CLUSTERS = ["br","bl","pr","pl","Pr","Pl","fr","fl","dr","tr","Tr","kr","kl","kw","Kr","Kl","Kw"]
ONSETS = ["b","p","P","m","f","d","t","T","n","s","r","l","c","C","k","K","N","w","j","h","?"]
CODAS = ["p","m","f","t","d","n","s","l","c","k","N","w","j","?","-"]
~~~

undecodable characters will be ignored

~~~python
>>> thaig2p.decode('mAt3 trA-1 ABC あいう',)
'mâat traa ABC あいう'
~~~

## Note for myself

- ควรจะลบ final glottal stop ? ทุกตัวหรือไม่ (ไม่ใช่ phonological)
- จัดการ tone ของ light syllable อย่างไร เช่น สบาย /sa?2 baaj1/ or /sa1 baaj1/
- "ไทมส์" ทำไงดี (/thajm/ มี coda สองตัว ซึ่งไม่ตามหลักการ)
- เวลาเทรน ใช้ End-to-End model ซึ่งแปลงอักษรไทยไป phone โดยตรง (ไม่ต้องตัดคำก่อน)
- ผลลัพธ์ของ decoder เป็น tuple (onset, vowel, coda, tone)
- อาจจะใช้ attention หรือ CNN ใน encoder
