export interface Choice {
  text: string;
  next: string;
}

export interface StoryNode {
  title: string;
  description: string[];
  choices: Choice[];
  icon?: 'terminal' | 'map' | 'skull' | 'wifi' | 'database' | 'cpu';
}

export const story: Record<string, StoryNode> = {
  intro: {
    title: "Akademik 'Ondraszek', ul. Łużycka",
    description: [
      "Gliwice, rok 202X. Gęsty, kwaśny deszcz bębni o szyby starego akademika Politechniki Śląskiej.",
      "Jako student wydziału AEiI (Automatyki, Elektroniki i Informatyki), piszesz skrypt w Pythonie do analizy anomalii w miejskim paśmie radiowym. Systemy wykryły dziwny szum w okolicach starego miasta.",
      "Nagle na ekranie terminala pojawia się nieznany ciąg znaków. Radio na biurku zaczyna trzeszczeć, emitując niski, nienaturalny dźwięk. Nie jest to zwykłe zakłócenie. Brzmi jak rytmiczne uderzenia kilofa o skałę, zniekształcone przez cyfrowy syntezator.",
      "Odkryłeś 'Głębię' – ukrytą warstwę miasta, w której śląskie demony zintegrowały się z dawną infrastrukturą przemysłową i siecią światłowodową."
    ],
    choices: [
      { text: "Skup się na sygnale i spróbuj go zdekodować", next: "decode_signal" },
      { text: "Zignoruj to, zamknij laptopa i idź na Rynek odetchnąć", next: "rynek" }
    ],
    icon: 'terminal'
  },
  decode_signal: {
    title: "Terminal Pythona - Dekodowanie Sygnału",
    description: [
      "Wpisujesz szybką pętlę w Pythonie: `import wave, struct...`. Dysk zaczyna szumieć.",
      "Sygnał układa się we współrzędne geograficzne: 50°18'48.0\"N 18°41'20.0\"E.",
      "To dokładna lokalizacja Radiostacji Gliwickiej. Legenda głosi, że najwyższa w Europie drewniana wieża zbudowana z modrzewia skrywa coś więcej, niż tylko mroczną historię prowokacji z 1939 roku.",
      "Na terminalu wyskakuje krótka wiadomość: 'OCZEKUJEMY POD IGLICĄ. WĘGIEL I KRZEM. PRZYNIEŚ KOD.'"
    ],
    choices: [
      { text: "Zabierz sprzęt i jedź pod Radiostację Gliwicką", next: "radiostacja" },
      { text: "Zbadaj hasło 'Węgiel i Krzem' w ukrytych archiwach uczelni", next: "archiwa_polsl" }
    ],
    icon: 'cpu'
  },
  rynek: {
    title: "Gliwice Rynek - Fontanna Neptuna",
    description: [
      "Opuszczasz akademik. Mokre, brukowane uliczki starówki odbijają neonowe światła pobliskich pubów.",
      "Stajesz przy Ratuszu, tuż obok Fontanny Neptuna. Jednak woda w fontannie zachowuje się dziwnie – płynie pod prąd, a trójząb rzeźby delikatnie pulsuje niebieskim, ledowym światłem.",
      "Z cienia wyłania się postać. Jej skóra przypomina ciemny metal, a z ust wydobywa się zapach ozonu i mułu z Kłodnicy. To Utopiec, zmodernizowany przez technologię, strażnik wodnych węzłów chłodzących miejskie serwery."
    ],
    choices: [
      { text: "Spróbuj skomunikować się z cyber-Utopcem przez port podczerwieni w telefonie", next: "utopiec_talk" },
      { text: "Uciekaj w stronę Palmiarni Miejskiej, by zgubić pościg w gąszczu", next: "palmiarnia" }
    ],
    icon: 'map'
  },
  utopiec_talk: {
    title: "Transfer Danych",
    description: [
      "Przesyłasz podstawowy pakiet powitalny. Oczy Utopca błyskają na zielono.",
      "Przez głośnik w jego gardle słyszysz mechaniczny śląski akcent: 'Pierona, synku, wtykosz nos w niy swojy pliki. Ale mosz odwagę.'",
      "Utopiec wręcza ci stary, zardzewiały pendrive wyglądający jak klucz do szafki na kopalni. 'Zanieś to Skarbnikowi. Szukaj go tam, gdzie fedrowali przodkowie, a teraz kompilują kod.'",
      "Zanim zdążysz dopytać, postać rozpływa się w deszczu, zostawiając kałużę oleju."
    ],
    choices: [
      { text: "Udaj się do 'Nowych Gliwic' - dawnej Kopalni Gliwice", next: "nowe_gliwice" }
    ],
    icon: 'wifi'
  },
  radiostacja: {
    title: "Radiostacja Gliwicka",
    description: [
      "Stoisz u stóp 111-metrowej modrzewiowej wieży. W nocy jej potężna konstrukcja wygląda jak szkielet cyfrowego lewiatana.",
      "Nie ma tu żadnych strażników. Zamiast tego, drewniane belki wibrują, emitując ten sam dźwięk, który słyszałeś w akademiku. Wieża nie nadaje fal radiowych – ona pobiera energię bezpośrednio z Głębi.",
      "U podstawy iglicy widzisz otwarty właz serwisowy, z którego bije pomarańczowy blask, niczym z pieca hutniczego."
    ],
    choices: [
      { text: "Zejdź do szybu pod wieżą", next: "podziemia_radiostacji" },
      { text: "Spróbuj podpiąć laptopa do zewnętrznej skrzynki transmisyjnej", next: "hack_radiostacja" }
    ],
    icon: 'wifi'
  },
  hack_radiostacja: {
    title: "Przeciążenie Systemu",
    description: [
      "Wpinasz kabel do starego portu szeregowego. Uruchamiasz swój skrypt.",
      "Natychmiastowy atak DDoS ze strony miejskich duchów sieci (tzw. Beboków) smaży płytę główną twojego laptopa.",
      "Tracisz przytomność, gdy potężny impuls elektromagnetyczny uderza w twoje ciało. Budzisz się rano na trawniku parku Chopina, bez sprzętu i wspomnień z ostatniej nocy. Tajemnica Gliwic pozostaje nieodkryta."
    ],
    choices: [
      { text: "Zacznij od nowa", next: "intro" }
    ],
    icon: 'skull'
  },
  podziemia_radiostacji: {
    title: "Rdzeń Transmisyjny",
    description: [
      "Zchodzisz po żelaznych drabinach głęboko pod ziemię. Zamiast fundamentów, odkrywasz ogromną serwerownię zasilaną krystalicznym węglem. To tutaj dawni Ślązacy zdigitalizowali swoje dusze, by chronić je przed upadkiem przemysłu.",
      "Centralny terminal prosi o podanie kodu dostępu, o którym wspominał sygnał."
    ],
    choices: [
      { text: "Wpisz 'WĘGIEL_I_KRZEM'", next: "end_join" },
      { text: "Zniszcz terminal, by przerwać ten nienaturalny eksperyment", next: "end_destroy" }
    ],
    icon: 'database'
  },
  archiwa_polsl: {
    title: "Biblioteka Główna, ul. Kaszubska",
    description: [
      "Włamujesz się do uczelnianej bazy danych z poziomu piwnic Biblioteki Głównej.",
      "Znajdujesz plik z 1999 roku oznaczony jako 'PROJEKT: NOWE_GLIWICE_OS'. Wynika z niego, że rektorat, wspólnie z ostatnimi dyrektorami Kopalni Węgla Kamiennego 'Gliwice', przeniósł świadomość Skarbnika (ducha kopalni) do superkomputera.",
      "Skarbnik zarządza teraz całą siecią miejską, z poziomu zrewitalizowanych budynków dawnej gruby."
    ],
    choices: [
      { text: "Udaj się do Nowych Gliwic (dawna kopalnia)", next: "nowe_gliwice" }
    ],
    icon: 'database'
  },
  palmiarnia: {
    title: "Palmiarnia Miejska - Park Chopina",
    description: [
      "Biegniesz w stronę szklanych pawilonów Palmiarni. Drzwi rozsuwają się same. Wewnątrz panuje tropikalny upał, ale coś jest nie tak.",
      "Liany i pnącza mają metaliczny połysk. W gigantycznych akwariach nie pływają płaszczki, lecz nanoboty filtrujące chłodziwo dla podziemnych procesorów.",
      "Przed tobą staje Południca – hologram utknął w pętli błędu, jej twarz jest złożona z ASCII artu. 'Za zimno, za dużo danych...' szepcze syntetycznym głosem."
    ],
    choices: [
      { text: "Spróbuj naprawić jej kod z poziomu terminala", next: "fix_poludnica" },
      { text: "Zignoruj ją i poszukaj wejścia do kanałów technologicznych", next: "kanaly_tech" }
    ],
    icon: 'cpu'
  },
  fix_poludnica: {
    title: "Patchowanie Południcy",
    description: [
      "Szybko piszesz łatkę w Pythonie, korygując wyciek pamięci w jej algorytmie.",
      "Hologram stabilizuje się. Południca uśmiecha się cyfrowo i otwiera przed tobą ukrytą windę schodzącą setki metrów pod ziemię – prosto do serca dawnej kopalni."
    ],
    choices: [
      { text: "Wsiądź do windy", next: "nowe_gliwice" }
    ],
    icon: 'terminal'
  },
  kanaly_tech: {
    title: "Kanały pod Kłodnicą",
    description: [
      "Wchodzisz do wilgotnych korytarzy, przez które tłoczona jest woda z rzeki Kłodnicy.",
      "Niestety, czujniki ciśnieniowe wykrywają intruza. Grodzie zamykają się, a korytarz zalewa lodowata woda ze ściekami technologicznymi.",
      "Twój system ulega awarii. Głębia cię pochłania."
    ],
    choices: [
      { text: "Zacznij od nowa", next: "intro" }
    ],
    icon: 'skull'
  },
  nowe_gliwice: {
    title: "Centrum Edukacji i Biznesu 'Nowe Gliwice'",
    description: [
      "Docierasz do ceglanych budynków dawnej Kopalni Gliwice. Nad głową góruje charakterystyczna wieża szybowa, przekształcona w gigantyczną antenę.",
      "Wchodzisz do hali, gdzie dawniej zjeżdżały windy górnicze (szole). Zamiast maszyn wyciągowych widzisz rzędy błyszczących czarnych serwerów, ociekających kondensatem przypominającym węglowy pył.",
      "Na głównym ekranie pojawia się potężna, zjawiskowa twarz starego górnika, utkana ze światła i dymu. To Skarbnik-AI."
    ],
    choices: [
      { text: "Zaoferuj Skarbnikowi pendrive od Utopca (jeśli go masz) / Poproś o dostęp", next: "skarbnik_rozmowa" }
    ],
    icon: 'cpu'
  },
  skarbnik_rozmowa: {
    title: "Mainframe Skarbnika",
    description: [
      "Skarbnik przemawia basem, od którego drżą mury: 'Dawniej fedrowalimy węgiel. Dziś fedrujemy dane. Gliwice to serce cyfrowego Śląska, a Głębia to nasz nowy dom.'",
      "AI oferuje ci wybór: możesz zostać strażnikiem Głębi, kompilując swój umysł w sieć, by na zawsze chronić tajemnic przed korporacjami próbującymi skomercjalizować tę technologię... lub możesz odejść i zapomnieć."
    ],
    choices: [
      { text: "Zgódź się na transfer i dołącz do Cyfrowego Śląska", next: "end_join" },
      { text: "Odmów i obiecaj zachować tajemnicę", next: "end_leave" }
    ],
    icon: 'database'
  },
  end_join: {
    title: "ZAKOŃCZENIE: Cyfrowy Ślązak",
    description: [
      "Twoja świadomość łączy się z infrastrukturą miasta. Stajesz się duchem opiekuńczym wędrującym światłowodami między Politechniką, Radiostacją a Nowymi Gliwicami.",
      "Dla świata zewnętrznego byłeś po prostu studentem, który zaginął w nocnej ulewie. W Głębi jesteś nieśmiertelnym bytem – strażnikiem Krzemu i Węgla.",
      "Wygrałeś. A może przegrałeś człowieczeństwo? Nieważne. System działa stabilnie."
    ],
    choices: [
      { text: "Zagraj ponownie", next: "intro" }
    ],
    icon: 'cpu'
  },
  end_destroy: {
    title: "ZAKOŃCZENIE: Przerwanie Obwodu",
    description: [
      "Rozbijasz gaśnicą centralny terminal pod Radiostacją. Czerwone światła gasną z jękiem uchodzącego powietrza.",
      "Głębia odłącza się od fizycznego świata. Demony i cyfrowe dusze Ślązaków zostają wymazane z serwerów. Ocaliłeś miasto przed obłędem, ale zniszczyłeś największy sekret regionu.",
      "Rano budzisz się w swoim pokoju. Radio już nigdy więcej nie szumi w ten sam sposób."
    ],
    choices: [
      { text: "Zagraj ponownie", next: "intro" }
    ],
    icon: 'skull'
  },
  end_leave: {
    title: "ZAKOŃCZENIE: Powrót do Normalności",
    description: [
      "Skarbnik akceptuje twoją decyzję. Ekran gaśnie, a drzwi hali otwierają się cicho.",
      "Wracasz do akademika na Łużyckiej. Kończysz studia, znajdujesz dobrą pracę w jednym z gliwickich software house'ów.",
      "Jednak czasami, podczas pisania kodu w Pythonie, widzisz w konsoli dziwne, trzeszczące znaki. I wiesz, że Głębia wciąż tam jest, tuż pod powierzchnią miasta."
    ],
    choices: [
      { text: "Zagraj ponownie", next: "intro" }
    ],
    icon: 'map'
  }
};
