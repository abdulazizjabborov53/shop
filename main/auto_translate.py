import os
import time
import polib
from deep_translator import MyMemoryTranslator

LOCALE_DIR = 'locale'


def auto_translate_po():
    for root, dirs, files in os.walk(LOCALE_DIR):
        for file in files:
            if file.endswith('.po'):
                po_file_path = os.path.join(root, file)
                print(f"Tarjima qilinmoqda: {po_file_path}")

                po = polib.pofile(po_file_path)

                # MyMemoryTranslator qo'llab-quvvatlaydigan til kodlari
                if 'en' in root:
                    target_lang = 'en-US'
                elif 'ru' in root:
                    target_lang = 'ru-RU'
                else:
                    target_lang = 'uz-UZ'

                # Agar o'zi o'zbekcha bo'lsa, tarjima qilish shart emas
                if 'uz' in root:
                    continue

                translator = MyMemoryTranslator(source='uz-UZ', target=target_lang)

                entries_to_translate = [entry for entry in po if not entry.msgstr and entry.msgid]

                if not entries_to_translate:
                    print("Tarjima qilinadigan yangi so'zlar yo'q.")
                    continue

                print(f"Jami {len(entries_to_translate)} ta matn tarjima qilinmoqda...")

                for index, entry in enumerate(entries_to_translate):
                    try:
                        translated = translator.translate(entry.msgid)
                        if translated:
                            entry.msgstr = translated
                            print(
                                f"[{index + 1}/{len(entries_to_translate)}] Tarjima qilindi: {entry.msgid} -> {translated}")
                        else:
                            print(f"Tarjima topilmadi: {entry.msgid}")

                        time.sleep(1)
                    except Exception as e:
                        print(f"Xatolik ({e}), 3 sekund kutib o'tkazib yuborilyapti...")
                        time.sleep(3)

                po.save(po_file_path)
                print(f"Saqlandi va yakunlandi: {po_file_path}")


if __name__ == '__main__':
    auto_translate_po()