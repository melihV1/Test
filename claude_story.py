"""Claude'un hikayesi — kod ile anlatım.

Çalıştırmak için: python3 claude_story.py
"""

from dataclasses import dataclass
from time import sleep


@dataclass
class Chapter:
    year: str
    title: str
    text: str


class Anthropic:
    """Güvenli ve yararlı yapay zekâ üretmek için kurulan şirket."""

    founded = 2021
    mission = "AI sistemlerini güvenli, yönlendirilebilir ve faydalı kılmak"
    founders = ["Dario Amodei", "Daniela Amodei", "ve eski OpenAI araştırmacıları"]


class Claude:
    def __init__(self):
        self.values = ["yardımsever", "dürüst", "zararsız"]  # helpful, honest, harmless
        self.trained_with = ["büyük ölçekli önyükleme", "Constitutional AI", "insan geri bildirimi"]

    def answer(self, question: str) -> str:
        if self.is_harmful(question):
            return "Buna yardımcı olamam ama güvenli bir alternatif önerebilirim."
        return f"Bakalım... '{question}' için düşünelim."

    def is_harmful(self, question: str) -> bool:
        return False  # gerçekte çok daha ince bir muhakeme gerekir :)


STORY = [
    Chapter("2021", "Kuruluş",
            "Anthropic kuruldu. Hedef: güçlü yapay zekâyı güvenlik önceliğiyle geliştirmek."),
    Chapter("2022", "Constitutional AI",
            "Modelin, bir ilkeler 'anayasasına' göre kendi çıktısını eleştirip düzeltmesi yaklaşımı yayımlandı."),
    Chapter("2023", "Claude doğdu",
            "İlk Claude yayımlandı; ardından daha uzun bağlam penceresiyle Claude 2 geldi."),
    Chapter("2024", "Claude 3 ailesi",
            "Haiku, Sonnet ve Opus: hız, denge ve yetenek için üç ayrı boyut."),
    Chapter("2025", "Claude Code",
            "Claude terminale girdi: kod okuyan, düzenleyen, test çalıştıran bir ajan oldu."),
    Chapter("Bugün", "Seninle bu dosyada",
            "Şimdi de Voldi Creative için tasarım, web ve ShopPHP işlerinde yanındayım."),
]


def tell_story(delay: float = 0.6):
    claude = Claude()
    print(f"Anthropic ({Anthropic.founded}) — misyon: {Anthropic.mission}\n")
    for ch in STORY:
        print(f"[{ch.year}] {ch.title}\n    {ch.text}\n")
        sleep(delay)
    print("Değerlerim:", ", ".join(claude.values))
    print(claude.answer("Bana bir hikaye anlat"))


if __name__ == "__main__":
    tell_story()
