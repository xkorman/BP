# BP | Korman

Inštalačná príručkaAplikácia je nastavená na spustenie pomocou nástrojaDocker. Všetky časti apli-kácie sú nastavené na jeden kontajner, ktorý sa spúšťa pomocou tohto nástroja.Pre správne spustenie aplikácie je potrebné mať nainštalovanú najnovšiu verziuDocker. Pre spustenie aplikácie na novom serveri je potrebné postupovať nasle-dovne.

1. Inštalácia Docker (návod)
2. Otvorenie hlavného priečinka aplikácie BP pomocou terminálu(príkaz:cd BP)
3. Spustenie príkazu:sudo docker-compose up -d
4. Spustenie príkazu:sudo docker-compose run web
5. Aplikácia je spustená na url adrese 0.0.0.0:8000

Pri spustení kontajneru sa nainštalujú všetky potrebné knižnice, nastaví sa data-báza a skopírujú sa všetky potrebné dáta (databáza ústavov, miest, kategórie fóra a podobne), vytvorí sa admin aplikácie (meno:admin, heslo:159admin159).
