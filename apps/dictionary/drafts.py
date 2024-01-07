
# class WordPairForm(ModelForm):
#     # english_word = forms.ModelChoiceField(
#     #     queryset=ALL_ENGLISH_WORDS,
#     #     empty_label="Select the English word",
#     #     widget=forms.Select(
#     #         attrs={
#     #             "class": "form-control form-control-lg mb-3",
#     #             # "style": "display:none",
#     #             # "style": "width: 100%",
#     #             "id": "englishWords",
#     #         }
#     #     ),
#     # )
#     # root = forms.ModelChoiceField(
#     #     queryset=ALL_WORD_PAIRS,
#     #     empty_label="Select a root word. Skip if this is the root.",
#     #     widget=forms.Select(
#     #         attrs={
#     #             "class": "form-control form-control-lg mb-3",
#     #             # "style": "display:none",
#     #             # "style": "height:50px",
#     #             "id": "rootWords",
#     #         }
#     #     ),
#     # )
#     # part_of_speech = forms.ModelChoiceField(
#     #     queryset=PartOfSpeech.objects.all().order_by("code"),
#     #     empty_label="Select the part of speech",
#     #     widget=forms.Select(
#     #         attrs={
#     #             "class": "form-control form-control-lg mb-3",
#     #             # "style": "display:none",
#     #             "id": "partsOfSpeech",
#     #         }
#     #     ),
#     # )
#     # synonyms = forms.MultipleChoiceField(
#     #     widget=forms.SelectMultiple(
#     #         attrs={
#     #             "class": "form-control form-control-lg mb-3",
#     #             "multiple": "multiple",
#     #             # "style": "display:none",
#     #             "id": "synonyms",
#     #         }
#     #     ),
#     #     choices=[
#     #         (pair.id, f"{pair.root__oshindonga_word} | {pair.english_word__word}")
#     #         for pair in ALL_WORD_PAIRS
#     #     ],
#     # )

#     class Meta:
#         model = WordPair
#         fields = [
#             "english_word",
#             "oshindonga_word",
#             "root",
#             "part_of_speech",
#             "synonyms"
#         ]
#         widgets = {
#             "english_word": forms.Select(
#                 attrs={
#                     "class": "form-control form-control-lg mb-3",
#                     "selected": "Select the English word",
#                     "id": "englishWords",
#                 }
#             ),
#             "oshindonga_word": forms.TextInput(
#                 attrs={
#                     "class": "form-control form-control-lg mb-3",
#                     "placeholder": "Shanga oshitya shOshindonga",
#                 }
#             ),
#             "root": forms.Select(
#                 attrs={
#                     "class": "form-control form-control-lg mb-3",
#                     "id": "rootWords",
#                 }
#             ),
#             "part_of_speech": forms.Select(
#                 attrs={
#                     "class": "form-control form-control-lg mb-3",
#                     "id": "partsOfSpeech",
#                 }
#             ),
#             "synonyms": forms.SelectMultiple(
#                 attrs={
#                     "class": "form-control form-control-lg mb-3",
#                     "multiple": "multiple",
#                     "id": "synonyms",
#                 }
#             ),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['english_word'].queryset = EnglishWord.objects.none()
#         self.fields['root'].queryset = WordPair.objects.none()
#         self.fields['part_of_speech'].queryset = PartOfSpeech.objects.none()
#         self.fields['synonyms'].queryset = WordPair.objects.none()
#         print(f"DATA: {self.data}")

#         # if 'english_word' in self.data:
#         #     self.fields['english_word'].queryset = ALL_ENGLISH_WORDS

#         # if 'root' in self.data:
#         #     self.fields['root'].queryset = ALL_WORD_PAIRS

#         # if 'synonyms' in self.data:
#         #     self.fields['synonyms'].queryset = ALL_WORD_PAIRS

#         # if 'part_of_speech' in self.data:
#         #     self.fields['part_of_speech'].queryset = PartOfSpeech.objects.all()

#         if self.instance.pk:
#             self.fields['english_word'].queryset = ALL_ENGLISH_WORDS.filter(pk=self.instance.english_word.pk)
#             # print(f"English word ID: {self.fields['english_word'].queryset}")
#             # print(f"English word ID: {self.instance.english_word.pk}")
#             self.fields['root'].queryset = WordPair.objects.none() if not self.instance.root else ALL_WORD_PAIRS.filter(pk=self.instance.root.pk)
#             self.fields['part_of_speech'].queryset = PartOfSpeech.objects.none() if not self.instance.part_of_speech else ALL_PARTS_OF_SPEECH.filter(pk=self.instance.part_of_speech.pk)
#             # self.fields['synonyms'].queryset = ALL_WORD_PAIRS.filter(synonyms in self.instance.synonyms)

#     def clean(self):
#         cleaned_data = super().clean()
#         english_word = cleaned_data.get("english_word")
#         word_case = english_word.word_case
#         oshindonga_word = cleaned_data.get("oshindonga_word")
#         if word_case == "Abbreviation":
#             self.cleaned_data["oshindonga_word"] = oshindonga_word.strip().upper()
#         elif word_case == "Proper Noun":
#             self.cleaned_data["oshindonga_word"] = oshindonga_word.strip().capitalize()
#         else:
#             self.cleaned_data["oshindonga_word"] = oshindonga_word.strip().lower()
